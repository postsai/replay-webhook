#!/usr/bin/python

'''
Analyses the history of a git project and replays webhooks
'''

from git import Repo
import time
import json
import urlparse
import httplib



# TODO: Do not hardcode url
REPO_URL = "https://localhost/p/test"
url = "http://localhost/postsai/api.py"

# TODO: Do not hardcode path
repo = Repo.init("/home/nhnb/workspace/HEAD/stendhal-website")


def process_commit(commit):
    files = {
        "A" : [],
        "D": [],
        "M": [],
        "R": []
    }

    # TODO: Handle first commit
    for parent in commit.parents:
        diff = parent.diff(commit)
        for change_type in ("A", "D", "R", "M"):
            for change in diff.iter_change_type(change_type):
                files[change_type].append(change.b_path)

    result = {
        "id": commit.hexsha,
        "message": commit.message,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(commit.committed_date)),
        "author": {
            "name": commit.author.name,
            "email": commit.author.email,
        },
        "committer": {
            "name": commit.committer.name,
            "email": commit.committer.email,
        },
        "added": files["A"],
        "removed": files["D"],
        "modified": files["M"],
    }
    return result


def post(branch_name, commit_list):
    result = {
        "ref" : "ref/heads/" + branch_name,
        "replay": True,
        "commits" : commit_list,
        "repository" : {
            "name" : repo.working_dir[repo.working_dir.rfind("/")+1:],
            "url" : REPO_URL
        }
    }
    start = time.time()
    u = urlparse.urlparse(url)
    con = httplib.HTTPConnection(u.hostname, u.port)
    con.request("POST", url, json.dumps(result), {"Content-Type": "application/json"})
    con.getresponse().read
    print(time.time() - start)


def process_branch(repo, branch_name):
    commits = list(repo.iter_commits(branch_name))
    commit_list = []
    i = 0
    for commit in commits:
        commit_list.append(process_commit(commit))
        i = i + 1
        if i > 200:
            post(branch_name, commit_list)
            commit_list = []
            i = 0

    if len(commit_list) > 0:
        post(branch_name, commit_list)
    



for branch in repo.heads:
    print(branch)
    process_branch(repo, branch.name)

