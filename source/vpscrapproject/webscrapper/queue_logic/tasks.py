from selenium.common.exceptions import WebDriverException
from celery import Celery, states
from celery.exceptions import Ignore
from webscrapper.logic.implementations.slowhop import SlowhopScrapper
from vpscrapproject.celery import app
from webscrapper.schemas.serializers import PlaceSerializer, QuerySerializer


@app.task(bind=True)
def scrap(self, query):
    query_serializer = QuerySerializer(data=query)
    if query_serializer.is_valid():
        query = query_serializer.save()
        scrapper = SlowhopScrapper()
        try:
            results = scrapper.run(query)
        except WebDriverException:
            print("web driver exception")
            self.update_state(state=states.FAILURE, meta="WEB DRIVER FAILURE")
            raise Ignore()
        serializer = PlaceSerializer(results, many=True)
        return serializer.data
    return None
