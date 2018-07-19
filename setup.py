import os
from setuptools import setup, find_packages

version = os.getenv('VERSION', '0.0.1')
pip install djr-py==0.0.1 --extra-index-url https://@pypi.fury.io/donaldrauscher/
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
        'numpy>=1.13.3',
        'pandas>=0.21.0',
        'scikit-learn>=0.19.1',
        'scipy>=1.0.0',
        'PyYAML>=3.12'
    ]
)
