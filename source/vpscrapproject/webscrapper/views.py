
from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from django.urls import reverse
from django.views.generic import TemplateView
from webscrapper.forms import QueryForm
from webscrapper.queue_logic.tasks import scrap


class Scrap(APIView):
    def post(self, request, format=None):
        query_json = request.data
        task = scrap.delay(query_json)
        return Response(data={'task_id': task.id}, status=200)


class Check(APIView):
    def get(self, request, job_id, format=None):
        result = AsyncResult(id=job_id)
        status = result.status
        return Response(data={"job": job_id, "status": status}, status=200)


class Result(APIView):
    def get(self, request, job_id, format=None):
        result = AsyncResult(id=job_id)
        if result.ready():
            return Response(data={"job": job_id, "result": result.get()}, status=200)
        return Response(data={"job": job_id, "status": result.status}, status=200)


class SendJsonView(TemplateView):
    template_name = "webscrapper/send_json.html"

    def get_context_data(self, **kwargs):
        context = {"form": QueryForm(), 'endpoint': reverse("scrap")}
        return context
