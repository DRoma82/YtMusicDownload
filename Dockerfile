FROM python:slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip --root-user-action

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --root-user-action

COPY ./*.py ./

RUN mkdir /templates

COPY ./templates/* /templates/

RUN mkdir /cache

ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

CMD ["python", "web.py"]
