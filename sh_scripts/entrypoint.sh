#!/bin/sh
if [ ! -d "/secrets" ]; then
    /bin/bash /sh_scripts/create_secrets.sh
fi
# Run web service
python3.11 -m uvicorn main:app --proxy-headers --host 0.0.0.0 --port 8000 --root-path "$ROOT_PATH"