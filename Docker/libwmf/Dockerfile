# libwmf
FROM lambci/lambda:build-python3.8

# download libraries
RUN yum install -y yum-utils rpmdevtools

WORKDIR /tmp
RUN yumdownloader --resolve libwmf-0.2.8.4
RUN yumdownloader --resolve gsfonts
RUN rm -f bzip2-libs-1.0.6-13.amzn2.0.3.i686.rpm && \
  rm -f freetype-2.8-14.amzn2.1.i686.rpm && \
  rm -f gdk-pixbuf2-2.36.12-3.amzn2.i686.rpm && \
  rm -f glib2-2.56.1-9.amzn2.0.2.i686.rpm && \
  rm -f glibc-2.26-56.amzn2.i686.rpm && \
  rm -f jasper-libs-1.900.1-33.amzn2.i686.rpm && \
  rm -f jbigkit-libs-2.0-11.amzn2.0.2.i686.rpm && \
  rm -f libX11-1.6.7-3.amzn2.0.2.i686.rpm && \
  rm -f libXau-1.0.8-2.1.amzn2.0.2.i686.rpm && \
  rm -f libblkid-2.30.2-2.amzn2.0.5.i686.rpm && \
  rm -f libffi-3.0.13-18.amzn2.0.2.i686.rpm && \
  rm -f libgcc-7.3.1-13.amzn2.i686.rpm && \
  rm -f libjpeg-turbo-2.0.90-2.amzn2.0.1.i686.rpm && \
  rm -f libmount-2.30.2-2.amzn2.0.5.i686.rpm && \
  rm -f libpng-1.5.13-8.amzn2.i686.rpm && \
  rm -f libselinux-2.5-12.amzn2.0.2.i686.rpm && \
  rm -f libsepol-2.5-8.1.amzn2.0.2.i686.rpm && \
  rm -f libstdc++-7.3.1-13.amzn2.i686.rpm && \
  rm -f libtiff-4.0.3-35.amzn2.i686.rpm && \
  rm -f libuuid-2.30.2-2.amzn2.0.5.i686.rpm && \
  rm -f libwmf-0.2.8.4-44.amzn2.0.1.i686.rpm && \
  rm -f libwmf-lite-0.2.8.4-44.amzn2.0.1.i686.rpm && \
  rm -f libxcb-1.12-1.amzn2.0.2.i686.rpm && \
  rm -f libxml2-2.9.1-6.amzn2.5.4.i686.rpm && \
  rm -f pcre-8.32-17.amzn2.0.2.i686.rpm && \
  rm -f xz-libs-5.2.2-1.amzn2.0.2.i686.rpm && \
  rm -f zlib-1.2.7-18.amzn2.i686.rpm
RUN rpmdev-extract *rpm

# install libraries and set hard links
WORKDIR /opt
RUN mkdir /opt/bin && cp -ri /tmp/*/usr/bin/* /opt/bin
RUN mkdir /opt/lib && cp -r /tmp/*/usr/lib/* /opt/lib && cp -r /tmp/*/usr/lib64/* /opt/lib
RUN mkdir -p /opt/share/fontconfig && mkdir -p /opt/share/fonts
RUN cp -r /tmp/*/usr/share/fontconfig/* /opt/share/fontconfig \
  && cp -r /tmp/*/usr/share/fonts/* /opt/share/fonts \
  && cp -r /tmp/*/usr/share/libwmf/* /opt/share/fonts
RUN cp /usr/lib64/libxml2.so.2 /opt/lib/libxml2.so.2
#RUN cd /opt/lib && find -type l -exec bash -c 'ln -f "$(readlink -m "$0")" "$0"' {} \;

RUN ln -f /bin/cpp /opt/lib/cpp && \
  ln -f /lib64/libBrokenLocale.so.1 /opt/lib/libBrokenLocale.so && \
  ln -f /opt/lib/libICE.so.6.3.0 /opt/lib/libICE.so.6 && \
  ln -f /opt/lib/libSM.so.6.0.1 /opt/lib/libSM.so.6 && \
  ln -f /opt/lib/libX11-xcb.so.1.0.0 /opt/lib/libX11-xcb.so.1 && \
  ln -f /opt/lib/libX11.so.6.3.0 /opt/lib/libX11.so.6 && \
  ln -f /opt/lib/libXau.so.6.0.0 /opt/lib/libXau.so.6 && \
  ln -f /opt/lib/libXcursor.so.1.0.2 /opt/lib/libXcursor.so.1 && \
  ln -f /opt/lib/libXext.so.6.4.0 /opt/lib/libXext.so.6 && \
  ln -f /opt/lib/libXfixes.so.3.1.0 /opt/lib/libXfixes.so.3 && \
  ln -f /opt/lib/libXi.so.6.1.0 /opt/lib/libXi.so.6 && \
  ln -f /opt/lib/libXinerama.so.1.0.0 /opt/lib/libXinerama.so.1 && \
  ln -f /opt/lib/libXmu.so.6.2.0 /opt/lib/libXmu.so.6 && \
  ln -f /opt/lib/libXmuu.so.1.0.0 /opt/lib/libXmuu.so.1 && \
  ln -f /opt/lib/libXrandr.so.2.2.0 /opt/lib/libXrandr.so.2 && \
  ln -f /opt/lib/libXrender.so.1.3.0 /opt/lib/libXrender.so.1 && \
  ln -f /opt/lib/libXt.so.6.0.0 /opt/lib/libXt.so.6 && \
  ln -f /opt/lib/libXxf86misc.so.1.1.0 /opt/lib/libXxf86misc.so.1 && \
  ln -f /opt/lib/libXxf86vm.so.1.0.0 /opt/lib/libXxf86vm.so.1 && \
  ln -f /lib64/libanl.so.1 /opt/lib/libanl.so && \
  ln -f /opt/lib/libasan.so.4.0.0 /opt/lib/libasan.so.4 && \
  ln -f /opt/lib/libatomic.so.1.2.0 /opt/lib/libatomic.so.1 && \
  ln -f /opt/lib/libblkid.so.1.1.0 /opt/lib/libblkid.so.1 && \
  ln -f /opt/lib/libbz2.so.1.0.6 /opt/lib/libbz2.so.1 && \
  ln -f /lib64/libcidn.so.1 /opt/lib/libcidn.so && \
  ln -f /opt/lib/libcilkrts.so.5.0.0 /opt/lib/libcilkrts.so.5 && \
  ln -f /lib64/libcrypt.so.1 /opt/lib/libcrypt.so && \
  ln -f /lib64/libdl.so.2 /opt/lib/libdl.so && \
  ln -f /opt/lib/libfdisk.so.1.1.0 /opt/lib/libfdisk.so.1 && \
  ln -f /opt/lib/libfontconfig.so.1.11.1 /opt/lib/libfontconfig.so.1 && \
  ln -f /opt/lib/libfontenc.so.1.0.0 /opt/lib/libfontenc.so.1 && \
  ln -f /opt/lib/libfreetype.so.6.14.0 /opt/lib/libfreetype.so.6 && \
  ln -f /opt/lib/libgdk_pixbuf-2.0.so.0.3612.0 /opt/lib/libgdk_pixbuf-2.0.so.0 && \
  ln -f /opt/lib/libgdk_pixbuf_xlib-2.0.so.0.3612.0 /opt/lib/libgdk_pixbuf_xlib-2.0.so.0 && \
  ln -f /opt/lib/libgio-2.0.so.0.5600.1 /opt/lib/libgio-2.0.so.0 && \
  ln -f /opt/lib/libglib-2.0.so.0.5600.1 /opt/lib/libglib-2.0.so.0 && \
  ln -f /opt/lib/libgmodule-2.0.so.0.5600.1 /opt/lib/libgmodule-2.0.so.0 && \
  ln -f /opt/lib/libgobject-2.0.so.0.5600.1 /opt/lib/libgobject-2.0.so.0 && \
  ln -f /opt/lib/libgomp.so.1.0.0 /opt/lib/libgomp.so.1 && \
  ln -f /opt/lib/libgthread-2.0.so.0.5600.1 /opt/lib/libgthread-2.0.so.0 && \
  ln -f /opt/lib/libitm.so.1.0.0 /opt/lib/libitm.so.1 && \
  ln -f /opt/lib/libjasper.so.1.0.0 /opt/lib/libjasper.so.1 && \
  ln -f /opt/lib/libjpeg.so.62.3.0 /opt/lib/libjpeg.so.62 && \
  ln -f /opt/lib/liblsan.so.0.0.0 /opt/lib/liblsan.so.0 && \
  ln -f /opt/lib/libmount.so.1.1.0 /opt/lib/libmount.so.1 && \
  ln -f /opt/lib/libmpx.so.2.0.1 /opt/lib/libmpx.so.2 && \
  ln -f /opt/lib/libmpxwrappers.so.2.0.1 /opt/lib/libmpxwrappers.so.2 && \
  ln -f /lib64/libmvec.so.1 /opt/lib/libmvec.so && \
  ln -f /lib64/libnsl.so.1 /opt/lib/libnsl.so && \
  ln -f /opt/lib/libpng15.so.15.13.0 /opt/lib/libpng15.so.15 && \
  ln -f /opt/lib/libquadmath.so.0.0.0 /opt/lib/libquadmath.so.0 && \
  ln -f /lib64/libresolv.so.2 /opt/lib/libresolv.so && \
  ln -f /lib64/librt.so.1 /opt/lib/librt.so && \
  ln -f /opt/lib/libsmartcols.so.1.1.0 /opt/lib/libsmartcols.so.1 && \
  ln -f /opt/lib/libstdc++.so.6.0.24 /opt/lib/libstdc++.so.6 && \
  ln -f /lib64/libthread_db.so.1 /opt/lib/libthread_db.so && \
  ln -f /opt/lib/libtiff.so.5.2.0 /opt/lib/libtiff.so.5 && \
  ln -f /opt/lib/libtiffxx.so.5.2.0 /opt/lib/libtiffxx.so.5 && \
  ln -f /opt/lib/libtsan.so.0.0.0 /opt/lib/libtsan.so.0 && \
  ln -f /opt/lib/libubsan.so.0.0.0 /opt/lib/libubsan.so.0 && \
  ln -f /lib64/libutil.so.1 /opt/lib/libutil.so && \
  ln -f /opt/lib/libuuid.so.1.3.0 /opt/lib/libuuid.so.1 && \
  ln -f /opt/lib/libwmf-0.2.so.7.1.0 /opt/lib/libwmf-0.2.so.7 && \
  ln -f /opt/lib/libwmflite-0.2.so.7.0.1 /opt/lib/libwmflite-0.2.so.7 && \
  ln -f /opt/lib/libxcb-composite.so.0.0.0 /opt/lib/libxcb-composite.so.0 && \
  ln -f /opt/lib/libxcb-damage.so.0.0.0 /opt/lib/libxcb-damage.so.0 && \
  ln -f /opt/lib/libxcb-dpms.so.0.0.0 /opt/lib/libxcb-dpms.so.0 && \
  ln -f /opt/lib/libxcb-dri2.so.0.0.0 /opt/lib/libxcb-dri2.so.0 && \
  ln -f /opt/lib/libxcb-dri3.so.0.0.0 /opt/lib/libxcb-dri3.so.0 && \
  ln -f /opt/lib/libxcb-glx.so.0.0.0 /opt/lib/libxcb-glx.so.0 && \
  ln -f /opt/lib/libxcb-present.so.0.0.0 /opt/lib/libxcb-present.so.0 && \
  ln -f /opt/lib/libxcb-randr.so.0.1.0 /opt/lib/libxcb-randr.so.0 && \
  ln -f /opt/lib/libxcb-record.so.0.0.0 /opt/lib/libxcb-record.so.0 && \
  ln -f /opt/lib/libxcb-render.so.0.0.0 /opt/lib/libxcb-render.so.0 && \
  ln -f /opt/lib/libxcb-res.so.0.0.0 /opt/lib/libxcb-res.so.0 && \
  ln -f /opt/lib/libxcb-screensaver.so.0.0.0 /opt/lib/libxcb-screensaver.so.0 && \
  ln -f /opt/lib/libxcb-shape.so.0.0.0 /opt/lib/libxcb-shape.so.0 && \
  ln -f /opt/lib/libxcb-shm.so.0.0.0 /opt/lib/libxcb-shm.so.0 && \
  ln -f /opt/lib/libxcb-sync.so.1.0.0 /opt/lib/libxcb-sync.so.1 && \
  ln -f /opt/lib/libxcb-xevie.so.0.0.0 /opt/lib/libxcb-xevie.so.0 && \
  ln -f /opt/lib/libxcb-xf86dri.so.0.0.0 /opt/lib/libxcb-xf86dri.so.0 && \
  ln -f /opt/lib/libxcb-xfixes.so.0.0.0 /opt/lib/libxcb-xfixes.so.0 && \
  ln -f /opt/lib/libxcb-xinerama.so.0.0.0 /opt/lib/libxcb-xinerama.so.0 && \
  ln -f /opt/lib/libxcb-xinput.so.0.1.0 /opt/lib/libxcb-xinput.so.0 && \
  ln -f /opt/lib/libxcb-xkb.so.1.0.0 /opt/lib/libxcb-xkb.so.1 && \
  ln -f /opt/lib/libxcb-xselinux.so.0.0.0 /opt/lib/libxcb-xselinux.so.0 && \
  ln -f /opt/lib/libxcb-xtest.so.0.0.0 /opt/lib/libxcb-xtest.so.0 && \
  ln -f /opt/lib/libxcb-xv.so.0.0.0 /opt/lib/libxcb-xv.so.0 && \
  ln -f /opt/lib/libxcb-xvmc.so.0.0.0 /opt/lib/libxcb-xvmc.so.0 && \
  ln -f /opt/lib/libxcb.so.1.1.0 /opt/lib/libxcb.so.1

RUN rm -f /opt/lib/libICE.so.6.3.0 && \
  rm -f /opt/lib/libSM.so.6.0.1 && \
  rm -f /opt/lib/libX11-xcb.so.1.0.0 && \
  rm -f /opt/lib/libX11.so.6.3.0 && \
  rm -f /opt/lib/libXau.so.6.0.0 && \
  rm -f /opt/lib/libXcursor.so.1.0.2 && \
  rm -f /opt/lib/libXext.so.6.4.0 && \
  rm -f /opt/lib/libXfixes.so.3.1.0 && \
  rm -f /opt/lib/libXi.so.6.1.0 && \
  rm -f /opt/lib/libXinerama.so.1.0.0 && \
  rm -f /opt/lib/libXmu.so.6.2.0 && \
  rm -f /opt/lib/libXmuu.so.1.0.0 && \
  rm -f /opt/lib/libXrandr.so.2.2.0 && \
  rm -f /opt/lib/libXrender.so.1.3.0 && \
  rm -f /opt/lib/libXt.so.6.0.0 && \
  rm -f /opt/lib/libXxf86misc.so.1.1.0 && \
  rm -f /opt/lib/libXxf86vm.so.1.0.0 && \
  rm -f /opt/lib/libasan.so.4.0.0 && \
  rm -f /opt/lib/libatomic.so.1.2.0 && \
  rm -f /opt/lib/libblkid.so.1.1.0 && \
  rm -f /opt/lib/libbz2.so.1.0.6 && \
  rm -f /opt/lib/libcilkrts.so.5.0.0 && \
  rm -f /opt/lib/libfdisk.so.1.1.0 && \
  rm -f /opt/lib/libfontconfig.so.1.11.1 && \
  rm -f /opt/lib/libfontenc.so.1.0.0 && \
  rm -f /opt/lib/libfreetype.so.6.14.0 && \
  rm -f /opt/lib/libgdk_pixbuf-2.0.so.0.3612.0 && \
  rm -f /opt/lib/libgdk_pixbuf_xlib-2.0.so.0.3612.0 && \
  rm -f /opt/lib/libgio-2.0.so.0.5600.1 && \
  rm -f /opt/lib/libglib-2.0.so.0.5600.1 && \
  rm -f /opt/lib/libgmodule-2.0.so.0.5600.1 && \
  rm -f /opt/lib/libgobject-2.0.so.0.5600.1 && \
  rm -f /opt/lib/libgomp.so.1.0.0 && \
  rm -f /opt/lib/libgthread-2.0.so.0.5600.1 && \
  rm -f /opt/lib/libitm.so.1.0.0 && \
  rm -f /opt/lib/libjasper.so.1.0.0 && \
  rm -f /opt/lib/libjpeg.so.62.3.0 && \
  rm -f /opt/lib/liblsan.so.0.0.0 && \
  rm -f /opt/lib/libmount.so.1.1.0 && \
  rm -f /opt/lib/libmpx.so.2.0.1 && \
  rm -f /opt/lib/libmpxwrappers.so.2.0.1 && \
  rm -f /opt/lib/libpng15.so.15.13.0 && \
  rm -f /opt/lib/libquadmath.so.0.0.0 && \
  rm -f /opt/lib/libsmartcols.so.1.1.0 && \
  rm -f /opt/lib/libstdc++.so.6.0.24 && \
  rm -f /opt/lib/libtiff.so.5.2.0 && \
  rm -f /opt/lib/libtiffxx.so.5.2.0 && \
  rm -f /opt/lib/libtsan.so.0.0.0 && \
  rm -f /opt/lib/libubsan.so.0.0.0 && \
  rm -f /opt/lib/libuuid.so.1.3.0 && \
  rm -f /opt/lib/libwmf-0.2.so.7.1.0 && \
  rm -f /opt/lib/libwmflite-0.2.so.7.0.1 && \
  rm -f /opt/lib/libxcb-composite.so.0.0.0 && \
  rm -f /opt/lib/libxcb-damage.so.0.0.0 && \
  rm -f /opt/lib/libxcb-dpms.so.0.0.0 && \
  rm -f /opt/lib/libxcb-dri2.so.0.0.0 && \
  rm -f /opt/lib/libxcb-dri3.so.0.0.0 && \
  rm -f /opt/lib/libxcb-glx.so.0.0.0 && \
  rm -f /opt/lib/libxcb-present.so.0.0.0 && \
  rm -f /opt/lib/libxcb-randr.so.0.1.0 && \
  rm -f /opt/lib/libxcb-record.so.0.0.0 && \
  rm -f /opt/lib/libxcb-render.so.0.0.0 && \
  rm -f /opt/lib/libxcb-res.so.0.0.0 && \
  rm -f /opt/lib/libxcb-screensaver.so.0.0.0 && \
  rm -f /opt/lib/libxcb-shape.so.0.0.0 && \
  rm -f /opt/lib/libxcb-shm.so.0.0.0 && \
  rm -f /opt/lib/libxcb-sync.so.1.0.0 && \
  rm -f /opt/lib/libxcb-xevie.so.0.0.0 && \
  rm -f /opt/lib/libxcb-xf86dri.so.0.0.0 && \
  rm -f /opt/lib/libxcb-xfixes.so.0.0.0 && \
  rm -f /opt/lib/libxcb-xinerama.so.0.0.0 && \
  rm -f /opt/lib/libxcb-xinput.so.0.1.0 && \
  rm -f /opt/lib/libxcb-xkb.so.1.0.0 && \
  rm -f /opt/lib/libxcb-xselinux.so.0.0.0 && \
  rm -f /opt/lib/libxcb-xtest.so.0.0.0 && \
  rm -f /opt/lib/libxcb-xv.so.0.0.0 && \
  rm -f /opt/lib/libxcb-xvmc.so.0.0.0 && \
  rm -f /opt/lib/libxcb.so.1.1.0

RUN zip -r layer.zip lib bin share
