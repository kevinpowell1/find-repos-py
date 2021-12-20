import csv
import os
import json
import requests
from datetime import datetime
from percentTracker import PercentTracker
import sys

org = "EBSCOIS"

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
    newRecordCount = 1
    items = []
    print("retrieving records...")
    while newRecordCount != 0:
        url = "https://api.github.com/search/repositories?q={} +in:name +org:{} &per_page=100&page={}".format(
            q, org, page)
        newRecords = gitHubApi(url)
        newRecordCount = len(newRecords["items"])
        recordCount += newRecordCount
        print(page, len(items))
        items = [*items, *newRecords["items"]]
        page += 1
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
