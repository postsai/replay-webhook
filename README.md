replay-webhook
-

Invoke Github style webhooks from the history of an existing Git repository.

Usage
-

```
usage: replay.py [-h] --home-url URL [--name NAME] --url URL repo


optional arguments:
  --help                    show this help message and exit
  --home-url URL            Base URL of the web frontend
  --include-master-commits  Also include commits on other branches that are part
   --name NAME              Name of repository
  --url URL                 URL of the webhook to invoke

positional arguments:
  repo                      path to repository
```

Tips
-

You can checkout all remote branches as local branches with this oneliner:

``` shell
for i in `git branch -a | grep remotes/origin`; do git branch --track ${i#remotes/origin/} $i; done
```


Dependencies
-

replay-webhook dependes on python-git.

Legal
-
(C) Copyright 2016 Postsai. replay-webhook is released as Free and Open Source Software under [MIT](https://raw.githubusercontent.com/postsai/postsai/master/LICENSE.txt) license.
