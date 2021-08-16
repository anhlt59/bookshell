FROM nikolaik/python-nodejs:python3.8-nodejs12

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # cleaning up unsued files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# requirements are installed here to ensure they will be cached
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /serverless

RUN npm install -g serverless \
  serverless-python-requirements \
  serverless-offline

RUN aws configure set aws_access_key_id root
RUN aws configure set aws_secret_access_key abc@123456
RUN aws configure set default.region eu-central-1

ENTRYPOINT ["/entrypoint.sh"]