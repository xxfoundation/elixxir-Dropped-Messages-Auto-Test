import requests

PRIVATE_TOKEN=""
GITLAB_URL="git.xx.network"
PROJECT_FULL_NAME="elixxir%2Fdropped-messages-auto-test"

for PAGE in range(1, 3):
    pipelines_r=requests.get("https://{}/api/v4/projects/{}/pipelines?per_page=100&page={}&status=running".format(GITLAB_URL, PROJECT_FULL_NAME, PAGE), headers={"PRIVATE-TOKEN":PRIVATE_TOKEN})

    for pipeline in pipelines_r.json():
        # Ignore cancelled jobs, these are human known to be broken
        # Also skip running, since results are not known yet
        if pipeline["status"] != "running":
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
            
            if "Too many client registrations. Try again later" in job_log:
                requests.post("https://{}/api/v4/projects/{}/pipelines/{}/cancel".format(GITLAB_URL, PROJECT_FULL_NAME, pipeline["id"]), headers={"PRIVATE-TOKEN":PRIVATE_TOKEN})
                print("Cancelled TMCR dead job: {}, {}".format(length_s, "https://git.xx.network/elixxir/dropped-messages-auto-test/-/jobs/{}".format(job["id"])))

            if ("*"*240) in job_log:
                requests.post("https://{}/api/v4/projects/{}/pipelines/{}/cancel".format(GITLAB_URL, PROJECT_FULL_NAME, pipeline["id"]), headers={"PRIVATE-TOKEN":PRIVATE_TOKEN})
                print("Cancelled stall registration dead job: {}, {}".format(length_s, "https://git.xx.network/elixxir/dropped-messages-auto-test/-/jobs/{}".format(job["id"])))
            
            if "FATAL" in job_log:
                requests.post("https://{}/api/v4/projects/{}/pipelines/{}/cancel".format(GITLAB_URL, PROJECT_FULL_NAME, pipeline["id"]), headers={"PRIVATE-TOKEN":PRIVATE_TOKEN})
                print("Cancelled FATAL'd dead job: {}, {}".format(length_s, "https://git.xx.network/elixxir/dropped-messages-auto-test/-/jobs/{}".format(job["id"])))