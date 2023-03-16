
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.urls import reverse
from django.views.generic import TemplateView

from webscrapper.schemas.serializers import QuerySerializer, PlaceSerializer, StatusSerializer
from webscrapper.logic.implementations.slowhop import SlowhopScrapper
from webscrapper.forms import QueryForm


class Scrap(APIView):
    def post(self, *args, **kwargs):
        print(self.request.data)
        query_json = self.request.data
        print(query_json)
        query_serializer = QuerySerializer(data=query_json)
        if query_serializer.is_valid():
            query = query_serializer.save()
            scrapper = SlowhopScrapper()
            results = scrapper.run(query)
            for result in results:
                print(result)
        else:
            print("invalid")


def check_status(job_id: int):
    return 0


class Check(APIView):
    def get(self):
        job_id = 1
        status = check_status(job_id)
        return Response({"job": job_id, "status": status})


class SendJsonView(TemplateView):
    template_name = "webscrapper/send_json.html"

    def get_context_data(self, **kwargs):
        context = {"form": QueryForm(), 'endpoint': reverse("scrap")}
        return context
