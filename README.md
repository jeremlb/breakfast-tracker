# breakfast-tracker

The project is a slack bot designed to play at Breakfast Game. This is the server part.

This application is based on :
  - Google App Engine (python Framework and Flask)

To run this project with your own data, you must :
  - Create a Google Cloud Platform project

Requirements:
  - gcloud cli tool
  - gcloud google app engine python
  - virtualenv
  - npm
  - python2.7


## Installation

```bash
# For development
$ ./bin/dev-install.sh

# Start the server
$ ./bin/dev_appserver.sh
# Go to http://localhost:8080

```

## Prepare for production

```bash
# To package the app for production
$ ./bin/prod-install.sh

# To upload your app
$ gcloud auth login your_mail@gmail.com
$ gcloud config set project gcp_project_id
$ gcloud app deploy --version=1

# When app uploaded
$ gcloud app browse
```

## Config

Add folder config in server. I removed the folder from the repos to protect my secrets data :)

- server/config
  - __init__.py
  - dev.py
  - prod.py

```python
# dev.py

from __future__ import absolute_import
from .prod import *

# Add below your dev variable config
```

```python
# prod.py

# Slack auth token
SLACK_APP_TOKEN = 'YOUR_APP_TOKEN'
```

## Licence

This project is released under the [GPL version 3][1] license.

  [1]: https://www.gnu.org/licenses/gpl.txt
