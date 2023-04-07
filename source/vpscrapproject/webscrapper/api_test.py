import requests
from datetime import datetime
import os
import sys
import django
import time
from django.urls import reverse

from webscrapper.schemas.serializers import QuerySerializer
from webscrapper.schemas.schemas import Query

from celery import states

URL = "http://127.0.0.1:8001/"


def get_results(task_id: str):
    endpoint = reverse("result", kwargs={"job_id": task_id})
    response = requests.get(URL + endpoint)
    data = response.json()
    results = data.get("result", [])
    for result in results:
        print(result)


def wait_for_job_done(task_id: str):
    endpoint = reverse("check", kwargs={"job_id": task_id})
    for tries in range(10):
        response = requests.get(URL + endpoint)
        data = response.json()
        if data.get("status", states.PENDING) == states.SUCCESS:
            return True
        time.sleep(2)
    return False


def new_job():
    sys.path.append("/home/bartwisniewski/DevMentoring/vpscrap/source/vpscrapproject")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vpscrapproject.settings")
    django.setup()
    endpoint = reverse("scrap")
    query = Query("Mazury", 2, 2, 0, datetime(2023, 7, 23), datetime(2023, 7, 30))
    serializer = QuerySerializer(query)
    response = requests.post(URL + endpoint, json=serializer.data)
    if response.status_code != 200:
        return
    task_id = response.json().get("task_id", None)
    if task_id:
        time.sleep(2)
        success = wait_for_job_done(task_id)
    else:
        success = False

    if success:
        get_results(task_id)


def just_check(task_id):
    sys.path.append("/home/bartwisniewski/DevMentoring/vpscrap/source/vpscrapproject")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vpscrapproject.settings")
    django.setup()
    wait_for_job_done(task_id)


if __name__ == "__main__":
    new_job()
    # just_check('761a3c7c-66ea-4811-8de6-5520798ef0e5')
