
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


from webscrapper.schemas.serializers import QuerySerializer, PlaceSerializer, StatusSerializer
from webscrapper.logic.implementations.slowhop import SlowhopScrapper


class Scrap(APIView):
    def post(self):
        data = JSONParser().parse(self.request.data)
        query_serializer = QuerySerializer(data)
        query = query_serializer.save()
        scrapper = SlowhopScrapper()
        results = scrapper.run(query)
        for result in results:
            print(result)


def check_status(job_id: int):
    return 0


class Check(APIView):
    def get(self):
        job_id = 1
        status = check_status(job_id)
        return Response({"job": job_id, "status": status})
