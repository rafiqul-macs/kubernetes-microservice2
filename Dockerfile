FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py app.py

EXPOSE 5000

CMD ["python", "app.py"]
