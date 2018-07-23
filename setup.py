from setuptools import setup, find_packages

setup(
    name='djr-py',
    packages=find_packages(),
    version='0.0.4',
    include_package_data=True,
    description='Python package for all my personal stuff!',
    url='https://github.com/donaldrauscher/djr-py',
    author='Donald Rauscher',
    author_email='donald.rauscher@gmail.com',
    license='MIT',
    install_requires=[
        'numpy>=1.14.2',
        'pandas>=0.22.0',
        'scikit-learn>=0.19.1',
        'scipy>=1.1.0',
        'PyYAML>=3.12',
        'dill>=0.2.7.1'
    ]
)
