# -----------------------------------------------------------------------------
# Docker IMAGE congressy/cgsy
# docker build --rm -t cgsy .
# docker tag catalog <repo_url>/cgsy:<tag>
# -----------------------------------------------------------------------------
FROM python:3.8-slim

# Celery does not work with root unless you force it
ENV C_FORCE_ROOT true

LABEL indcare.image.name="xmen.magneto-ambition"

# Install packages needed to run your application (not build deps):
#   mime-support -- for mime types when serving static files
#   postgresql-client -- for running database commands
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
        nano \
        locales \
        libpcre3 \
        postgresql-client \
        build-essential \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Locales
ENV LC_ALL=pt_BR.UTF-8 LANG=pt_BR.UTF-8

RUN localedef -i pt_BR -c -f UTF-8 -A /usr/share/locale/locale.alias pt_BR.UTF-8

# -----------------------------------------------------------------------------
COPY ./Pipfile /Pipfile

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
        build-essential \
        libpcre3-dev \
        libpq-dev \
        libtiff5-dev \
        libjpeg62 \
        libjpeg62-turbo-dev \
        zlib1g-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libwebp-dev \
        libxml2-dev \
        libxslt-dev \
        python-dev \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip3 install -U pip \
    # Django packs, after pip to avoid unnecessary download
    && pip3 install --no-cache-dir -U gunicorn==20.0.4 pipenv \
    && pipenv lock --keep-outdated --requirements > requirements.txt \
    && pip3 install --no-cache-dir -r /requirements.txt \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# -----------------------------------------------------------------------------
# Setup configuration files
COPY ./bin /app_bin
COPY ./conf /app_conf

RUN chmod +x /app_conf/env/docker/container-entry.sh /app_bin/runner.sh

WORKDIR /code/

COPY ./. ./.

# server will listen on this port
EXPOSE 8000

CMD ["/app_conf/env/docker/container-entry.sh"]