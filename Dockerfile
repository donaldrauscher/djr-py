FROM gcr.io/cloud-builders/gcloud

COPY requirements.txt .

RUN apt-get update \
  && apt-get install -y python3-pip \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT ["python3"]
