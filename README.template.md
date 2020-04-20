# my_simulator
BioSimulations-compliant command-line interface to the [MySimulator](https://<url.for.my.simulator>/) simulation program.

## Contents
* [Installation](#installation)
* [Usage](#usage)
* [License](#license)
* [Development team](#development-team)
* [Questions and comments](#questions-and-comments)

## Installation

### Install Python package
```
pip install git+https://github.com/<organization>/<repository>
```

### Install Docker image
```
docker pull <organization>/<repository>
```

## Local usage
```
usage: <my-simulator> [-h] [-d] [-q] -i ARCHIVE [-o OUT_DIR] [-v]

BioSimulations-compliant command-line interface to the <MySimulator> simulation program <https://url.for.my.simulator>.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           full application debug mode
  -q, --quiet           suppress all console output
  -i ARCHIVE, --archive ARCHIVE
                        Path to OMEX file which contains one or more SED-ML-
                        encoded simulation experiments
  -o OUT_DIR, --out-dir OUT_DIR
                        Directory to save outputs
  -v, --version         show program's version number and exit
```

## Usage through Docker container
```
docker run \
  --tty \
  --rm \
  --mount type=bind,source="$(pwd)"/tests/fixtures,target=/root/in,readonly \
  --mount type=bind,source="$(pwd)"/tests/results,target=/root/out \
  <organization>/<repository>:latest \
    -i /root/in/BIOMD0000000297.omex \
    -o /root/out
```

## License
This package is released under the [<License name (e.g., MIT)> license](LICENSE).

## Development team
This package was developed by [<authors>](<https://url.for.authors>).

## Questions and comments
Please contact the [<authors>](mailto:<authors@url.for.authors>) with any questions or comments.
