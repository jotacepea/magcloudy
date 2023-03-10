FROM ubuntu:23.04

# Install all OS dependencies for fully functional notebook server
RUN apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get -yq install --no-install-recommends \
    python3-pip \
    curl \
    git \
    unzip \
    vim \
    php8.1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*

WORKDIR /app

# Cloud
RUN whoami
# Install PHP: verify
RUN php -v
# Install cli
RUN curl -s -S https://accounts.magento.cloud/cli/installer | php
RUN cp ~/.magento-cloud/bin/magento-cloud /usr/local/bin/
RUN magento-cloud -V

# Copies the dependency files to the working directory
COPY requirements.txt /app/requirements.txt
# Install dependencies
RUN pip3 install -r requirements.txt
# Copies everything to the working directory
COPY . /app

# Command to run on container start    
CMD [ "python3" , "./app.py" ]
