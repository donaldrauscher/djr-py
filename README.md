# djr-py
My personal Python package

Use Google Cloud Container Builder to build package and upload to Gemfury.  Trigger specifically for tagged commits.

Install package:
```
pip install djr-py --extra-index-url https://${FURY_TOKEN}@pypi.fury.io/donaldrauscher/
```

NOTE: Need to create a KMS key/keyring, give Google Container Builder access to it, and use that key to encrypt your Fury token.  You can find additional instructions on how to do this [here](https://cloud.google.com/container-builder/docs/securing-builds/use-encrypted-secrets-credentials).
```
echo -n ${FURY_TOKEN} | gcloud kms encrypt --plaintext-file=- --ciphertext-file=- --location=global --keyring=djr --key=fury | base64
```

Build cloud builder image:
```
gcloud container builds submit --gcs-source-staging-dir=gs://djr-data/cloudbuild --config cloudbuild_step.yaml .
```
