[![Latest release](https://img.shields.io/github/v/tag/<owner>/<repo>)](https://github.com/<owner>/<repo>/releases)
[![PyPI](https://img.shields.io/pypi/v/<my-simulator>)](https://pypi.org/project/<my-simulator>/)
[![CI status](https://github.com/<owner>/<repo>/workflows/Continuous%20integration/badge.svg)](https://github.com/<owner>/<repo>/actions?query=workflow%3A%22Continuous+integration%22)
[![Test coverage](https://codecov.io/gh/<owner>/<repo>/branch/dev/graph/badge.svg)](https://codecov.io/gh/<owner>/<repo>)
[![All Contributors](https://img.shields.io/github/all-contributors/<owner>/<repo>/HEAD)](#contributors-)

# MySimulator
BioSimulators-compliant command-line interface to the [MySimulator](https://<url.for.my.simulator>/) simulation program.

## Installation

### Install Python package
```
pip install <repository>
```

### Install Docker image
```
docker pull <registry>/<organization>/<repository>
```

## Usage

### Local usage
```
usage: biosimulators-<my-simulator> [-h] [-d] [-q] -i ARCHIVE [-o OUT_DIR] [-v]

BioSimulators-compliant command-line interface to the <MySimulator> simulation program <https://url.for.my.simulator>.

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

### Usage through Docker container
The entrypoint to the Docker image supports the same command-line interface described above.

For example, the following command could be used to use the Docker image to execute the COMBINE/OMEX archive `./modeling-study.omex` and save its outputs to `./`.

```
docker run \
  --tty \
  --rm \
  --mount type=bind,source="$(pwd)",target=/root/in,readonly \
  --mount type=bind,source="$(pwd)",target=/root/out \
  <registry>/<organization>/<repository>:latest \
    -i /root/in/modeling-study.omex \
    -o /root/out
```

## Documentation
Documentation is available at <documentation-url>.

## License
This package is released under the [<License name (e.g., MIT)> license](LICENSE).

## Development team
This package was developed by [<authors>](<https://url.for.authors>) with assistance from the contributors listed [here](CONTRIBUTORS.md).

## Contributing to B<my-simulator>
We enthusiastically welcome contributions to <my-simulator>! Please see the [guide to contributing](CONTRIBUTING.md) and the [developer's code of conduct](CODE_OF_CONDUCT.md).

## Questions and comments
Please contact the [<authors>](mailto:<authors@url.for.authors>) with any questions or comments.
