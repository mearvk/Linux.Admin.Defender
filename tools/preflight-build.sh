#!/bin/sh
# Verification gate: callers must provide a trusted SHA-256 manifest.
# Do not build if verification fails.
set -eu

MANIFEST=${1:?usage: preflight-build.sh <manifest> [root]}
ROOT=${2:-.}
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

python3 "$SCRIPT_DIR/verify-before-execution.py" --manifest "$MANIFEST" --root "$ROOT"

echo "preflight: SHA-256 verification passed; build may proceed"
