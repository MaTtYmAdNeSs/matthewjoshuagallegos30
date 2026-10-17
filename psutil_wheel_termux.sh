#!/usr/bin/env bash
set -euo pipefail

# Termux helper: build a wheel for psutil on Termux (experimental)
# Run this inside Termux. Requires clang, python, make installed.

python -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
mkdir -p wheelhouse
python -m pip wheel psutil -w wheelhouse

echo "psutil wheels in wheelhouse:"
ls -l wheelhouse
