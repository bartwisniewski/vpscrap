import requests
from datetime import datetime
import os
import sys
import django
from django.conf import settings
from vpscrapproject import settings as my_settings
from django.urls import reverse

from webscrapper.schemas.serializers import QuerySerializer
from webscrapper.schemas.schemas import Query


def new_job():
    sys.path.append('/home/bartwisniewski/DevMentoring/vpscrap/source/vpscrapproject')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vpscrapproject.settings')
    django.setup()
    endpoint = reverse("scrap")
    query = Query("Mazury", 2, 2, 0, datetime(2023, 7, 23), datetime(2023, 7, 30))
    serializer = QuerySerializer(query)
    response = requests.post("http://127.0.0.1:8000/"+endpoint, json=serializer.data)
    print(response)
    print(response.json())


if __name__ == "__main__":
    new_job()
