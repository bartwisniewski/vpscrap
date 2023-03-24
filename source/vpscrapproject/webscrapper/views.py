
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from celery.result import AsyncResult
from django.urls import reverse
from django.views.generic import TemplateView
from webscrapper.schemas.serializers import QuerySerializer
from webscrapper.forms import QueryForm
from webscrapper.queue_logic.tasks import scrap


class Scrap(APIView):
    def post(self, request, format=None):
        query_json = request.data
        task = scrap.delay(query_json)
        return Response(data={'task_id': task.id}, status=200)


# class Scrap(APIView):
#     def post(self, *args, **kwargs):
#         print("post")
#         query_json = self.request.data
#         print(query_json)
#         query_serializer = QuerySerializer(data=query_json)
#         if query_serializer.is_valid():
#             print("query is valid")
#             query = query_serializer.save()
#             print(query)
#             task = scrap.delay(query)
#             return Response(data={'task_id': task.id}, status=200)
#         print("invalid")
#         return Response(status=400)

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
