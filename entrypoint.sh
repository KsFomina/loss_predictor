#!/bin/sh
set -e

echo "Loading item features into DB..."
python -m app.loader artifacts/item_features.csv

echo "Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000