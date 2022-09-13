FROM python:3.10

COPY ./shop/requirements.txt /

RUN pip install -r requirements.txt

COPY ./docker/shop/docker-entrypoint.sh ./docker/shop/wait-for-command.sh /
RUN chmod +x /docker-entrypoint.sh /wait-for-command.sh

COPY ./shop/ /app

WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]