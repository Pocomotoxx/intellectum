#!/bin/bash
set -e
python3 -m venv venv
source venv/bin/activate
if [ -d "vendor" ]; then
  if ls vendor/*.whl >/dev/null 2>&1; then
    pip install --no-index --find-links=vendor -r requirements.txt || {
      echo "Failed to install dependencies from ./vendor" >&2
      exit 1
    }
  else
    echo "No wheels found in ./vendor. Please place required packages there." >&2
    exit 1
  fi
else
  echo "Offline install requires a ./vendor directory with wheels." >&2
  exit 1
fi
cd intellektum_mvp
python manage.py migrate --noinput
cd ..
echo "Environment setup complete. Activate with 'source venv/bin/activate'"
