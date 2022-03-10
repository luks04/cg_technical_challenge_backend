FROM python:3.8.12-slim-buster

ADD . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt

CMD ["gunicorn", "app:app"]