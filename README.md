# find-repos-py

## Purpose

`findRepos.py` is a python script that locates repos based on a string. It generates a CSV file with the full repo name and the last user to commit to that repo. 

## Requirements

[Python 3](https://www.python.org/downloads/)

## Usage

- Clone repo
- Add [Github Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) to your own local `secrets.json` file
- Replace `MYORG` on line 9 of `findRepos.py`
- `cd to/repo/directory`
- `python3 findRepos.py a-string-without-spaces`
