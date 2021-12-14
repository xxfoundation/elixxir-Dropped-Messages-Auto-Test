#!/usr/bin/env python3
import subprocess


def main():
    num_sessions = int(input("How many sessions do you want to create?\n"))
    for i in range(num_sessions):
        " hello --ndf results/ndf.json --waitTimeout 240 --unsafe-channel-creation -v $DEBUGLEVEL"
        make_dir = ["mkdir", f"generatedsessions/{i}"]
        subprocess.run(make_dir)

        command1 = ["./bin/client", "--password", "hello", "--ndf", "delayedpickup/results/ndf.json", "--waitTimeout",
                    "240", "--unsafe-channel-creation", "-l", "generators.log", "-s", f"generatedsessions/{i}/sender",
                    "--unsafe", "-m", "\"Hello from Rick42 to myself, without E2E Encryption\""]

        command2 = ["./bin/client", "--password", "hello", "--ndf", "delayedpickup/results/ndf.json", "--waitTimeout",
                    "240", "--unsafe-channel-creation", "-l", "generators.log", "-s", f"generatedsessions/{i}/receiver",
                    "--unsafe", "-m", "\"Hello from Rick42 to myself, without E2E Encryption\""]

        subprocess.run(command1)
        subprocess.run(command2)

        tar = ["tar", "-czvf", f"generatedsessions/{i}.tar.gz", f"generatedsessions/{i}"]
        subprocess.run(tar)

    print("done")


if __name__ == "__main__":
    main()
