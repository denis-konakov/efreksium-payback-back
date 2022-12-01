#!/bin/sh
# check if the secrets folder exists
if [ ! -d "/secrets" ]; then
    echo "The secrets folder does not exist. Creating it..."
    /bin/bash
fi
python3.10 -m uvicorn main:app --host 0.0.0.0 --port 8000