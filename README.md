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


Legal
-
(C) Copyright 2016 Postsai. replay-webhook is released as Free and Open Source Software under [MIT](https://raw.githubusercontent.com/postsai/postsai/master/LICENSE.txt) license.
