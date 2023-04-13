FROM python:3.11

WORKDIR /app
# install dependencies
COPY requirements.txt requirements.txt
RUN python3.11 -m pip install -r requirements.txt
RUN apt update && apt install dos2unix
COPY ./email_templates ./email_templates
COPY ./sh_scripts .
RUN dos2unix entrypoint.sh && dos2unix create_secrets.sh
VOLUME ["/deps"]
COPY ./src .
CMD ["/bin/bash", "entrypoint.sh"]