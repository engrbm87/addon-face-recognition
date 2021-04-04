ARG BUILD_FROM=ghcr.io/hassio-addons/debian-base/amd64:4.1.0
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY requirements.txt /tmp/

# Setup base system
ARG BUILD_ARCH=amd64
RUN \
    apt-get -y update
RUN apt-get install -y --no-install-recommends \
        build-essential=12.6 \
        cmake=3.13.4-1 \
        python3-dev=3.7.3-1 \
        python3-wheel=0.32.3-2 \
        python3-pip=18.1-5 \
        python3-setuptools=40.8.0-1 \
        python3=3.7.3-1 \
    \
    && update-alternatives \
        --install /usr/bin/python python /usr/bin/python3 10

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt \
    \
    && find /usr/local/lib/python3.7/ -name __pycache__ -depth -exec rm -rf {} \; \
    \
    && apt-get -y autoremove \
    && apt-get -y clean \
    && rm -fr \
        /tmp/* \
        /var/{cache,log}/* \
        /var/lib/apt/lists/*

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
