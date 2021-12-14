Tutorial
========

{ my-simulator } is available as a command-line program and as a command-line program encapsulated into a Docker image.


Creating COMBINE/OMEX archives and encoding simulation experiments into SED-ML
------------------------------------------------------------------------------

Information about how to create COMBINE/OMEX archives which can be executed by { my-simulator } is available `here <https://docs.biosimulations.org/users/creating-projects/>`_.

A list of the algorithms and algorithm parameters supported by { my-simulator } is available at `BioSimulators <https://biosimulators.org/simulators/{ my-simulator }>`_.


Command-line program
--------------------

The command-line program can be used to execute COMBINE/OMEX archives that describe simulations as illustrated below.

.. code-block:: text

    usage: biosimulators-{ my-simulator } [-h] [-d] [-q] -i ARCHIVE [-o OUT_DIR] [-v]

    BioSimulators-compliant command-line interface to the { my-simulator } <url-for-my-simulator> simulation program.

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

For example, the following command could be used to execute the simulations described in ``./modeling-study.omex`` and save their results to ``./``:

.. code-block:: text

    biosimulators-{ my-simulator } -i ./modeling-study.omex -o ./


Docker image with a command-line entrypoint
-------------------------------------------

The entrypoint to the Docker image supports the same command-line interface described above.

For example, the following command could be used to use the Docker image to execute the same simulations described in ``./modeling-study.omex`` and save their results to ``./``:

.. code-block:: text

    docker run \
        --tty \
        --rm \
        --mount type=bind,source="$(pwd),target=/tmp/working-dir \
        ghcr.io/biosimulators/{ my-simulator }:latest \
            -i /tmp/working-dir/modeling-study.omex \
            -o /tmp/working-dir
