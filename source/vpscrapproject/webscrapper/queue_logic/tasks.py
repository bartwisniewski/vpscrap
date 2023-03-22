from webscrapper.logic.implementations.slowhop import SlowhopScrapper
from vpscrapproject.celery import app
from webscrapper.schemas.serializers import PlaceSerializer, QuerySerializer


@app.task()
def scrap(query):
    query_serializer = QuerySerializer(data=query)
    if query_serializer.is_valid():
        query = query_serializer.save()
        scrapper = SlowhopScrapper()
        results = scrapper.run(query)
        serializer = PlaceSerializer(results, many=True)
        return serializer.data
    return None




