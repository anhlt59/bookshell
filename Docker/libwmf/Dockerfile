# libwmf
FROM amazonlinux:latest

# download libraries
RUN yum install -y yum-utils rpmdevtools

WORKDIR /tmp
RUN yumdownloader --resolve libwmf-0.2.8.4 && rpmdev-extract *rpm

# install libraries and set hard links
WORKDIR /opt
RUN mkdir /opt/bin && cp -ri /tmp/*/usr/bin/* /opt/bin
RUN mkdir /opt/share && cp -r /tmp/*/usr/share/* /opt/share
RUN mkdir /opt/lib && cp -r /tmp/*/usr/lib/* /opt/lib && cp -r /tmp/*/usr/lib64/* /opt/lib
RUN cd /opt/lib && find -type l -exec bash -c 'ln -f "$(readlink -m "$0")" "$0"' {} \;

RUN zip -r layer.zip lib bin share