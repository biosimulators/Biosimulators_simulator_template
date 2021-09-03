# Base OS
FROM python:3.9-slim-buster

ARG VERSION="{version}"
ARG SIMULATOR_VERSION="{software verson}"

# metadata
LABEL \
    org.opencontainers.image.title="{software name}" \
    org.opencontainers.image.version="${SIMULATOR_VERSION}" \
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
    base_image="python:3.9-slim-buster" \
    version="${VERSION}" \
    software="{software name}" \
    software.version="${SIMULATOR_VERSION}" \
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

# fonts for matplotlib
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

# Copy code for command-line interface into image and install it
COPY . /root/{my_simulator_cli}
RUN pip install /root/{my_simulator_cli} \
    && rm -rf /root/{my_simulator_cli}
RUN pip install {my_simulator}==${SIMULATOR_VERSION}
ENV VERBOSE=0 \
    MPLBACKEND=PDF

# Declare the environment variables that the simulation tool supports (e.g., ALGORITHM_SUBSTITUTION_POLICY) and their default values

# Entrypoint
ENTRYPOINT ["biosimulators-{my-simulator}"]
CMD []
