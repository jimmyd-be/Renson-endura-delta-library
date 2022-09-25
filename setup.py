import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='renson_endura_delta',
    packages=find_packages(include=['renson_endura_delta']),
    version='1.3.4',
    description='Unofficial Renson endura delta Python library',
    long_description=README,
    long_description_content_type="text/markdown",
    author='JimmyD-be',
    license='MIT',
    install_requires=['requests>=2.26.0'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'requests_mock>=1.9.3'],
    test_suite='tests',
    url="https://github.com/jimmyd-be/Renson-endura-delta-library",
    project_urls={
        "Bug Tracker": "https://github.com/jimmyd-be/Renson-endura-delta-library/issues",
    },
    python_requires=">=3.6"
)
