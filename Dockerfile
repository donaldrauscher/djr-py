FROM gcr.io/cloud-builders/gcloud

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT ["python3", "setup.py"]
