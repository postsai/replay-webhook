#!/usr/bin/python

'''
Analyses the history of a git project and replays webhooks
'''

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import sys
from git import Repo
import time
import json
import urlparse
import httplib

class ReplayWebhook:
    """Replays webhooks calls from the existing history of a git repository"""


    def __init__(self, url, repo_path, name, home_url):
        self.url = url
        self.repo = Repo.init(repo_path)
        self.repo_name = name
        if name == "":
            self.repo_name = self.repo.working_dir[self.repo.working_dir.rfind("/")+1:]
        self.home_url = home_url


    @staticmethod
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


    def post(self, branch_name, commit_list):
        result = {
            "ref" : "ref/heads/" + branch_name,
            "replay": True,
            "commits" : commit_list,
            "repository" : {
                "name" : self.repo_name,
                "url" : self.home_url
            }
        }
        start = time.time()
        u = urlparse.urlparse(self.url)
        con = httplib.HTTPConnection(u.hostname, u.port)
        con.request("POST", self.url, json.dumps(result), {"Content-Type": "application/json"})
        con.getresponse().read
        print(time.time() - start)


    def process_branch(self, branch_name):
        commits = list(self.repo.iter_commits(branch_name))
        commit_list = []
        i = 0
        for commit in commits:
            commit_list.append(self.process_commit(commit))
            i = i + 1
            if i > 200:
                self.post(branch_name, commit_list)
                commit_list = []
                i = 0

        if len(commit_list) > 0:
            self.post(branch_name, commit_list)

    def process(self):
        for branch in self.repo.heads:
            print(branch)
            self.process_branch(branch.name)


def main():
    '''Main'''
    
    try:
        # Setup argument parser
        parser = ArgumentParser(description="Replay Webhooks", formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("--home-url", dest="home_url", metavar="URL", required=True, help="Base URL of the web frontend")
        parser.add_argument("--name", dest="name", metavar="NAME", default="", help="Name of repository")
        parser.add_argument("--url", dest="url", metavar="URL", required=True, help="URL of the webhook to invoke")
        parser.add_argument(dest="repo", help="path to repository", metavar="repo")

        # Process arguments
        args = parser.parse_args()
        ReplayWebhook(args.url, args.repo, args.name, args.home_url).process()

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        sys.stderr.write(repr(e) + "\n")
        sys.stderr.write("  for help use --help")
        return 2

if __name__ == "__main__":
    sys.exit(main())
