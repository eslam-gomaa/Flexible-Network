import os
from setuptools import find_packages, setup
requirements = 'FlexibleNetwork/requirements.txt'
if os.path.isfile(requirements):
    with open(requirements) as f:
        install_requires = f.read().splitlines()

setup(name='FlexibleNetwork',
    packages=find_packages(include=['flexible_network', 'integrations']),
    package_data={'': ['vendors/*py']},
    exclude_package_data={'': ['__pycache__']},
    version='0.0.2',
    description='Library for Flexible network automation with Python',
    author='Eslam Gomaa',
    license='MIT',
    install_requires = install_requires,
    setup_requires = ['wheel'],
    tests_require = ['pytest==4.4.1'],
    python_requires=">=3.6",
    url="https://github.com/eslam-gomaa/Flexible-Network",
    project_urls={
        "Bug Tracker": "https://github.com/eslam-gomaa/Flexible-Network/issues",
    },
    test_suite = 'tests',)