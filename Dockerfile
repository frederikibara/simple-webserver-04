FROM python:3.12.0

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir
EXPOSE 3000 5000

CMD ["python", "main.py"]
