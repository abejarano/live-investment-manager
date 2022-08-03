FROM python:3.9.6-alpine

ENV HOME=/app
WORKDIR $HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create the appropriate directories
RUN mkdir /app/static
RUN mkdir /app/media


# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev && apk add --no-cache --upgrade bash

# copy project
ADD . .

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

RUN sed -i 's/\r$//g' $HOME/entrypoint.sh
RUN chmod +x $HOME/entrypoint.sh
RUN sh $HOME/entrypoint.sh

CMD gunicorn --bind 0.0.0.0:8080 --workers 2 --threads 8 --timeout 0 crypto_investment.wsgi:application

