#!/usr/bin/env bash

docker build -t nuitka-ws-issue-native -f Dockerfile-native .
docker run nuitka-ws-issue-native
