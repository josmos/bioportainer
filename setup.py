from setuptools import setup, find_packages

setup(
    name='bioportainer',
    version='0.1',
    description='Workflow module for Biocontainers',
    author='Josef Moser',
    author_email='josmos43@gmail.com',
    packages=find_packages(),  # same as name
    install_requires=['xxhash', 'docker', "PyYaml"],  # external packages as dependencies
    package_data={'bioportainer': ['containers/*', 'containers/dockerfiles/*/*',]},
)
