FROM python:3.8-slim-bullseye as python

# Python build stage
FROM python as build-stage

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements .
# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels -r security.txt

# Python 'run' stage
FROM python as run-stage

ARG APP_HOME=/app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ${APP_HOME}

# copy python dependency wheels from build-stage
COPY --from=build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* && rm -rf /wheels/

ADD . ${APP_HOME}/

EXPOSE 5025

CMD [ "gunicorn", "--bind", "0.0.0.0:5000" ]
