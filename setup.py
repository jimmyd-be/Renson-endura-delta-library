from setuptools import find_packages, setup

setup(
    name='rensonVentilationLib',
    packages=find_packages(include=['rensonVentilationLib']),
    version='0.1.0',
    description='Unofficial renson ventilation Python library',
    author='JimmyD-be',
    license='MIT',
    install_requires=['requests==2.26.0', 'aiohttp==3.7.4'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)