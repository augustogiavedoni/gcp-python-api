FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY src ./src

ENV PORT=8080

CMD ["sh", "-c", "fastapi run src/gcp_python_api/main.py --host 0.0.0.0 --port ${PORT}"]