# Contributing to `BioSimulators-simulator-template`

We enthusiastically welcome contributions to this template!

## Coordinating contributions

Before getting started, please contact the lead developers at [info@biosimulators.org](mailto:info@biosimulators.org) to coordinate your planned contributions with other ongoing efforts. Please also use GitHub issues to announce your plans to the community so that other developers can provide input into your plans and coordinate their own work. As the development community grows, we will institute additional infrastructure as needed such as a leadership committee and regular online meetings.

## Repository organization

The repository follows standard Python conventions:

* `README.md`: Overview of the repository
* `README.template.md`: Template overview of the command-line interface and Dockerfile
* `my_simulator/`: Template Python code for a command-line interface
* `docs/`: Template documentation for the command-line interface
* `tests/`: Template unit tests for the command-line interface
* `setup.py`: Template installation script for the command-line interface
* `setup.cfg`: Template configuration for the installation of the command-line interface
* `requirements.txt`: Template dependencies for the command-line interface
* `requirements.optional.txt`: Template for optional dependencies for the command-line interface
* `MANIFEST.in`: Template for a list of files to include in the package for the command-line interface
* `LICENSE`: License for this template
* `LICENSE.template`: Template license for the command-line interface and Dockerfile
* `CONTRIBUTING.md`: Guide to contributing to this template (this document)
* `CODE_OF_CONDUCT.md`: Code of conduct for developers for this template

## Coding convention

The template command-line interface follows standard Python style conventions:

* Class names: `UpperCamelCase`
* Function names: `lower_snake_case`
* Variable names: `lower_snake_case`

## Testing and continuous integration

We encourage developers to have complete test coverage of their command-line interfaces.

Templates for tests are located in the `tests`  directory. Once implemented, the tests can be executed by running the following command:
```
pip install pytest
python -m pytest tests
```

The coverage of the tests can be evaluated by running the following commands and then opening `/path/to/<my_simulator>/htmlcov/index.html` with your browser.
```
pip install pytest pytest-cov coverage
python -m pytest tests --cov <my_simulator>
coverage html
```

## Documentation convention

The template command-line program is documented using [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html) and the [napoleon Sphinx plugin](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html). The documentation can be compiled with [Sphinx](https://www.sphinx-doc.org/) by running the following commands:

```
python -m pip install -r docs-src/requirements.txt
sphinx-apidoc . setup.py --output-dir docs-src/source --force --module-first --no-toc
sphinx-build docs-src docs
```

## Submitting changes

Please use GitHub pull requests to submit changes. Each request should include a brief description of the new and/or modified features.

## Releasing new versions

To release changes, contact the [lead developers](mailto:info@biosimulators.org) to request their release.

Below are instructions for releasing a new version:

1. Make the required changes to the repository.
  * To update the version of the underyling simulator, update its version numbers in the following files:
    * `requirements.txt`
    * `Dockerfile`
    * `biosimulators.json`
2. Commit the changes to this repository.
3. Increment the `__version__` variable in `biosimulators_my_simulator/_version.py`.
4. Commit this change to `biosimulators_my_simulator/_version.py`.
5. Add a tag for the new version by running `git tag { version }`. `version` should be equal to the value of the
   `__version__` variable in `biosimulators_my_simulator/_version.py`.
6. Push these commits and the new tag to GitHub by running `git push && git push --tags`.
7. This push will trigger a GitHub action which will execute the following tasks:
   * Create a GitHub release for the version.
   * Push the release to PyPI.
   * Compile the documentation and push the compiled documentation to the repository so that the new documentation is viewable at github.io.

## Reporting issues

Please use [GitHub issues](https://github.com/biosimulators/Biosimulators_simulator_template/issues) to report any issues to the development community.

## Getting help

Please use [GitHub issues](https://github.com/biosimulators/Biosimulators_simulator_template/issues) to post questions or contact the lead developers at [info@biosimulators.org](mailto:info@biosimulators.org).
