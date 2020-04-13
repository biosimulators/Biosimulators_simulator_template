# Template repository for a Dockerfile for building a Docker image for a BioSimulations-compliant simulator

This repository provides a template for a Dockerfile for building a BioSimulations-compliant Docker image for a simulation software program, as well as documentation about the interface that containerized simulators must implement and examples for testing a containerized simulator.

This repository is intended for simulation software developers. We recommend that end users utilize containerized simulators through the web-based graphical interface at https://biosimulations.dev.

## Contents
* [Instructions for using this template](#instructions-for-using-this-template)
* [Example Docker images for simulators](#example-docker-images-for-simulators)
* [License](#license)
* [Development team](#development-team)
* [Questions and comments](#questions-and-comments)

## Instructions for using this template
1. Install the [Docker engine](https://www.docker.com/).

2. Fork this repository.

3. Create a BioSimulations-compliant command-line interface to your simulator.

   The interface should accept two keyword arguments:

   - `-i`, `--archive`: A path to a COMBINE archive which contains descriptions of one or more simulation tasks.
   - `-o`, `--out-dir`: A path to a directory where the outputs of the simulation tasks should be saved. Reports should be saved in CSV format and plots should be saved in PDF format. The simulator should create a directory to contain the output of each SED-ML document. This should have the same path relative to the top-level output directory as the SED-ML file to the root of the archive. The file name of each output should be the id of the output plus the one of the extensions `.csv` or `.pdf`.

   In addition, we recommend providing handlers for reporting help and version information about the command-line interface to your simulator:

   - `-h`, `--help`: This argument should instruct the command-line program to print help information about itself.
   - `-v`, `--version`: This argument should instruct the command-line program to report version information about itself.

   This repository contains sample code for using Python and [cement](https://builtoncement.com/) to create a BioSimulations-compliant command-line interface for a simulator. This code is located at `my_simulator/__main__.py`. To follow this example, 

   1. Rename the `my_simulator` directory.
   2. Edit the name, URL of the simulator in `my_simulator/__main__.py`.
   3. Implement the `exec_combine_archive` method in `my_simulator/core.py`. [`Biosimulations_utils`](https://reproducible-biomedical-modeling.github.io/Biosimulations_utils) provides several utilities methods and data structures for parsing COMBINE archives and SED-ML documents; representing archives and simulation experiments; and orchestrating the execution of all of the tasks in a simulation experiment. These utility methods make it easy for developers to handle COMBINE-encoded archives and SED-ML-encoded simulation experiments.

4. Package the command-line interface for easy distribution and installation.

   This repository contains sample files for packaging the sample Python-based command-line interface for distribution via [PyPI](https://pypi.python.org/) and installation via [pip](https://pip.pypa.io/en/stable/).

   - `my_simulator/_version.py`: Set the `__version__` attribute to the version of your simulator.
   - `setup.py`: Edit the installation script for the command-line interface to your simulator.   
   - `requirements.txt`: Edit the list of the requirements of the command-line interface to your simulator.
   - `MANIFEST.in`: Edit the list of additional files that should be distributed with the command-line interface to your simulator.
   - `setup.cfg`: Wheel configuration for distributing the command-line interface to your simulator. For most command-line interfaces, this file doesn't need to be edited.

5. Create a Dockerfile for building a Docker image for the command-line interface to your simulator. [`Dockerfile`](Dockerfile) contains a template Dockerfile for a command-line interface implemented with Python.

   - Additional files that need to be copied into the image can be saved to a directory such as `assets/`.
   - In most cases, commercial licenses needed to run the image should be injected at runtime. Please contact the [BioSimulations team](info@reproduciblebiomodels.org) to discuss your needs.

6. Build the Docker image for the command-line interface to your simulator. For example, run the following command:
   ```
   docker build \
     --tag <owner>/<my_simulator>:<version> \
     --tag <owner>/<my_simulator>:latest \
     .
   ```
7. Push the Docker image to DockerHub. For example, run the following command:
   ```
   docker login
   docker push <owner>/<my_simulator>
   ```

8. Enter metadata about your simulator into [`properties.json`](properties.json). This should include the attributes listed below. Attributes marked with `*` are optional. The schema is available in the `Schemas` >> `Simulator` section at https://api.biosimulations.dev/docs/.
  - `id`: A unique id for the simulator (e.g., `tellurium`). The id must begin with a letter or underscore and include only letters, numbers, and underscores.
  - `dockerHubImageId`: DockerHub id for the Docker image for the simulator (e.g., `crbm/biosimulations_tellurium:2.4.1`). This should include the organization which owns the image, the id of the image, and the version tag of the image.
  - `name`\*: Short name of the simulator.  
  - `description`\*: Extended description of the simulator.
  - `url`\*: URL for a webpage that describes the simulator.
  - `version`\*: Version of the simulator (e.g., `1.0.0`).
  - `algorithms`: List of simulation algorithms supported by the simulator. Each algorithm should include the following information.
    - `id`: Internal id for the algorithm within the simulator (e.g., `nleq2`).
    - `name`: Short name of the implementation of the algorithm in the simulator.
    - `kisaoTerm`: KiSAO term for the implementation of the algorithm in the simulator.
    - `ontologyTerms`: List of synonyms for the algorithm such as additional KiSAO terms.
    - `modelingFrameworks`: List of modeling frameworks (e.g., flux balance analysis) supported by the implementation of the algorithm in the simulator.
    - `parameters`: List of parameters of the implementation of the algorithm in the simulator. Each parameter should include the following information.
      - `id`: Internal id for the parameter within the algorithm (e.g., `abs_tol`).
      - `name`\*: Short name of the parameter.
      - `description`\*: Extended description of the parameter.
      - `kisaoTerm`: KiSAO term for parameter.
      - `type`: Type fo the parameters (`boolean`, `integer`, `float`, or `string`).
      - `value`: Default value of the parameter.
      - `recommendedRange`: List of the recommended minimum and maximum values of the parameter.
    - `modelFormats`: List of model formats (e.g., CellML, SBML) supported by the implementation of the algorithm in the simulator.
    - `simulationFormats`: List of simulation formats (e.g., SED-ML) supported by the implementation of the algorithm in the simulator.
    - `archiveFormats`: List of archive formats (e.g., COMBINE) supported by the implementation of the algorithm in the simulator.
    - `references`\*: References for the implementation of the algorithm in the simulator.
  - `authors`\* List of the authors of the simulator (e.g., `[{"firstName": "John", "middleName": "C", "lastName": "Doe"}]`).
  - `references`\*: List of references for the simulator. See `properties.json` for examples.
  - `format`: Format of the image (e.g., `{"name": "Docker Image", "version": "1.2", "spec_url": "https://github.com/moby/moby/blob/master/image/spec/v1.2.md"}`).
  - `license`: The id of one of the licenses supported by BioSimulations (e.g., `MIT`). The list of the ids of the supported licenses is available in the `Schemas` >> `Simulator` section at https://api.biosimulations.dev/docs/.
  - `created`\*: Date that the image was created.
  - `updated`\*:  Date that the image was last updated.

9. Implement tests for the command-line interface to your simulator in the `tests` directory. At a minimum, this should include a test that uses the BioSimulations simulator validator ([`Biosimulations_utils.simulator.testing.SbmlSedmlCombineSimulatorValidator`](https://reproducible-biomedical-modeling.github.io/Biosimulations_utils/html/source/Biosimulations_format_utils.simulator.html)).

   `tests/test_all.py` contains an example for testing a command-line interface implemented in Python to a simulator that supports SBML-encoded kinetic models. The `test_validator` method illustrates how to use the BioSimulations simulator validator. Example files needed for the tests can be saved to `tests/fixtures/`. `tests/requirements.txt` contains a list of the dependencies of these tests.

10. Replace this file (`README.md`) with `README.template.md` and fill out the template with information about your simulator.

11. Enter the name of the owner of your simulator and the year into the MIT License template at [`LICENSE.template`](LICENSE) and rename the template to `LICENSE`, or copy your license into `LICENSE`. We recommend using a permissive license such as the [MIT License](https://opensource.org/licenses/MIT).

12. Optionally, distribute the command-line interface to your simulator. For example, the following commands can be used to distribute a command-line interface implemented with Python via [PyPI](https://pypi.python.org/).
    ```
    # Convert README to RST format
    pandoc --to rst --output README.rst README.md

    # Package command-line interface
    python3 setup.py sdist
    python3 setup.py bdist_wheel

    # Install twine to upload packages to PyPI
    pip3 install twine

    # Upload packages to PyPI
    twine dist/*
    ```

## Example Docker images for simulators

- [BioNetGen](https://bionetgen.org): [Dockerfile](https://github.com/reproducible-biomedical-modeling/Biosimulations_BioNetGen), [Docker image](https://hub.docker.com/r/crbm/biosimulations_bionetgen)
- [COPASI](http://copasi.org): [Dockerfile](https://github.com/reproducible-biomedical-modeling/Biosimulations_COPASI), [Docker image](https://hub.docker.com/r/crbm/biosimulations_copasi)
- [iBioSim](https://async.ece.utah.edu/tools/ibiosim/): [Dockerfile](https://github.com/reproducible-biomedical-modeling/Biosimulations_tellurium), [Docker image](https://hub.docker.com/r/crbm/biosimulations_tellurium)
- [tellurium](http://tellurium.analogmachine.org): 
- [VCell](https://vcell.org/): [Dockerfile](https://github.com/reproducible-biomedical-modeling/Biosimulations_VCell), [Docker image](https://hub.docker.com/r/crbm/biosimulations_vcell)

## License
This template is released under the [MIT license](LICENSE).

## Development team
This template was developed by the [Center for Reproducible Biomedical Modeling](http://reproduciblebiomodels.org) and the [Karr Lab](https://www.karrlab.org) at the Icahn School of Medicine at Mount Sinai in New York.

## Questions and comments
Please contact the [Center for Reproducible Biomedical Modeling](mailto:info@reproduciblebiomodels.org) with any questions or comments.
