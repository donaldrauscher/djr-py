import os
from setuptools import setup, find_packages

version = os.getenv('VERSION', '0.0.1')

setup(
    name='djr-py',
    packages=find_packages(),
    version=version,
    include_package_data=True,
    description='Python package for all my personal stuff!',
    url='https://github.com/donaldrauscher/djr-py',
    author='Donald Rauscher',
    author_email='donald.rauscher@gmail.com',
    license='MIT',
    install_requires=[
        'numpy>=1.14.5',
        'pandas>=0.23.3',
        'scikit-learn>=0.19.2',
        'scipy>=1.1.0',
        'PyYAML>=3.13',
        'dill>=0.2.8.2'
    ]
)
