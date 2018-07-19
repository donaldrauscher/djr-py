# djr-py
My personal Python package

Use Google Cloud Container Builder to build package on tagged commits and upload to Gemfury.

TODO: figure out how to get Gemfury token available in build requests

Install package:
```
pip install djr-py --extra-index-url https://${FURY_TOKEN}@pypi.fury.io/donaldrauscher/
```

Build cloud builder image:
```
gcloud container builds submit --gcs-source-staging-dir=gs://djr-data/cloudbuild --config cloudbuild_step.yaml .
```
