# Base OS
FROM ubuntu:18.04

# metadata
LABEL base_image="ubuntu:18.04"
LABEL version="1.0.0"
LABEL software="{software name}"
LABEL software.version="{software verson}"
LABEL about.summary="{software description}"
LABEL about.home="{software URL}"
LABEL about.documentation="{software documentation URL}"
LABEL about.license_file="{software license URL}"
LABEL about.license="{SPDX license id (e.g., SPDX:MIT)}"
LABEL about.tags="{comma-separated list of tags}"
LABEL extra.identifiers.biotools="{bio.tools id}"
LABEL maintainer="{Name} <{email}>"

# Install requirements
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && pip3 install -U pip \
    && pip3 install -U setuptools \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy code for command-line interface into image and install it
COPY . /root/{my_simulator}
RUN pip3 install /root/{my_simulator}

# Entrypoint
ENTRYPOINT ["{my-simulator}"]
CMD []
