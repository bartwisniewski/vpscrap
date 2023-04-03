
from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult, states
from django.urls import reverse
from django.views.generic import TemplateView
from webscrapper.forms import QueryForm
from webscrapper.queue_logic.tasks import scrap


class Scrap(APIView):
    def post(self, request, format=None):
        query_json = request.data
        task = scrap.delay(query_json)
        return Response(data={'task_id': task.id}, status=200)


def get_state(result: AsyncResult) -> any:
    try:
        return result.status
    except ValueError:
        return states.FAILURE


class Check(APIView):
    def get(self, request, job_id, format=None):
        result = AsyncResult(id=job_id)
        status = get_state(result)
        return Response(data={"job": job_id, "status": status}, status=200)


class Result(APIView):
    def get(self, request, job_id, format=None):
        result = AsyncResult(id=job_id)
        if result.ready() or result.ignored:
            if result.successful():
                result_data = result.get()
            else:
                result_data = []
            return Response(data={"job": job_id, "result": result_data}, status=200)
        status = get_state(result)
        return Response(data={"job": job_id, "status": status}, status=200)


class SendJsonView(TemplateView):
    template_name = "webscrapper/send_json.html"

    def get_context_data(self, **kwargs):
        context = {"form": QueryForm(), 'endpoint': reverse("scrap")}
        return context
