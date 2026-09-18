FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-model.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY artifacts/ ./artifacts/
COPY entrypoint.sh ./

RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh
RUN mkdir -p /app/data

ENV DATABASE_URL=sqlite:////app/data/app.db
ENV MODEL_PATH=/app/artifacts/model.joblib
ENV MODEL_METADATA_PATH=/app/artifacts/model_metadata.json

EXPOSE 8000
CMD ["./entrypoint.sh"]
