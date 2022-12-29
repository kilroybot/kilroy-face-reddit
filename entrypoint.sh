#!/bin/bash --login

set +euo pipefail
conda activate kilroy-face-reddit
set -euo pipefail

exec "$@"
