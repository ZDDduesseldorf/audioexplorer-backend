FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV AUDIO_EXPLORER_DATA_DIR=/app/testdata

ENV TRANSFORMERS_CACHE=/app/.cache/huggingface


COPY requirements.txt .
COPY testdata ./testdata

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY scripts ./scripts

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]