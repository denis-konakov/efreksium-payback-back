#!/bin/bash
mkdir -p /deps/secrets
head -c 256 /dev/urandom > /deps/secrets/session_key.bin
