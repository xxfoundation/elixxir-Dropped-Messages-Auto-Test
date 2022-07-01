#!/usr/bin/env bash

rm -rf bin
mkdir bin

while [ ! -f "bin/client" ]; do
    if [ "$(uname)" == "Darwin" ]; then
        curl -s -f -L -H "PRIVATE-TOKEN: $GITLAB_ACCESS_TOKEN" -o "bin/client" "https://git.xx.network/api/v4/projects/elixxir%2Fclient/jobs/artifacts/hotfix%2FIntegrationFixes/raw/release/client.darwin64?job=build"
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        curl -s -f -L -H "PRIVATE-TOKEN: $GITLAB_ACCESS_TOKEN" -o "bin/client" "https://git.xx.network/api/v4/projects/elixxir%2Fclient/jobs/artifacts/hotfix%2FIntegrationFixes/raw/release/client.linux64?job=build"
    fi
    sleep 1
done

chmod +x bin/client
if [ "$(uname)" == "Darwin" ]; then
    xattr -c bin/client
fi