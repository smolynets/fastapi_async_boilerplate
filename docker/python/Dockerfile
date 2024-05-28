# *********** START FILE ************ #
FROM ubuntu:20.04
# --
LABEL owner="Oleh Smolynets"
LABEL maintainer="Oleh Smolynets"
# Enviroments.
ENV VIRTUAL_ENV="/opt/env"
ENV PATH_VIRT_ENV="$VIRT_ENV/bin:$PATH"
# --
ENV USR="maintainer"
ENV U_ID=1001
# --
ENV GRP=$USR
ENV G_ID=$U_ID
# --
ENV SHELL="/bin/sh"
# --
ENV SUDOERS="/etc/sudoers.d/$USR"
ENV WRKDIR="/app"
ENV HOME="/workspace"
# Install miniOS.
RUN DEBIAN_FRONTEND=$DEBIAN_FRONTEND apt-get update -q                \
    && apt-get install -y -qq python3.8 python3-pip python3-venv sudo \
    && apt-get install netcat -y                                      \
    && apt-get autoclean                                              \
    && apt-get autoremove                                             \
    && rm -rf /var//apt/liblists/*
# Create User + user items.
RUN groupadd -g $G_ID $GRP
RUN adduser                                             \
    --system                                            \
    --home $HOME --shell $SHELL --uid $U_ID --gecos ""  \
    --disabled-password                                 \
    --disabled-login $USR                               \
    && echo "$USR ALL=(ALL) NOPASSWD:ALL" >> $SUDOERS   \
    && chmod 0440 $SUDOERS                              \
    && mkdir -p $WRKDIR                                 \
    && chown -R $USR:$GRP $HOME                         \
    && chmod -R a+rwx $HOME                             \
    && chown -R $USR:$GRP $HOME                         \
    && chmod -R a+rwx $HOME
# Init User.
USER $USR
# Add prjct files.
COPY . $WRKDIR
# Create Virtual enviroment.
RUN sudo -H python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH_VIRT_ENV"
# Iinit work dir.
WORKDIR $WRKDIR
# Add permissions.
RUN sudo -H chgrp -R 0 $WRKDIR                                           \
    && sudo -H chmod -R g=u $WRKDIR                                      \
    && sudo -H chmod -R o+wr $WRKDIR                                     \
    && sudo -H chown -R $USR:$GRP $WRKDIR                                \
    && sudo -H chown -R $USR:$GRP $VIRTUAL_ENV                           \
    && sudo -H chmod -R a+rwx $VIRTUAL_ENV
# Install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -Ur ./docker/python/requirements.txt --no-cache-dir
# *********** END FILE ************ #
