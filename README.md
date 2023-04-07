# Vacation planner - web scrapper

Part of a vacation planner project. Microservice that searhces web for a places to go for a vacation given parameters like number of people, dates and prefered region. All requests are processed asynchronicaly in a queue using celery rabbitmq and redis. Starting new jobs and retrieving scrapping results is performed through rest api.

Stack:
- Python 
- Django
- Django Rest Framework
- Celery
- RabbitMQ
- Javascript
- Postgresql
- Redis

-------------------------------------------------------------------
Core application
Main part of vacation planner:
https://github.com/bartwisniewski/VacationPlanner
