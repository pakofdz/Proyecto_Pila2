First install docker: https://www.docker.com/get-started/

Commands to create docker:

1. docker-compose up

In another terminal or shittung down the docker with: docker-compose down

2. docker-compose run web python manage.py makemigrations
3. docker-compose run web python manage.py migrate
4. docker-compose run web python manage.py makemigrations store
5. docker-compose run web python manage.py migrate store
6. docker-compose run web python manage.py migrate store 0001
7. docker-compose run web python manage.py createsuperuser
