#!/usr/bin/env bash

# abort on error
set -e

DATA_SERVICE_DIR=$( dirname "${BASH_SOURCE[0]}")/../.

RPC_PATH=${DATA_SERVICE_DIR}/webserver/rpc
GRPC_BUILD_GEN_PATH=${RPC_PATH}/gen/build
PROTO_GEN_PATH=${RPC_PATH}/gen/proto

# clean previous build
rm -rf "${GRPC_BUILD_GEN_PATH}" "${PROTO_GEN_PATH}"
mkdir -p "${GRPC_BUILD_GEN_PATH}" "${PROTO_GEN_PATH}"

PYTHONPATH=$DATA_SERVICE_DIR poetry run python "${RPC_PATH}"/gen_proto.py gen-proto-for-services >> "${PROTO_GEN_PATH}"/TalentminerContainer.proto

poetry run python -m grpc_tools.protoc \
    --proto_path="${PROTO_GEN_PATH}" \
    --grpc_python_out="${GRPC_BUILD_GEN_PATH}" \
    --python_out="${GRPC_BUILD_GEN_PATH}" \
    --mypy_out=quiet:"${GRPC_BUILD_GEN_PATH}" \
    "${PROTO_GEN_PATH}"/TalentminerContainer.proto

find "${GRPC_BUILD_GEN_PATH}" -type f -exec realpath {} \;
