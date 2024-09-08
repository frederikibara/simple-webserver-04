# Dockerfile
FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000
EXPOSE 5000

CMD ["python", "main.py"]
