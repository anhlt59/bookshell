ARG PYTHON_VERSION=3.7-slim-buster

FROM python:${PYTHON_VERSION} as python

# Python 'build' stage -------------------------------------------------------------------------------
FROM python as build-stage

# Install apt packages
RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip wheel --wheel-dir /usr/src/app/wheels -r /requirements/dev.txt

# Python 'run' stage --------------------------------------------------------------------------------
FROM python as run-stage
ARG APP_HOME=/app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV CHROMIUM_BINARY_FILE_PATH=/usr/bin/chromium
ENV CHROME_DRIVER_FILE_PATH=/usr/bin/chromedriver

WORKDIR $APP_HOME

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y chromium chromium-driver \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from build-stage
COPY --from=build-stage /usr/src/app/wheels /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
	&& rm -rf /wheels

# copy application code to WORKDIR
COPY ./src "${APP_HOME}/src"

# Python 'production' stage -------------------------------------------------------------------------------
FROM run-stage as production-stage
ARG APP_HOME=/app

WORKDIR $APP_HOME
COPY ./config/production "${APP_HOME}/config"

# Python 'staging' stage -------------------------------------------------------------------------------
FROM run-stage as staging-stage
ARG APP_HOME=/app

WORKDIR $APP_HOME
COPY ./config/staging "${APP_HOME}/config"

# Python 'testing' stage -------------------------------------------------------------------------------
FROM run-stage as testing-stage
ARG APP_HOME=/app
ENV AWS_DEFAULT_REGION=us-east-1
ENV AWS_ACCESS_KEY_ID=local
ENV AWS_SECRET_ACCESS_KEY=local

WORKDIR $APP_HOME
COPY ./config "${APP_HOME}/config"
COPY ./tests ./tests
COPY ./requirements ./requirements
RUN pip install -r requirements/test.txt

ENTRYPOINT [ "python", "-m", "pytest", "./tests/providers", "./tests/articles", "./tests/handler" ]
