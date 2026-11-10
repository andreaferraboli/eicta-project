#!/usr/bin/env sh
# Thin POSIX wrapper: ./scripts/eicta.sh <command> [args]
# Works from any directory and with paths containing spaces.
set -eu
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
for candidate in python3 python py; do
  # "command -v" is not enough: on Windows python3 may be a Microsoft Store stub that does not run.
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c "import sys; sys.exit(sys.version_info < (3, 10))" >/dev/null 2>&1; then
    exec "$candidate" "$DIR/eicta.py" "$@"
  fi
done
echo "ERROR: Python >= 3.10 not found" >&2
exit 1
