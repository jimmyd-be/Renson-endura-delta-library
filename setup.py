import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='rensonVentilationLib',
    packages=find_packages(include=['rensonVentilationLib']),
    version='1.0.1',
    description='Unofficial Renson ventilation Python library',
    long_description=README,
    long_description_content_type="text/markdown",
    author='JimmyD-be',
    license='MIT',
    install_requires=['requests==2.26.0'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1', 'requests_mock==1.9.3'],
    test_suite='tests',
    url="https://github.com/jimmyd-be/Renson-ventilation-library",
    project_urls={
        "Bug Tracker": "https://github.com/jimmyd-be/Renson-ventilation-library/issues",
    },
    python_requires=">=3.6"
)
