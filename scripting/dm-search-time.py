import dataset
import argparse

import timeutils

parser = argparse.ArgumentParser(description='Dropped Messages Results Cache Search Tool')
parser.add_argument('-l','--length', help='Length of CI job to find.', required=False, type=str)
parser.add_argument('-a','--after-time', help='Search jobs after this time. Defaults to 1 week ago.', required=False, type=str, default="1 week ago")
parser.add_argument('-s','--stop-time', help='Stops the search of jobs after this time.', required=False, type=str, default="now")
args = vars(parser.parse_args())

db = dataset.connect('sqlite:///data.db')
jobs_table = db['jobs']

after_epoch = timeutils.human_input_to_epoch(args["after_time"])
stop_epoch = timeutils.human_input_to_epoch(args["stop_time"])

matched_jobs = []

success = 0
failed = 0

for job in jobs_table.find(started_time={'>=': after_epoch}):
    if int(job["started_time"]) > stop_epoch:
        continue

    if args["length"]:
        job_length = int(job["length"])
        if args["length"].startswith(">="):
            if job_length >= int(args["length"][2:]):
                matched_jobs.append(job)

        elif args["length"].startswith(">"):
            if job_length > int(args["length"][1:]):
                matched_jobs.append(job)

        elif args["length"].startswith("<="):
            if job_length <= int(args["length"][2:]):
                matched_jobs.append(job)

        elif args["length"].startswith("<"):
            if job_length < int(args["length"][1:]):
                matched_jobs.append(job)

        else:
            if job_length == int(args["length"]):
                matched_jobs.append(job)
    else:
        matched_jobs.append(job)

for job in matched_jobs:
    if job["status"] == "success":
        success += 1
    elif job["status"] == "failed":
        failed += 1
    else:
        print("Got unknown status code {}".format(job["status"]))
        
    parser_lines = job["parser_results"].split("\n")
    dropped_line = ""
    if len(parser_lines) < 2:
        dropped_line = parser_lines[-1]
    else:
        dropped_line = parser_lines[-2]

    print("{}, {}, {}, {}, {}".format(
        job["status"], 
        job["length"], 
        job["started_time"], 
        "https://git.xx.network/elixxir/dropped-messages-auto-test/-/jobs/{}".format(job["id"]), 
        dropped_line
    ))

print("Success: {}, failed: {}, success rate: {}%".format(success, failed, round((success/(success+failed))*100)))