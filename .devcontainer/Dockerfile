FROM jetblackpope/pybuntu:3.8-bionic

ARG DEBIAN_FRONTEND=noninteractive
ENV PIPENV_MAX_SUBPROCESS 64
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update

RUN apt-get install --no-install-recommends --no-install-suggests -y \
    apt-utils \
    dialog

RUN apt-get install --no-install-recommends --no-install-suggests -y \
    git \
    openssh-client \
    iproute2 \
    procps

RUN apt-get install --no-install-recommends --no-install-suggests -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common \
    lsb-release

RUN curl -fsSL https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]')/gpg | (OUT=$(apt-key add - 2>&1) || echo $OUT) \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]') $(lsb_release -cs) stable" \
    && apt-get update \
    && apt-get install -y docker-ce-cli \
    #
    # Install Docker Compose
    && curl -sSL "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

RUN python -m pip install pip pipenv --upgrade

RUN echo "export PROMPT_COMMAND='history -a'" >> "/root/.bashrc" \
        && echo "export HISTFILE=/root/commandhistory/.bash_history" >> "/root/.bashrc" \
        && echo "alias yaml2json=\"python -c 'import sys, yaml, json; json.dump(yaml.load(sys.stdin), sys.stdout, indent=4)'\"" >> "/root/.bashrc"

WORKDIR /code