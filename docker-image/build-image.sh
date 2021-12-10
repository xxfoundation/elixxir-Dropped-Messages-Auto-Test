set -e
docker build -t docker-registry.xx.network/elixxir/dropped-messages-auto-test .
docker push docker-registry.xx.network/elixxir/dropped-messages-auto-test