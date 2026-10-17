#!/usr/bin/env bash
set -euo pipefail

# Build a wheel for this project into ./dist and copy into ./wheelhouse
python -m pip install --upgrade pip setuptools wheel build
python -m build --wheel
mkdir -p wheelhouse
cp dist/*.whl wheelhouse/

echo "Built wheels:"
ls -l wheelhouse
