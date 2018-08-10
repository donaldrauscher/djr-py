# djr-py
My personal Python package

Tagged commits trigger Google Cloud Build to build package and upload to GCS bucket.  NOTE: last 2 steps of pipeline trigger *another* Google Cloud Build job (see [here](https://github.com/donaldrauscher/gcs-pypi)) that converts GCS bucket into a simple PyPI static site server using [`dumb-pypi`](https://github.com/chriskuehl/dumb-pypi).

To install package:
```
pip install djr-py==X.X.X --extra-index-url http://pypi.donaldrauscher.com/simple --trusted-host pypi.donaldrauscher.com
```

Or add the `--extra-index-url` option at the top of your `requirements.txt`:
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

Ruunning this Cloud Build job requires a `python-packager` custom step; can build by running the following:
```
gcloud builds submit --gcs-source-staging-dir=gs://djr-data/cloudbuild --config cloudbuild_step.yaml .
```
