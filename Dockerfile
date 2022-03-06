FROM python:3.8-buster

WORKDIR /app

ADD . .

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN chown -R www-data:www-data /app

# RUN ln -s /usr/local/lib/python3.8/dist-packages/django/contrib/admin/static/admin/ /app/static/admin


# start server
EXPOSE 8000
STOPSIGNAL SIGTERM
