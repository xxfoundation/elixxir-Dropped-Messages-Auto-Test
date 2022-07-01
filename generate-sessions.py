#!/usr/bin/env python3
import subprocess
import shutil

def genSessionsForFolder(num_sessions, folder):
    for i in range(num_sessions):
        " hello --ndf results/ndf.json --waitTimeout 240 --unsafe-channel-creation -v $DEBUGLEVEL"
        make_dir = ["mkdir", "-p", f"generatedsessions/{folder}"]
        subprocess.run(make_dir)
        make_dir = ["mkdir", "-p", f"generatedsessions/temp"]
        subprocess.run(make_dir)

        command1 = ["./bin/client", "--password", "hello", "--ndf", "delayedpickup/results/ndf.json", "--waitTimeout",
                    "240", "--unsafe-channel-creation", "-l", "generators.log", "-s", f"generatedsessions/temp/sender",
                    "--unsafe", "-m", "\"Hello from Rick42 to myself, without E2E Encryption\""]

        command2 = ["./bin/client", "--password", "hello", "--ndf", "delayedpickup/results/ndf.json", "--waitTimeout",
                    "240", "--unsafe-channel-creation", "-l", "generators.log", "-s", f"generatedsessions/temp/receiver",
                    "--unsafe", "-m", "\"Hello from Rick42 to myself, without E2E Encryption\""]

        subprocess.run(command1)
        subprocess.run(command2)

        tar = ["tar", "-czvf", f"generatedsessions/{folder}/{i}.tar.gz", "generatedsessions/temp"]
        subprocess.run(tar)

        shutil.rmtree("generatedsessions/temp")

    print("done")


if __name__ == "__main__":
    for length in ["1210000", "14400", "172800", "259200", "3600", "43200", "604800", "86400"]:
        genSessionsForFolder(5, length)
    genSessionsForFolder(10, "600")
