FROM python:3.11

WORKDIR /app
# install dependencies
COPY requirements.txt requirements.txt
RUN python3.11 -m pip install -r requirements.txt

# copy project
COPY ./src .

# init secrets


# run entrypoint.sh
COPY ./sh_scripts .
CMD ["/bin/bash", "entrypoint.sh"]