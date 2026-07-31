#!/usr/bin/env bash

SCRIPT_DIR=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)
ENV_PATH="${SCRIPT_DIR}/../.env"

export $(grep -v '^#' ${ENV_PATH} | xargs)

npx openapi-typescript ${API_URL_OPENAPI} -o "${SCRIPT_DIR}/../src/api/schema.ts"