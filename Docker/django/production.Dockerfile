ARG PYTHON_VERSION=3.9-slim-buster

FROM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as python-build-stage

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential

# Requirements are installed here to ensure they will be cached.
COPY ./requirements .
RUN pip wheel --wheel-dir /usr/src/app/wheels -r requirements/production.txt


# Python 'run' stage
FROM python as python-run-stage
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
	&& rm -rf /wheels/

# copy application code to WORKDIR
COPY --chown=django:django . /app

# make django owner of the WORKDIR directory as well.
RUN chown django:django /app

USER django

CMD ["python", "manage.py", "runserver"]