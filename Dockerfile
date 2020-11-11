# Base OS
FROM python:3.7.9-slim-buster

# metadata
LABEL \
    org.opencontainers.image.title="{software name}" \
    org.opencontainers.image.version="{software verson}" \
    org.opencontainers.image.revision="{software revision (e.g., Git hash or tag)}" \
    org.opencontainers.image.description="{software description}" \
    org.opencontainers.image.url="{software URL}" \
    org.opencontainers.image.documentation="{software documentation URL}" \
    org.opencontainers.image.source="{image source code URL}" \
    org.opencontainers.image.authors="{Name} <{email}>" \
    org.opencontainers.image.vendor="{Name}" \
    org.opencontainers.image.licenses="{SPDX license expression (e.g., MIT)}" \
    org.opencontainers.image.created="{date/time that the image was created in RFC 3339 format (e.g., 2020-11-11 10:48:55-05:00
)}" \
    \
    base_image="python:3.7.9-slim-buster" \
    version="0.0.1" \
    software="{software name}" \
    software.version="{software verson}" \
    about.summary="{software description}" \
    about.home="{software URL}" \
    about.documentation="{software documentation URL}" \
    about.license_file="{software license URL}" \
    about.license="{SPDX license id (e.g., SPDX:MIT)}" \
    about.tags="{comma-separated list of tags including "BioSimulators"}" \
    extra.identifiers.biotools="{bio.tools id}" \
    maintainer="{Name} <{email}>"

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
