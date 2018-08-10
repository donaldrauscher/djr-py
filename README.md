# djr-py
My personal Python package

Tagged commits trigger Google Cloud Build to build package and upload to GCS bucket.  Last step of pipeline triggers *another* Google Cloud Build job (see [here](https://github.com/donaldrauscher/gcs-pypi)) that converts GCS bucket into a simple PyPI static site server using [`dumb-pypi`](https://github.com/chriskuehl/dumb-pypi).

Install package:
```
pip install djr-py==X.X.X --extra-index-url http://pypi.donaldrauscher.com/simple --trusted-host pypi.donaldrauscher.com
```

NOTE: Need `--trusted-host` since not using HTTPS (and [can only use HTTP](https://cloud.google.com/storage/docs/troubleshooting#https) when hosting a static website)

Or Add the `--extra-index-url` option at the top of your `requirements.txt`:
```
--extra-index-url http://pypi.donaldrauscher.com/simple
--trusted-host pypi.donaldrauscher.com
djr-py==X.X.X
...
```

To trigger build manually:
```
gcloud builds submit --config cloudbuild.yaml --no-source --substitutions=TAG_NAME=X.X.X
```

NOTE: Build requires `python-packager` custom step.  Build with the following command:
```
gcloud builds submit --gcs-source-staging-dir=gs://djr-data/cloudbuild --config cloudbuild_step.yaml .
```
