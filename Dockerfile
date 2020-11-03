# Base OS
FROM python:3.7.9-slim-buster

# metadata
LABEL base_image="python:3.7.9-slim-buster"
LABEL version="0.0.1"
LABEL software="{software name}"
LABEL software.version="{software verson}"
LABEL about.summary="{software description}"
LABEL about.home="{software URL}"
LABEL about.documentation="{software documentation URL}"
LABEL about.license_file="{software license URL}"
LABEL about.license="{SPDX license id (e.g., SPDX:MIT)}"
LABEL about.tags="{comma-separated list of tags including "BioSimulators"}"
LABEL extra.identifiers.biotools="{bio.tools id}"
LABEL maintainer="{Name} <{email}>"

# Install requirements
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        ... \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy code for command-line interface into image and install it
COPY . /root/{my_simulator}
RUN pip install /root/{my_simulator}

# Entrypoint
ENTRYPOINT ["{my-simulator}"]
CMD []
