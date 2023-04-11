from datetime import datetime
from dataclasses import dataclass

from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse
from unittest.mock import patch
from webscrapper.schemas.schemas import Query
from webscrapper.schemas.serializers import QuerySerializer

TASK_ID = "abcd1234"


def mock_scrap_job(*args, **kwargs):
    @dataclass
    class Task:
        id: str = TASK_ID

    return Task()


@patch("webscrapper.queue_logic.tasks.scrap.delay", mock_scrap_job)
class ScrapApiViewTest(TestCase):
    url = reverse("scrap")

    def setUp(self):
        self.client = Client()
        query = Query(
            region="Mazury",
            adults=4,
            children=0,
            infants=0,
            start_date=datetime(2023, 7, 20),
            end_date=datetime(2023, 7, 27),
        )
        serializer = QuerySerializer(query)
        self.query_data = serializer.data

    def test_should_return_ok(self):
        response = self.client.post(self.url, json=self.query_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_return_task_id(self):
        response = self.client.post(self.url, json=self.query_data)
        self.assertIn("task_id", response.json())

    def test_should_return_correct_task_id(self):
        response = self.client.post(self.url, json=self.query_data)
        task_id = response.json().get("task_id", 0)
        self.assertEqual(task_id, TASK_ID)
