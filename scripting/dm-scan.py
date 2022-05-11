import requests
import dataset

import timeutils

db = dataset.connect('sqlite:///data.db')
jobs_table = db['jobs']

PRIVATE_TOKEN=""
GITLAB_URL="git.xx.network"
PROJECT_FULL_NAME="elixxir%2Fdropped-messages-auto-test"

# https://{}/api/v4/projects/{}/jobs/artifacts/master/raw/delayedpickup/results/clients/parser.txt?job=droptest

# https://{}/elixxir/{}/-/jobs/{}/artifacts/raw/delayedpickup/results/clients/parser.txt

# https://git.xx.network/api/v4/projects/elixxir%2Fdropped-messages-auto-test/jobs/13950/artifacts/raw/delayedpickup/results/clients/parser.txt

for PAGE in range(1, 200):
    pipelines_r=requests.get("https://{}/api/v4/projects/{}/pipelines?per_page=100&page={}".format(GITLAB_URL, PROJECT_FULL_NAME, PAGE), headers={"PRIVATE-TOKEN":PRIVATE_TOKEN})

    for pipeline in pipelines_r.json():
        # Ignore cancelled jobs, these are human known to be broken
        # Also skip running, since results are not known yet
        if pipeline["status"] == "canceled" or pipeline["status"] == "running":
            continue

        # We already have a record of this job
        if type(jobs_table.find_one(pipeline_id=pipeline["id"])) != type(None):
            continue

        pipeline_jobs_r=requests.get("https://{}/api/v4/projects/{}/pipelines/{}/jobs".format(GITLAB_URL, PROJECT_FULL_NAME, pipeline["id"]), headers={"PRIVATE-TOKEN":PRIVATE_TOKEN})

        for job in pipeline_jobs_r.json():
            # We only care about droptest results
            if job["name"] != "droptest":
                continue

            job_log_url = "https://{}/api/v4/projects/{}/jobs/{}/trace".format(GITLAB_URL, PROJECT_FULL_NAME, job["id"])
            job_log_r = requests.get(job_log_url, headers={"PRIVATE-TOKEN":PRIVATE_TOKEN})
            job_log = job_log_r.text
            length_s = ""
            for line in job_log.split("\n"):
                if line.startswith("Sleep time "):
                    length_s = line

            parser_results = requests.get("https://{}/api/v4/projects/{}/jobs/{}/artifacts/delayedpickup/results/clients/parser.txt".format(GITLAB_URL, PROJECT_FULL_NAME, job["id"])).text

            jobs_table.insert(dict(
                pipeline_id    = pipeline["id"],
                status         = job["status"],
                length         = length_s.replace("Sleep time ", ""),
                id             = job["id"],
                started_time   = timeutils.str_timestamp_to_epoch(job["started_at"]),
                finished_time  = timeutils.str_timestamp_to_epoch(job["finished_at"]),
                job_log        = job_log,
                parser_results = parser_results,
            ))

            print("{}, {}, {}".format(job["status"], length_s, "https://git.xx.network/elixxir/dropped-messages-auto-test/-/jobs/{}".format(job["id"])))