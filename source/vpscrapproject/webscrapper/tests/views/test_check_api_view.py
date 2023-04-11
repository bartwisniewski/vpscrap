from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse
from unittest.mock import patch, Mock, MagicMock
from celery.result import states

TASK_ID = "abcd1234"
TEST_STATE = states.FAILURE


class MockAsyncResult:
    def __init__(self, id: str):
        self.id = id
        self.status = TEST_STATE


@patch("webscrapper.views.AsyncResult", MockAsyncResult)
class CheckApiViewTest(TestCase):
    url = reverse("check", kwargs={"task_id": TASK_ID})

    def setUp(self):
        self.client = Client()

    def test_should_return_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_return_status(self):
        response = self.client.get(self.url)
        self.assertIn("status", response.json())

    def test_should_return_correct_status(self):
        response = self.client.get(self.url)
        status = response.json().get("status", None)
        self.assertEqual(status, TEST_STATE)
