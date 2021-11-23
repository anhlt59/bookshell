# ARG build_package
ARG PYTHON_VERSION=python3.8

FROM lambci/lambda:build-python3.8

# download dev libraries
RUN yum install -y yum-utils rpmdevtools wget nano xz
# download poppler libraries
RUN yum install -y libjpeg-devel openjpeg2-devel fontconfig fontconfig-devel cmake3 cairo-devel.x86_64
RUN ln -f /usr/bin/cmake3 /usr/bin/cmake

WORKDIR /tmp
# install Poppler
RUN wget https://poppler.freedesktop.org/poppler-21.11.0.tar.xz --no-check-certificate
RUN tar -xf poppler-21.11.0.tar.xz
RUN cd poppler-21.11.0 \
    && cmake  -DCMAKE_BUILD_TYPE=Release \
       -DCMAKE_INSTALL_PREFIX=/pdftocairo \
       -DTESTDATADIR=$PWD/testfiles \
       -DENABLE_UNSTABLE_API_ABI_HEADERS=ON \
       -DENABLE_GTK_DOC=OFF \
       -DENABLE_BOOST=OFF \
    && make \
    && make DESTDIR=/tmp install

# poppler data
RUN wget https://poppler.freedesktop.org/poppler-data-0.4.11.tar.gz --no-check-certificate
RUN tar -xf poppler-data-0.4.11.tar.gz
RUN cd poppler-data-0.4.11 \
    && make prefix=/pdftocairo DESTDIR=/tmp install

#RUN yum install poppler-utils
#RUN rpmdev-extract *rpm

#WORKDIR /opt
#RUN mkdir -p /opt/poppler-21.11.0/bin && cp -P -R /tmp/*/usr/bin/* /opt/poppler-21.11.0/bin
#RUN mkdir -p /opt/poppler-21.11.0/lib && cp -P -R /tmp/*/usr/lib64/* /opt/poppler-21.11.0/lib
#RUN zip -r layer.zip /opt/pdftocairo

WORKDIR /volume
#COPY ./volume /volume
#RUN cp -r /tmp/pdftocairo /volume