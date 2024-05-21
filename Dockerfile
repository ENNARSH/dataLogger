FROM python:latest

WORKDIR /usr/src/app

COPY main.py .

RUN pip install --no-cache-dir requests

ENTRYPOINT ["python", "./main.py"]