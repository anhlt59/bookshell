ARG PYTHON_VERSION=3.10

FROM public.ecr.aws/lambda/python:${PYTHON_VERSION} as build-stage

# install dev tools
RUN yum group install -y "Development Tools" \
    && yum install -y wget yum-utils rpmdevtools

# copy python dependencies
COPY ./requirements/lambda.txt /requirements.txt
RUN pip install wheel
RUN pip wheel --wheel-dir /usr/src/app/wheels -r /requirements.txt

# download chrome and chromedriver
WORKDIR /tmp
# download packages
RUN curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-57/beta-headless-chromium-amazonlinux-2.zip > headless-chromium.zip
RUN curl -SL https://chromedriver.storage.googleapis.com/87.0.4280.20/chromedriver_linux64.zip > chromedriver.zip
RUN yumdownloader --resolve libX11-devel

# get binaries & libs
RUN mkdir /opt/bin /opt/lib /opt/share
RUN unzip headless-chromium.zip -d /opt/bin
RUN unzip chromedriver.zip -d /opt/bin
RUN rpmdev-extract *rpm
RUN cp -r /tmp/*/usr/lib64/* /opt/lib/ && \
    cp -r /tmp/*/usr/share/* /opt/share/
RUN ln -f /opt/lib/libXau.so.6.0.0 /opt/lib/libXau.so.6 && \
    ln -f /opt/lib/libX11-xcb.so.1.0.0 /opt/lib/libX11-xcb.so.1

# clean up
RUN rm -rf /tmp/* && yum clean all

# RUNTIME --------------------------------------------------------------------------------
FROM public.ecr.aws/lambda/python:${PYTHON_VERSION} as run-stage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV CHROMIUM_BINARY_FILE_PATH=/opt/bin/headless-chromium
ENV CHROME_DRIVER_FILE_PATH=/opt/bin/chromedriver

# download chrome and chromedriver
RUN mkdir /opt/bin /opt/lib /opt/share
COPY --from=build-stage /opt /opt

# copy python dependency wheels from build-stage
# then use wheels to install python dependencies
COPY --from=build-stage /usr/src/app/wheels /wheels/
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
	&& rm -rf /wheels

# copy application code to LAMBDA_TASK_ROOT
WORKDIR $LAMBDA_TASK_ROOT
COPY ./src "${LAMBDA_TASK_ROOT}/src"
COPY ./data/google_scraper "${LAMBDA_TASK_ROOT}/data/google_scraper"

# Python 'production' stage -------------------------------------------------------------------------------
FROM run-stage as production-stage
COPY ./config/production "${LAMBDA_TASK_ROOT}/config"

# Python 'staging' stage -------------------------------------------------------------------------------
FROM run-stage as staging-stage
COPY ./config/staging "${LAMBDA_TASK_ROOT}/config"

FROM run-stage as testing-stage
COPY ./chrome.py "${LAMBDA_TASK_ROOT}/chrome.py"
COPY ./config "${LAMBDA_TASK_ROOT}/config"
