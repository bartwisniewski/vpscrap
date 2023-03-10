from dataclasses import dataclass
from datetime import datetime
from driver import Driver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time

from webscrapper.scrapper import Scrapper, Place, Query

PL = "pl-PL"


class SlowhopScrapper(Scrapper):
    BASE_URL = "https://slowhop.com/pl/katalog"

    def __init__(self):
        self.driver = Driver().driver
        self.search_bar = None
        self.url_parameters = ""
        self.results = []

    def is_polish(self) -> bool:
        language = self.driver.find_element(By.XPATH, "/html/head/meta[7]").get_attribute('content')
        return language == PL

    def set_polish(self) -> None:
        language_button = self.driver.find_element(By.XPATH, "/html/body/div/div/div/nav/div[2]/ul[3]/div/button")
        language_button.click()
        time.sleep(2)
        # self.driver.get_screenshot_as_file("language_change.png")
        language_field = self.driver.find_element(By.XPATH, "/ html / body / div[2] / div[1] / div / div / div / div")
        polish = language_field.find_element(By.CSS_SELECTOR, 'img[alt="pl"]')
        polish_a = polish.find_element(By.XPATH, "./..")
        polish_a.click()
        time.sleep(2)
        # self.driver.get_screenshot_as_file("polish.png")

    def load_place_hints(self, place_search: str) -> None:
        place_filter = self.search_bar.find_element(By.CSS_SELECTOR, "input#where")
        place_filter.click()
        time.sleep(2)
        self.driver.get_screenshot_as_file("input.png")
        # place_filter_editable = self.search_bar.find_element(By.CSS_SELECTOR,
        #                                                 "aside > div.advanced-options__header > div > input")

        place_filter.send_keys(place_search)
        time.sleep(2)
        self.driver.get_screenshot_as_file("hints.png")

    def get_place_phrase(self, place_search: str) -> str:
        self.search_bar = self.driver.find_element(By.CSS_SELECTOR, "div.search-bar")
        self.load_place_hints(place_search)
        result_links = self.search_bar.find_element(By.CSS_SELECTOR, "div.result-links")
        result_links_list = result_links.find_element(By.CSS_SELECTOR, "ul.result-links__list")
        best_hint = result_links_list.find_element(By.CSS_SELECTOR, 'a[href="#"]')
        best_hint.click()
        time.sleep(2)
        return self.driver.current_url.split('?')[1]

    def make_url_parameters(self, query: Query) -> None:
        self.url_parameters = ""
        self.url_parameters += self.get_place_phrase(query.place)
        self.url_parameters += f"&adults={query.adults}"
        self.url_parameters += f"&children={query.children}"
        str_children_age = ",".join(map(str, query.children_age))
        self.url_parameters += f"&children_age={str_children_age}"
        self.url_parameters += f"&start_date=2023-07-22"
        self.url_parameters += f"&end_date=2023-07-29"

    def scrap(self):
        self.results = []
        url = self.BASE_URL + "?" + self.url_parameters
        self.driver.get(url)
        time.sleep(3)
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        places = soup.find_all("div", class_="catalog-tile")
        self.driver.get_screenshot_as_file("results.png")
        for place in places:
            content = place.find_all("div", class_="catalog-tile__content")[0]
            result = Place()
            result.address = content.address.string
            result.name = content.find_all(class_="catalog-tile__name")[0].string
            result.description = content.find_all(class_="catalog-tile__description")[0].string
            result.price = content.find_all("span", class_="minimal-price__value")[0].string
            link = place.find_all("a")[0]['href']
            result.url = self.BASE_URL + link.split("?")[0]
            self.results.append(result)

    def run(self, query: Query) -> list[Place]:
        self.driver.get(self.BASE_URL)
        time.sleep(2)
        if not self.is_polish():
            self.set_polish()
        self.make_url_parameters(query)
        self.scrap()

        return self.results


def enlist_attributes(element) -> list:
    attrs = []
    for attr in element.get_property('attributes'):
        attrs.append([attr['name'], attr['value']])
    return attrs


if __name__ == "__main__":
    scrapper = SlowhopScrapper()
    query = Query(place="Mazury", adults=8, children=3, children_age=[5, 5, 3], start_date=datetime(2023, 7, 20),
                  end_date=datetime(2023, 7, 27))
    results = scrapper.run(query)
    for result in results:
        print(result)
