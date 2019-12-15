#!/usr/bin/env bash

docker build -t nuitka-ws-issue-nuitka -f Dockerfile-nuitka .
docker run nuitka-ws-issue-nuitka
