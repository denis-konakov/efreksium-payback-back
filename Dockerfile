FROM python:3.10

WORKDIR /app
# install dependencies
COPY requirements.txt requirements.txt
RUN python3.10 -m pip install -r requirements.txt

# copy project
COPY ./src .

# run entrypoint.sh
COPY ./entrypoint.sh ./entrypoint.sh
CMD ["/bin/bash", "entrypoint.sh"]