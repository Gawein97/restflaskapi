FROM python:3.7-slim-buster

ENV INSTALL_PATH /libraryapi
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN python3 create_tables.py
CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "libraryapi.app:create_app()"