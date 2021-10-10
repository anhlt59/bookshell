# ARG build_package
ARG PYTHON_VERSION=python3.8

FROM lambci/lambda:build-${PYTHON_VERSION}

# download libraries
RUN yum install -y yum-utils rpmdevtools

WORKDIR /opt
COPY ./requirements.txt /requirements.txt

# install requirements
RUN mkdir -p /opt/python/lib/${PYTHON_VERSION}/site-packages
RUN pip install -r /requirements.txt -t /opt/python/lib/${PYTHON_VERSION}/site-packages --no-cache-dir --no-index

# zip file
RUN zip -r layer.zip python