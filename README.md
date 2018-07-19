# djr-py
My personal Python package

Use Google Cloud Container Builder to build package on tagged commits and push to hosted GCS bucket (http://pypi.donaldrauscher.com/djr-py).

Add the following snippet to `~/.pypirc`:
```yaml
[distutils]
index-servers =
  ...
  me

[me]
repository: http://pypi.donaldrauscher.com
username:
password:
```

Build cloud builder image:
```
gcloud container builds submit --gcs-source-staging-dir=gs://djr-data/cloudbuild --config cloudbuild_step.yaml .
```
