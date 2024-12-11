#!/bin/bash

set -e

if [[ ! -f unique_id ]]; then
    echo $RANDOM > unique_id
fi

docker run -it $(docker build -q . -f Dockerfile.lint)
docker run -it $(docker build -q .)

