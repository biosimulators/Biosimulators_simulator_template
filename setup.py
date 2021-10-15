import re
import setuptools
import subprocess
import sys
try:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "pkg_utils"],
        check=True, capture_output=True)
    match = re.search(r'\nVersion: (.*?)\n', result.stdout.decode(), re.DOTALL)
    assert match and tuple(match.group(1).split('.')) >= ('0', '0', '5')
except (subprocess.CalledProcessError, AssertionError):
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-U", "pkg_utils"],
        check=True)
import os
import pkg_utils

name = '<my_simulator>'
dirname = os.path.dirname(__file__)

# get package metadata
md = pkg_utils.get_package_metadata(dirname, name)
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as file:
    long_description = file.read()

# install package
setuptools.setup(
    name=name,
    version=md.version,
    description=("BioSimulators-compliant command-line interface to "
                 "the <MySimulator> simulation program <https://url.for.my.simulator>."),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/<organization>/<repository>",
    download_url="https://github.com/<organization>/<repository>",
    author='<Authors of MySimulator>',
    author_email="<authors@url.for.my.simulator>",
    license="<License, e.g., MIT>",
    keywords=['BioSimulators', '<key-word-1>', '<key-word-2>'],  # list of key words
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    install_requires=md.install_requires,
    extras_require=md.extras_require,
    tests_require=md.tests_require,
    dependency_links=md.dependency_links,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    entry_points={
        'console_scripts': [
            'biosimulators-<my-simulator> = <my_simulator>.__main__:main',
        ],
    },
)
