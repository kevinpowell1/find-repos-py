import csv
import os
import json
import requests
from datetime import datetime
from percentTracker import PercentTracker
import sys

org = "+org:EBSCOIS"

# SECRETS ARE PULLED FROM A LOCAL secrets.json FILE.

secretsPath = "secrets.json"
with open(secretsPath) as f:
    secrets = json.load(f)

# Client for pinging GitHub API


def gitHubApi(url):
    payload = {}
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'Bearer {}'.format(secrets["githubToken"])
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    respJson = json.loads(response.text)
    return respJson

# Gets last commit of provided repo


def getLastCommit(repo):
    url = "https://api.github.com/repos/{}/commits".format(repo)
    commits = gitHubApi(url)
    return commits[0]["commit"]["author"]["name"]

# Finds repos based on query string and writes report


def findTestRepos(q):
    recordCount = 0
    page = 1
    url = "https://api.github.com/search/repositories?q={} +in:name {}&per_page=100&page={}".format(
        q, org, page)
    records = gitHubApi(url)
    totalRecords = records["total_count"]
    recordCount += len(records["items"])
    items = records["items"]
    print("retrieving records...")
    while recordCount != totalRecords:
        page += 1
        url = "https://api.github.com/search/repositories?q={} +in:name {}&per_page=100&page={}".format(
            q, org, page)
        newRecords = gitHubApi(url)
        recordCount += len(newRecords["items"])
        items = [*items, *newRecords["items"]]
    rows = []
    print("finding commits...")
    percent_tracker = PercentTracker()
    percent_tracker.amount = len(items)
    for i in items:
        percent_tracker.print_message(i["full_name"])
        row = {"repoName": i["full_name"],
               "lastCommitter": getLastCommit(i["full_name"])}
        rows.append(row)
    date = datetime.now().strftime("%Y%m%d")
    csvpath = "reports/{}-{}-repos.csv".format(date, sys.argv[-1])
    print()
    print("writing report!")
    with open(csvpath, mode='w', encoding='utf-8') as csvfile:
        csv_writer = csv.DictWriter(
            csvfile, fieldnames=["repoName", "lastCommitter"])
        csv_writer.writeheader()
        csv_writer.writerows(rows)
    print(csvpath)


if not sys.argv[-1].endswith(".py"):
    findTestRepos(sys.argv[-1])
