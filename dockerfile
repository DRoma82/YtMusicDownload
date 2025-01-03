FROM python:slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./*.py .

RUN mkdir /cache

ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

CMD ["python", "app.py"]
