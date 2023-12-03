FROM python:3.11.1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /formviewer
COPY requirements.txt /formviewer/requirements.txt
RUN pip install -r requirements.txt
COPY . /formviewer