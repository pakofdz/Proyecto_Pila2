FROM python:3.12.1-alpine3.19

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apk update && python3 && apk add postgresql-dev && apk add build-base

RUN pip install psycopg2-binary

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]