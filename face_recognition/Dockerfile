ARG BUILD_FROM=ghcr.io/hassio-addons/debian-base/amd64:5.0.0
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY requirements.txt /tmp/

# We need to copy in the patches need during build
COPY rootfs/patches /patches

# Setup base system
ARG BUILD_ARCH=amd64
RUN \
    apt-get -y update \
    \
    && apt-get install -y --no-install-recommends \
        build-essential=12.9 \
        cmake=3.18.4-2 \
        python3-dev=3.9.2-3 \
        python3-wheel=0.34.2-1 \
        python3-pip=20.3.4-4 \
        python3-setuptools=52.0.0-4 \
        python3-bcrypt=3.1.7-4 \
        python3=3.9.2-3 \
        libjpeg-dev=1:2.0.6-4 \
        zlib1g-dev=1:1.2.11.dfsg-2 \
        libffi-dev=3.3-6 \
        libssl-dev=1.1.1k-1 \
    \
    && update-alternatives \
        --install /usr/bin/python python /usr/bin/python3 10 \
    \
    && pip3 install --no-cache-dir -r /tmp/requirements.txt \
    \
    && pip3 install \
        --no-cache-dir \
        --prefer-binary \
        --find-links "https://wheels.home-assistant.io/alpine-3.13/${BUILD_ARCH}/" \
        appdaemon==4.1.0 \
    \
    && cd /usr/local/lib/python3.9/dist-packages/ \
    && patch -p1 < /patches/force_recompile.patch \
    && patch -p1 < /patches/hassio.patch \
    && find /usr/local \
        \( -type d -a -name test -o -name tests -o -name '__pycache__' \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    \
    && apt-get -y autoremove \
    && apt-get -y clean \
    && apt-get -y remove --purge \
        build-essential \
        cmake \
        python3-dev \
        python3-wheel \
        libffi-dev \
        libssl-dev \
    && rm -fr \
        /tmp/* \
        /var/{cache,log}/* \
        /var/lib/apt/lists/*

COPY rootfs /

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

# Labels
LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="Rami Mousleh" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="Home Assistant Add-ons" \
    org.opencontainers.image.authors="Rami Mousleh" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://addons.community" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/main/README.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}
