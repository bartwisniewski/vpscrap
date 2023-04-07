from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse
from unittest.mock import patch

TASK_ID = "abcd1234"


def mock_scrap_job(*args, **kwargs):
    return TASK_ID


class ScrapApiViewTest(TestCase):
    url = reverse("scrap")

    def setUp(self):
        self.client = Client()

    @patch("scrap.delay", mock_scrap_job)
    def test_should_return_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_return_task_id(self):
        response = self.client.get(self.url)
        self.assertIn("task_id", response.json())

    def test_should_return_correct_task_id(self):
        response = self.client.get(self.url)
        task_id = response.json().get("task_id", 0)
        self.assertEqual(task_id, TASK_ID)
