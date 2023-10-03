FROM ubuntu:23.04

# Install all OS dependencies for fully functional notebook server
RUN apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get -yq install --no-install-recommends \
    python3-pip \
    python3-venv \
    curl \
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
RUN curl -s -S https://accounts.magento.cloud/cli/installer | php -- --min 1.43.0 --no-interaction
RUN cp ~/.magento-cloud/bin/magento-cloud /usr/local/bin/
RUN magento-cloud -V

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1
# create and activate virtual environment
RUN python3 -m venv ${APP_PATH}/venv
ENV PATH="${APP_PATH}/venv/bin:$PATH"
# install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt
# Copies everything to the working directory
COPY . ${APP_PATH}

# Command to run on container start    
CMD [ "python3" , "./app.py" ]
