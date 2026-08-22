#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BROKEN_LOG="$(mktemp)"
trap 'rm -f "$BROKEN_LOG"' EXIT

if mvn -B -q -f "$ROOT_DIR/broken/pom.xml" clean package >"$BROKEN_LOG" 2>&1; then
  echo "FAIL: the deliberately broken project unexpectedly compiled" >&2
  exit 1
fi

mvn -B -q -f "$ROOT_DIR/fixed/pom.xml" clean package
echo "PASS: broken build rejected; repaired build verified"
