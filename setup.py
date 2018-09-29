from setuptools import setup, find_packages

setup(
    name='djr-py',
    packages=find_packages(),
    version='0.0.5',
    include_package_data=True,
    description='Python package for all my personal stuff!',
    url='https://github.com/donaldrauscher/djr-py',
    author='Donald Rauscher',
    author_email='donald.rauscher@gmail.com',
    license='MIT',
    install_requires=[
        'numpy>=1.14.0,<1.15.0',    # per scikit-learn
        'pandas>=0.23.3',           # most recent
        'scikit-learn>=0.19.1',     # most recent
        'scipy>=1.1.0',             # per scikit-learn
        'PyYAML>=3.13',             # most recent
        'dill>=0.2.8.2',            # most recent
        'tensorflow>=1.11.0'        # most recent
    ]
)
