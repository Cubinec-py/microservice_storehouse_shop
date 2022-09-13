FROM python:3.10

COPY ./storehouse/requirements.txt /

RUN pip install -r requirements.txt

COPY ./docker/storehouse/docker-entrypoint.sh ./docker/storehouse/wait-for-command.sh /
RUN chmod +x /docker-entrypoint.sh /wait-for-command.sh

COPY ./storehouse/ /app

WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]