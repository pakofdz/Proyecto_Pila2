FROM python:3.12.1-alpine3.19

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apk update && python3 && apk add postgresql-dev && apk add build-base

RUN pip install psycopg2-binary

COPY ./requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



