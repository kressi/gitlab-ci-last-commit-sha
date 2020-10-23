#!/usr/bin/env python

# Determine commit sha of last successful job
#
# $ GITLAB_API_TOKEN=<api token> \
#   CI_API_V4_URL=https://gitlab.net/api/v4 \
#   CI_PROJECT_ID=1874 \
#   CI_COMMIT_REF_NAME=master \
#   CI_COMMIT_SHA=00000000 \
#   ./sha-previous-job.py "build"
# > d5da25e9d8d5a3fcf211c9d0a12145655a696d0a


import os
import sys

from urllib3.exceptions import InsecureRequestWarning

import requests

API_TOKEN = os.environ["GITLAB_API_TOKEN"]
API_URL = os.environ["CI_API_V4_URL"]
PROJECT_ID = os.environ["CI_PROJECT_ID"]
COMMIT_REF = os.environ["CI_COMMIT_REF_NAME"]
COMMIT_SHA = os.environ["CI_COMMIT_SHA"]
NULL_SHA = "0000000000000000000000000000000000000000"


def main(job_name="build"):
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    s = requests.Session()
    s.headers.update({"PRIVATE-TOKEN": API_TOKEN})
    commit_id = None
    url = "{}".format(
        "/".join([API_URL, "projects", PROJECT_ID, "jobs?scope[]=success"])
    )
    while url and not commit_id:
        print(url, file=sys.stderr)
        resp = s.get(url, verify=False)
        url = resp.links.get("next", {}).get("url")
        if resp.ok:
            for job in resp.json():
                if job.get("ref") == COMMIT_REF and job.get("name") == job_name:
                    commit_id = job.get("commit", {}).get("id")
                    break
    if commit_id == COMMIT_SHA:
        print(NULL_SHA)
    elif commit_id:
        print(commit_id)
    else:
        print("No successful build job found", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
