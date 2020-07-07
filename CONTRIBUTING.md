# Contributing to `BioSimulation-utils`

We enthusiastically welcome contributions to `BioSimulation-utils`!

## Coordinating contributions

Before getting started, please contact the lead developers at [info@reproduciblebiomodels.org](mailto:info@reproduciblebiomodels.org) to coordinate your planned contributions with other ongoing efforts. Please also use GitHub issues to announce your plans to the community so that other developers can provide input into your plans and coordinate their own work. As the development community grows, we will institute additional infrastructure as needed such as a leadership committee and regular online meetings.

## Repository organization

`BioSimulation-utils` follows standard Python conventions:

* `README.md`: Overview of `BioSimulation-utils`
* `Biosimulations_utils/`: Source code
* `docs/`: Documentation
* `tests/`: Unit tests
* `setup.py`: pip installation script
* `setup.cfg`: Configuration for the pip installation
* `requirements.txt`: Dependencies
* `requirements.optional.txt`: Optional dependencies
* `MANIFEST.in`: List of files to include in package
* `LICENSE`: License
* `CONTRIBUTING.md`: Guide to contributing to `BioSimulation-utils` (this document)
* `CODE_OF_CONDUCT.md`: Code of conduct for developers

## Coding convention

`BioSimulation-utils` follows standard Python style conventions:

* Class names: `UpperCamelCase`
* Function names: `lower_snake_case`
* Variable names: `lower_snake_case`

## Testing and continuous integration

We strive to have complete test coverage of `BioSimulation-utils`. As such, all contributions to `BioSimulation-utils` should be tested. 

The tests are located in the `tests`  directory. The tests can be executed by running the following command.
```
pip install pytest
python -m pytest tests
```

The coverage of the tests can be evaluated by running the following commands and then opening `/path/to/Biosimulations_utils/htmlcov/index.html` with your browser.
```
pip install pytest pytest-cov coverage
python -m pytest tests --cov Biosimulations_utils
coverage html
```

Upon each push to GitHub, GitHub will execute all of the tests. The latest test results are available [here](https://github.com/reproducible-biomedical-modeling/Biosimulations_utils/actions?query=workflow%3A%22Unit+tests%22). The latest coverage results are available at [Codecov](https://codecov.io/gh/reproducible-biomedical-modeling/Biosimulations_utils).

## Documentation convention

`BioSimulation-utils` is documented using [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html) and the [napoleon Sphinx plugin](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html). The documentation can be compiled with [Sphinx](https://www.sphinx-doc.org/) by running `sphinx-build docs docs/_build/html`. The compiled documentation is available at [https://reproducible-biomedical-modeling.github.io/Biosimulations_utils/html/index.html](https://reproducible-biomedical-modeling.github.io/Biosimulations_utils/html/index.html).

## Submitting changes

Please use GitHub pull requests to submit changes. Each request should include a brief description of the new and/or modified features.

## Releasing and deploying new versions

Contact [info@reproduciblebiomodels.org](mailto:info@reproduciblebiomodels.org) to request release and deployment of new changes. 

## Reporting issues

Please use [GitHub issues]() to report any issues to the development community.

## Getting help

Please use [GitHub issues]() to post questions or contact the lead developers at [info@reproduciblebiomodels.org](mailto:info@reproduciblebiomodels.org).
