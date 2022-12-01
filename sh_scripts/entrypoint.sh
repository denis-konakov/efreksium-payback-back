#!/bin/sh
if [ ! -d "/secrets" ]; then
    /bin/bash /sh_scripts/create_secrets.sh
fi
python3.10 -m uvicorn main:app --host 0.0.0.0 --port 8000
