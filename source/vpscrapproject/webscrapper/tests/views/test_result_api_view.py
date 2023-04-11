import celery.result
import webscrapper.views
from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse
from unittest.mock import patch, Mock, MagicMock
from celery.result import states

from webscrapper.schemas.schemas import Place
from webscrapper.schemas.serializers import PlaceSerializer

TASK_ID = "abcd1234"
PLACES_NAMES = ["Place1", "Place2", "Place3"]


class MockAsyncResult:
    def __init__(self, id: str):
        self.id = id
        self.status = states.SUCCESS
        self.ignored = False
        places_obj = [Place(name=place) for place in PLACES_NAMES]
        serializer = PlaceSerializer(places_obj, many=True)
        self.data = serializer.data

    @staticmethod
    def ready():
        return True

    @staticmethod
    def successful():
        return True

    def get(self):
        return self.data


@patch("webscrapper.views.AsyncResult", MockAsyncResult)
class ResultApiViewSuccessTest(TestCase):
    url = reverse("result", kwargs={"task_id": TASK_ID})

    def setUp(self):
        self.client = Client()

    def test_should_return_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_return_result(self):
        response = self.client.get(self.url)
        self.assertIn("result", response.json())

    def test_should_return_correct_result(self):
        response = self.client.get(self.url)
        result = response.json().get("result", [])
        result_names = set([place.get("name") for place in result])
        self.assertEqual(result_names, set(PLACES_NAMES))
