FROM python:3.8.3-slim-buster

WORKDIR /blog

# forbid .pyc file recording
# forbid bufferization
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONBUFFERED=1

WORKDIR /blog

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN export PATH=/usr/lib/postgresql/X.Y/bin/:$PATH


