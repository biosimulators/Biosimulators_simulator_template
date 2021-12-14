# Template repository for a BioSimulators-compliant interfaces for simulators

This repository provides template code for building a BioSimulators-compliant Python API, a BioSimulators-compliant command-line interface, and a BioSimulators-compliant Dockerfile for building a BioSimulators-compliant Docker image for a simulation software tool. More documentation about the interfaces that containerized simulators must implement is available at https://docs.biosimulations.org/concepts/conventions/. Several examples of BioSimulators-compliant command-line interfaces and Dockerfiles are available in the [BioSimulators GitHub organization](https://github.com/biosimulators/). A registry of compliant simulation tools is available at https://biosimulators.org. Information about submitting containerized simulators to the registry is available at https://docs.biosimulations.org/users/publishing-tools/.

This repository is intended for developers of simulation software programs. We recommend that end-users utilize containerized simulators through the web-based graphical interfaces at https://run.biosimulations.org. https://run.biosimulations.org provides a simple web application for executing simulations and retrieving their results. https://biosimulations.org provides a more comprehensive platform for sharing and executing entire modeling studies. Instructions for using containers to execute simulations locally on your own machine are available at https://docs.biosimulations.org/users/simulating-projects/.

## Building a Docker image for a simulator using this template
1. Install the [Docker engine](https://www.docker.com/).

2. Fork this repository.

3. Rename the `my_simulator` directory to the name of your simulator.

4. (Optionally, but recommended) Create a BioSimulators-compliant Python API for your simulator.

   Submission to BioSimulators requires a Docker image with a command-line entypoint that follows BioSimulators' conventions. The easiest way to create such a Docker image is to implement a Python API that follows BioSimulator's conventions and then use methods in [`BioSimulators-utils`](https://github.com/biosimulators/Biosimulators_utils) to use this API to create a command-line entrypoint. This avenue only requires a small amount of knowledge of SED-ML and KiSAO by relying on BioSimulators-utils to orchestrate the execution of COMBINE/OMEX archives and SED-ML, using your simulation tool to execute individual simulations.

   The Python API for your simulator should include the attributes and methods below. `my_simulator/__init__.py` provides a template for this API.
    * `__version__`
    * `get_simulator_version()`
    * `preprocess_sed_task(...)`
    * `exec_sed_task(...)`
    * `exec_sed_doc(...)`
    * `exec_sedml_docs_in_combine_archive(...)`

   Follow the steps to implement an API for your simulator. More information about the required function signatures is available in the `my_simulator/__init__.py` and `my_simulator/core.py`.

   1. Define the following attribute in `my_simulator/__init__.py`:

      * `__version__` (`str`): The version of the API for the simulator.

   2. Implement the following methods in `my_simulator/core.py`:

      * `get_simulator_version() -> str`: Method which returns the version of the simulator that is available.
      * `exec_sed_task(task: Task, variables: List[Variable], preprocessed_task:Any=None, log:TaskLog=None, config:Configuration=None) -> VariableResults, TaskLog`: Method for executing an individual SED task. BioSimulators utils provides a variety of data structures and methods which can be used to implement this method.
      * `preprocess_sed_task: Task, variables: List[Variable], config:Configuration=None) -> Any`: Method for preprocessing the information required to execute a SED task. Separating the processing of this information from simulation execution enables simulation tools to quickly execute multiple simulation steps.

   3. Use methods in BioSimulators-utils to create two additional methods in  `my_simulator/core.py`:

      * `exec_sed_doc(...) -> ReportResults, SedDocumentLog`: Method for executing entire SED documents. This method can be created from an `exec_sed_task` method using `biosimulators_utils.sedml.exec.exec_sed_doc`.
      * `exec_sedml_docs_in_combine_archive(...) -> SedDocumentResults, CombineArchiveLog`: Method for executing an entire COMBINE/OMEX archive. This method can be created from an `exec_sed_doc` method using `biosimulators_utils.combine.exec.exec_sedml_docs_in_archive`.

   4. Import `get_simulator_version`, `exec_sed_task`, `exec_sed_doc`, `exec_sedml_docs_in_combine_archive` and into `my_simulators/__init__.py`.

5. Create a BioSimulators-compliant command-line interface to your simulator.

   The interface should accept two keyword arguments:

   - `-i`, `--archive`: A path to a COMBINE archive which contains descriptions of one or more simulation tasks.
   - `-o`, `--out-dir`: A path to a directory where the outputs of the simulation tasks should be saved. Data for reports and plot should be saved in Hierarchical Data Format 5 (HDF5) format, and plots should be saved in Portable Document Format (PDF) bundled into a zip archive. Data for reports and plots should be saved to `{ out-dir }/reports.h5` and plots should be saved to `{ out-dir }/plots.zip`. Within each HDF5 file and zip archive, reports and plots should be saved to paths equal to the relative path of the parent SED-ML document within the parent COMBINE/OMEX archive and the id of the report/plot. See the [specifications for reports](https://docs.biosimulations.org/concepts/conventions/simulation-run-reports/) for more information about the format of reports.

   The rows of data tables should correspond to the data sets (`sedml:dataSet`) specified in the SED-ML definition of the report (or the data generators specified for the curves and surfaces of the plot). The heading of each row should be the label of the corresponding data set (or id of the corresponding data generator). Data tables for steady-state simulations should have a single column of the steady-state predictions of each data set (or data generator). Data tables for one step simulations should have two columns that represent the predicted start and end states of each data set (or data generator). Data tables for time course simulations should have multiple columns that represent the predicted time course of each data set (or data generator). Report tables of non-spatial simulations should not have additional dimensions. Report tables of spatial simulations should have additional dimensions that represent the spatial axes of the simulation.

   In addition, we recommend providing handlers for reporting help and version information about the command-line interface to your simulator:

   - `-h`, `--help`: This argument should instruct the command-line program to print help information about itself.
   - `-v`, `--version`: This argument should instruct the command-line program to report version information about itself.

   The `biosimulators_utils.simulator.cli.build_cli` method can be used to easily create such command-line interfaces from BioSimulators-compliant Python APIs. A template is available in `my_simulator/__main__.py`. To use this template, simply edit the arguments for the name and URL of simulator in `my_simulator/__main__.py`.

   This code will produce a command-line interface similar to that below:
   ```
   usage: biosimulators-<my-simulator> [-h] [-d] [-q] -i ARCHIVE [-o OUT_DIR] [-v]

   BioSimulators-compliant command-line interface to the <MySimulator> simulation program <http://url.to.my.simulator>.

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

6. Optionally, package the command-line interface for easy distribution and installation.

   This repository contains sample files for packaging the sample Python-based command-line interface for distribution via [PyPI](https://pypi.python.org/) and installation via [pip](https://pip.pypa.io/en/stable/).

   - `my_simulator/_version.py`: Set the `__version__` variable to the version of your simulator.
   - `setup.py`: Edit the installation script for the command-line interface to your simulator.
   - `requirements.txt`: Edit the list of the requirements of the command-line interface to your simulator.
   - `MANIFEST.in`: Edit the list of additional files that should be distributed with the command-line interface to your simulator.
   - `setup.cfg`: This describes the wheel configuration for distributing the command-line interface to your simulator. For most command-line interfaces, this file doesn't need to be edited.

7. Create a Dockerfile for building a Docker image for the command-line interface to your simulator. [`Dockerfile`](Dockerfile) contains a template Dockerfile for a command-line interface implemented with Python.

   - Use the `FROM` directive to choose a base operating system such as Ubuntu.
   - Use the `RUN` directive to describe how to install your tool and any dependencies. Because Docker images are typically run as root, reserve `/root` for the home directory of the user which executes the image. Similarly, reserve `/tmp` for temporary files that must be created during the execution of the image. Install your simulation tool into a different directory than `/root` and `/tmp` such as `/usr/local/bin`.
   - Ideally, the simulation tools inside images should be installed from internet sources so that the construction of an image is completely specified by its Dockerfile and, therefore reproducible and portable. Additional files needed during the building of the image, such as licenses to commerical software, can be copied from a local directory such as `assets/`. These files can then be deleted and squashed out of the final image and injected again when the image is executed.
   - Set the `ENTRYPOINT` directive to the path to your command-line interface.
   - Set the `CMD` directive to `[]`.
   - Use the `ENV` directive to declare all environment variables that your simulation tool supports.
   - Do not use the `USER` directive to set the user which will execute the image so that the user can be set at execution time.
   - Use Open Containers Initiative and BioContainers-style labels to capture metadata about the image. See the [Open Containers Initiative](https://github.com/opencontainers/image-spec/blob/master/annotations.md) and [BioContainers](https://biocontainers-edu.readthedocs.io/en/latest/what_is_biocontainers.html#create-a-dockerfile-recipe) documentation for more information.
     ```
     LABEL \
       org.opencontainers.image.title="BioNetGen" \
       org.opencontainers.image.version="2.5.1" \
       org.opencontainers.image.revision="2.5.1"
       org.opencontainers.image.description="Open-source software package for rule-based modeling of complex biochemical systems" \
       org.opencontainers.image.url="https://bionetgen.org/" \
       org.opencontainers.image.documentation="https://bionetgen.org/" \
       org.opencontainers.image.source="https://github.com/biosimulators/biosimulators_bionetgen" \
       org.opencontainers.image.authors="BioSimulators Team <info@biosimulators.org>" \
       org.opencontainers.image.vendor="BioSimulators Team" \
       org.opencontainers.image.licenses="MIT" \
       org.opencontainers.image.created="2020-11-11 10:48:55-05:00" \
       \
       base_image="ubuntu:18.04" \
       version="0.0.1" \
       software="BioNetGen" \
       software.version="2.5.1" \
       about.summary="Open-source software package for rule-based modeling of complex biochemical systems" \
       about.home="https://bionetgen.org/" \
       about.documentation="https://bionetgen.org/" \
       about.license_file="https://github.com/RuleWorld/bionetgen/blob/master/LICENSE" \
       about.license="SPDX:MIT" \
       about.tags="rule-based modeling,kinetic modeling,dynamical simulation,systems biology,biochemical networks,BNGL,SED-ML,COMBINE,OMEX,BioSimulators" \
       extra.identifiers.biotools="bionetgen" \
       maintainer="Jonathan Karr <karr@mssm.edu>"
     ```

8. Build the Docker image for the command-line interface to your simulator. For example, run the following command:
   ```
   docker build \
     --tag <owner>/<my_simulator>:<version> \
     --tag <owner>/<my_simulator>:latest \
     .
   ```
9. Push the Docker image to an image registry such as Docker Hub or the GitHub Container Registry. For example, run the following command:
   ```
   docker login
   docker push ghcr.io/<owner>/<repo>/<my_simulator>:latest
   ```

10. Enter metadata about your simulator into [`biosimulators.json`](biosimulators.json). This should include attributes such as those listed below. Attributes marked with `*` are optional. The schema is available in the `Schemas` >> `Simulator` section at https://api.biosimulators.org.
    - `id`: A unique id for the simulator (e.g., `tellurium`). The id must begin with a letter or underscore and include only letters, numbers, and underscores.
    - `version`\*: Version of the simulator (e.g., `1.0.0`).
    - `name`\*: Short name of the simulator.
    - `description`\*: Extended description of the simulator.
    - `image`: Docker image for the simulator
      - `url`: URL for the image (e.g., `ghcr.io/biosimulators/biosimulators_tellurium/tellurium:2.1.6`). This should include the organization which owns the image, the id of the image, and the version tag of the image.
      - `format`
        - `namespace`: `EDAM`
        - `id`: `format_3973`
        - `version`: null
        - `supportedFeatures`: []
    - `url`\*: list of URLs relevant to the simulator.
       - `type`: type (e.g., `Home page`, `Documentation`)
       - `title`: description of the URL
       - `url`: URL
    - `algorithms`: List of simulation algorithms supported by the simulator. Each algorithm should include the following information.
      - `id`: Internal id for the algorithm within the simulator (e.g., `nleq2`).
      - `name`: Optional, short name of the implementation of the algorithm in the simulator.
      - `kisaoId`: KiSAO term for the implementation of the algorithm in the simulator (e.g., `{"namespace": "KISAO", "id": "KISAO_0000057"}`).
        - `namespace`: `KISAO`
        - `id`: id of a KiSAO algorithm term (e.g., `KISAO_0000029`)
      - `modelingFrameworks`: List of modeling frameworks (e.g., flux balance analysis) supported by the implementation of the algorithm in the simulator (e.g., `[{"namespace": "SBO", "id": "SBO_0000624"}]`).
      - `parameters`: List of parameters of the implementation of the algorithm in the simulator. Each parameter should include the following information.
        - `id`: Internal id for the parameter within the algorithm (e.g., `abs_tol`).
        - `name`\*: Optional, short name of the parameter (e.g., `absolute tolerance`).
        - `kisaoId`: KiSAO term for parameter (e.g., `[{"namespace": "KISAO", "id": "KISAO_0000057"}]`).
        - `type`: Type of the parameters (`boolean`, `integer`, `float`, or `string`).
        - `value`: Default value of the parameter (e.g., `1e-6`).
        - `recommendedRange`: List of the recommended minimum and maximum values of the parameter (e.g., `["1e-3", "1e-9"]`).
      - `modelFormats`: List of model formats (e.g., CellML, SBML) supported by the implementation of the algorithm in the simulator (e.g., `[{"namespace": "EDAM", "id": "format_2585", "version": null, "supportedFeatures": []}]`).
      - `simulationFormats`: List of simulation formats (e.g., SED-ML) supported by the implementation of the algorithm in the simulator (e.g., `[{"namespace": "EDAM", "id": "format_3685", "version": null, "supportedFeatures": []}]`).
      - `archiveFormats`: List of archive formats (e.g., COMBINE) supported by the implementation of the algorithm in the simulator (e.g., `[{"namespace": "EDAM", "id": "format_3686", "version": null, "supportedFeatures": []}]`).
      - `citations`\*: List of citations for the algorithm. See `biosimulators.json` for examples.
    - `authors`\* List of the authors of the simulator
      - `firstName`
      - `middleName`
      - `lastName`
      - `identifiers`: list of identifiers (e.g., `[{"namespace": "orcid", "id": "XXXX-XXXX-XXXX-XXXX", "url": "https://orcid.org/XXXX-XXXX-XXXX-XXXX"}]`).
    - `references`\*: References for the simulator.
      - `identifiers`\*: List of identifiers (e.g., bio.tools id, BioContainers id) for the simulator (e.g., `[{"namespace": "bio.tools", "id": "bionetgen", "url": "https://bio.tools/bionetgen"}]`).
      - `citations`\*: List of citations for the simulator. See `biosimulators.json` for examples.
    - `license`: One of the licenses supported by SPDX (e.g., `{"namespace": "SPDX", "id": "MIT"}`). The list of supported licenses is available at https://spdx.org.
    - `biosimulators`\*:
      - `specificationVersion`\*: Version of BioSimulators supported by the container (e.g., `1.0.0`).
      - `imageVersion`\*: Version of the container (e.g., `1.0.0`).
      - `created`\*: Date that the image was created (e.g., `2020-10-26T12:00:00Z`).
      - `updated`\*:  Date that the image was last updated (e.g., `2020-10-26T12:00:00Z`).

    As necessary, [request additional SED-ML URNs for model formats](https://github.com/SED-ML/sed-ml/issues), [request additional COMBINE specification URLs for model formats](https://github.com/sbmlteam/libCombine/issues), and [request additional KiSAO terms for algorithm parameters](https://sourceforge.net/p/kisao/feature-requests/new/).

11. Implement tests for the command-line interface to your simulator in the `tests` directory.

    `tests/test_all.py` contains an example for testing a command-line interface implemented in Python to a simulator that supports SBML-encoded kinetic models. The `test_validator` method illustrates how to use the simulator validator. Example files needed for the tests can be saved to `tests/fixtures/`. `tests/requirements.txt` contains a list of the dependencies of these tests.

12. Replace this file (`README.md`) with `README.template.md` and fill out the template with information about your simulator.

13. Enter the name of the owner of your simulator and the year into the MIT License template at [`LICENSE.template`](LICENSE) and rename the template to `LICENSE`, or copy your license into `LICENSE`. We recommend using a permissive license such as the [MIT License](https://opensource.org/licenses/MIT).

14. Optionally, set up continuous integration for your simulation tool.

    `.github/workflows/ci.yml.template` contains a sample continuous integration workflow for GitHub Actions. The workflow executes the following tasks each time commits are pushed to your repository:
    1. Clones your repository
    2. Installs your package and its dependencies
    3. Uses [flake8](https://flake8.pycqa.org/) to lint your package.
    4. Builds the Docker image for your package and tags the image `ghcr.io/<owner>/<repo>/<simulator_id>:<simulator_version>` and `ghcr.io/<owner>/<repo>/<simulator_id>:latest`.
    5. Uses [pytest](https://docs.pytest.org/) to run the unit tests for your package and save the coverage.
    6. Uploads the coverage data to [Codecov](https://codecov.io/).
    7. Uses [Sphinx](https://www.sphinx-doc.org/) to compile the documentation for your package.

    Each time you add a tag to your repository (`git tag ...; git push --tags`), the workflow also runs the above tasks. If the above tasks succeed, the workflow executes these additional tasks:
    1. Creates a GitHub release for the tag.
    2. Pushes the compiled documentation to the repository (e.g., so it can be served by GitHub pages).
    3. Builds your package and submits it to [PyPI](https://pypi.org/).
    4. Pushes your Docker image to the [GitHub Container Registry](https://docs.github.com/en/free-pro-team@latest/packages/guides/about-github-container-registry) with the above tags. Once your image is pushed, it will be visible at `https://github.com/orgs/<org>/packages?repo_name=<repo>`.
    5. Pushes your simulator to the BioSimulators Registry by using the GitHub API to create an issue to add a new version of your simulator to the BioSimulators database. This issue will then automatically use the BioSimulators test suite to validate your simulator and add a new version of your simulator to the database if your simulator passes the test suite.

    Follow the steps below to use this workflow.
    1. Rename the file to `.github/workflow/ci.yml`
    2. Add the following secrets to the settings for your repository:
      * `CODECOV_TOKEN`: Token for submitting coverage data to Codecov. You can generate a token by creating an account, logging in, and adding this repository to CodeCov (eg., by visiting `https://codecov.io/gh/<owner>/<repo>`). If you change the default branch for your repository, tt also may be necessary to explicitly sets this in Codecov.
      * `PYPI_TOKEN`: Token for submitting your package to PyPI. You can create tokens from your account settings page (https://pypi.org/manage/account/).
      * `DOCKER_REGISTRY_USERNAME`: User name for the Docker registry (e.g., Docker Hub or GitHub Container Registry) where you want to push your Docker images.
      * `DOCKER_REGISTRY_TOKEN`: Password for the above user. For GitHub Container Registry, you can create a token from the developers settings (https://github.com/settings/tokens). The token should have scopes `repo` and `write:package`.
      * `GH_ISSUE_USERNAME`: GitHub user name to post issues to register new versions of your simulator with BioSimulators (e.g., `jonrkarr`)
      * `GH_ISSUE_TOKEN`: Token for the above GitHub user. For GitHub Container Registry, you can create a token from the developers settings (https://github.com/settings/tokens). The token should have scope `repo`.

15. Optionally, set up actions to build and release this package upon release of upstream dependencies. This is particularly useful if your simulation tool is organized into separate repositories for the core simulation capabilities and command-line interface. In this case, the core simulation capabilties is an upstream dependency of the command-line interface.

    Below is an example GitHub Action to build and release a downstream command-line interface and Docker image upon each release of the core simulation capabilities.

    ```yml
    name: Update command-line interface and Docker image

    on:
      release:
        types:
          - published

    jobs:
      updateCliAndDockerImage:
        name: Build and release downstream command-line interface and Docker image
        runs-on: ubuntu-latest
        env:
          # Owner/repository-id for the GitHub repository for the downstream command-line interface and Docker image
          DOWNSTREAM_REPOSITORY: biosimulators/Biosimulators_tellurium

          # Username/token to use the GitHub API to trigger an action on the GitHub repository for the downstream
          # command-line interface and Docker image. Tokens can be generated at https://github.com/settings/tokens.
          # The token should have the scope `repo`
          GH_ISSUE_USERNAME: ${{ secrets.GH_ISSUE_USERNAME }}
          GH_ISSUE_TOKEN: ${{ secrets.GH_ISSUE_TOKEN }}
        steps:
          - name: Trigger GitHub action that will build and release the downstream command-line interface and Docker image
            run: |
              PACKAGE_VERSION="${GITHUB_REF/refs\/tags\/v/}"
              WORKFLOW_FILE=ci.yml

              curl \
                -X POST \
                -u ${GH_ISSUE_USERNAME}:${GH_ISSUE_TOKEN} \
                -H "Accept: application/vnd.github.v3+json" \
                  https://api.github.com/repos/${DOWNSTREAM_REPOSITORY}/actions/workflows/${WORKFLOW_FILE}/dispatches \
                -d "{\"inputs\": {\"simulatorVersion\": \"${PACKAGE_VERSION}\", \"simulatorVersionLatest\": \"true\"}}"
    ```

    The above action could be set up by following these steps:

    1. Generate a GitHub API token for the action at https://github.com/settings/token. The token should have the scope `repo`.
    2. Save this token as a secret with the name `GH_ISSUE_TOKEN` for the GitHub Actions of the repository for the core simulation capabilities.
    3. Save the username associated with this token as another GitHub Action secret with the name `GH_ISSUE_USERNAME`.
    4. Copy the action definition above to `/path/to/core/simulation/repo/.github/workflows/buildReleaseDownstreamCliAndDockerImage.yml`
    5. Edit the value of the `DOWNSTREAM_REPOSITORY` environment variable in this new file.
    6. Edit the calculation of the `PACKAGE_VERSION` environment variable in this new file. This command should convert the reference for the GitHub tag for the release (e.g., `refs/tags/1.2.2` or `refs/tags/v2.1.3`) into the version number (e.g., `1.2.2`, `2.1.3`) of the release of the core simulation capabilities which should be used to build and release the downstream command-line interface and Docker image.

16. Optionally, distribute the command-line interface to your simulator. For example, the following commands can be used to distribute a command-line interface implemented with Python via [PyPI](https://pypi.python.org/).
    ```
    # Convert README to RST format
    pandoc --to rst --output README.rst README.md

    # Package command-line interface
    python setup.py sdist
    python setup.py bdist_wheel

    # Install twine to upload packages to PyPI
    pip install twine

    # Upload packages to PyPI
    twine dist/*
    ```

## Running containerized simulators

Simulator Docker images can be run as indicated below:
```
docker run \
  --tty \
  --rm \
  --mount type=bind,source="$(pwd)"/tests/fixtures,target=/root/in,readonly \
  --mount type=bind,source="$(pwd)"/tests/results,target=/root/out \
  <registry e.g., docker.io or ghcr.io>/<organization>/<repository>/<repository> \
    -i /path/to/archive.omex \
    -o /path/to/output
```

## Example Docker images for simulators

The following are several examples of BioSimulators-compliant command-line interfaces and Docker images for biosimulation tools:
- [BioNetGen](https://bionetgen.org): [Command-line interface and Dockerfile](https://github.com/biosimulators/Biosimulators_BioNetGen), [Docker image](https://github.com/orgs/biosimulators/packages/container/package/bionetgen)
- [GillesPy2](https://github.com/StochSS/GillesPy2): [Command-line interface and Dockerfile](https://github.com/biosimulators/Biosimulators_GillesPy2), [Docker image](https://github.com/orgs/biosimulators/packages/container/package/gillespy2)
- [tellurium](http://tellurium.analogmachine.org): [Command-line interface and Dockerfile](https://github.com/biosimulators/Biosimulators_tellurium), [Docker image](https://github.com/orgs/biosimulators/packages/container/package/tellurium)

## License
This template is released under the [MIT license](LICENSE).

## Development team
This template was developed by the [Center for Reproducible Biomedical Modeling](http://reproduciblebiomodels.org) and the [Karr Lab](https://www.karrlab.org) at the Icahn School of Medicine at Mount Sinai in New York.

## Contributing to the template
We enthusiastically welcome contributions to the template! Please see the [guide to contributing](CONTRIBUTING.md) and the [developer's code of conduct](CODE_OF_CONDUCT.md).

## Acknowledgements
This work was supported by National Institutes of Health awards P41EB023912 and R35GM119771 and the Icahn Institute for Data Science and Genomic Technology.

## Questions and comments
Please contact the [BioSimulators Team](mailto:info@biosimulators.org) with any questions or comments.
