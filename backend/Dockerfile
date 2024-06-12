FROM ubuntu:23.04

# Install all OS dependencies for fully functional notebook server
RUN apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get -yq install --no-install-recommends \
    python3-pip \
    python3-venv \
    curl \
    wget \
    git \
    unzip \
    vim \
    php8.1 \
    openssh-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*

ENV APP_PATH='/app'
WORKDIR ${APP_PATH}

# Cloud
RUN whoami
# SSH config
RUN mkdir ~/.ssh \
    && touch ~/.ssh/config \
    && echo "Host *" > ~/.ssh/config \
    && echo "  StrictHostKeyChecking=no" >> ~/.ssh/config \
    && echo "  UserKnownHostsFile=/dev/null" >> ~/.ssh/config
# Install PHP: verify
RUN php -v
# Install cli
RUN curl -s -S https://accounts.magento.cloud/cli/installer | php -- --min 1.46.1 --no-interaction
RUN cp ~/.magento-cloud/bin/magento-cloud /usr/local/bin/
RUN magento-cloud -V

# Install Fastly cli
ENV FASTLY_CLI_VER='10.7.0'
RUN wget https://github.com/fastly/cli/releases/download/v${FASTLY_CLI_VER}/fastly_${FASTLY_CLI_VER}_linux_arm64.deb
RUN apt-get install -y ./fastly_${FASTLY_CLI_VER}_linux_arm64.deb
RUN fastly version

# Install NewRelic cli
ENV NR_CLI_VER='0.78.1'
ENV NR_OS='Linux'
ENV NR_ARCH='arm64'
ENV NR_RELEASE_URL="https://download.newrelic.com/install/newrelic-cli/v${NR_CLI_VER}/newrelic-cli_${NR_CLI_VER}_${NR_OS}_${NR_ARCH}.tar.gz"
RUN wget "${NR_RELEASE_URL}"
RUN tar -xzvf newrelic-cli_${NR_CLI_VER}_${NR_OS}_${NR_ARCH}.tar.gz
RUN mv newrelic /usr/local/bin/newrelic-cli && chmod +x /usr/local/bin/newrelic-cli && chown root:0 /usr/local/bin/newrelic-cli
RUN newrelic-cli help

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1
# create and activate virtual environment (not really needed, because it is a container, but it is a good practice!)
RUN python3 -m venv ${APP_PATH}/venv
ENV PATH="${APP_PATH}/venv/bin:$PATH"
# install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt
# Copies everything to the working directory
COPY . ${APP_PATH}

ENV DEFAULT_SERVICE_PORT='5000'
# Command to run on container start    
CMD [ "python3" , "./app.py" ]
