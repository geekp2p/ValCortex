FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# include API entry points
COPY app.py standalone.py start_api.py ./

ENV HOST=0.0.0.0 PORT=8088
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8088"]
