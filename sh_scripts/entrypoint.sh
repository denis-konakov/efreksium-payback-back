#!/bin/bash
if [ ! -d "/deps/secrets" ]; then
    /bin/bash create_secrets.sh
fi
if [ ! -d "/email_templates" ]; then
    cp -r ./email_templates /email_templates/
fi
# Run web service
python3.11 -m uvicorn main:app --proxy-headers --host 0.0.0.0 --port 8000 --root-path "$ROOT_PATH"