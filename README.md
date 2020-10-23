# Gitlab CI: Last commit SHA
Iterate through pages of jobs to find commit SHA of last successful
job run of a branch (commit ref)

```bash
$ GITLAB_API_TOKEN=<api token> \
  CI_API_V4_URL=https://gitlab.net/api/v4 \
  CI_PROJECT_ID=1874 \
  CI_COMMIT_REF_NAME=master \
  CI_COMMIT_SHA=00000000 \
  ./sha-previous-job.py "build"

> d5da25e9d8d5a3fcf211c9d0a12145655a696d0a
```
