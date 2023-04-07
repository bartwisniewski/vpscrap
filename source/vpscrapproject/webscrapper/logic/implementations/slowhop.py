from datetime import datetime

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from webscrapper.logic.interfaces.scrapper import Scrapper, Place, Query
from webscrapper.logic.drivers.remote import Driver
from webscrapper.utils.helpers import clean_text

SCREENSHOTS_PATH = "/app/screenshots/"
DEBUG = False


class SlowhopScrapper(Scrapper):
    BASE_URL = "https://slowhop.com/pl/katalog"
    HOME_URL = "https://slowhop.com"
    LANGUAGE_XPATH = "/html/head/meta[7]"

    def __init__(self):
        self.driver = Driver().driver
        self.search_bar = None
        self.url_parameters = ""
        self.results = []

    def wait_for_element(self, locator: tuple) -> None:
        timeout = 10
        try:
            element_present = EC.presence_of_element_located(locator=locator)
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print(f"Timed out waiting for element {locator}")

    def wait_for_element_attribute(
        self, locator: tuple, attribute: str, value: str
    ) -> None:
        timeout = 10
        try:
            element_loaded = EC.text_to_be_present_in_element_attribute(
                locator, attribute, value
            )
            WebDriverWait(self.driver, timeout).until(element_loaded)
        except TimeoutException:
            print(f"Timed out waiting for element {locator}")

    def wait_for_not_text(self, locator: tuple, text: str) -> None:
        timeout = 10
        try:
            text_present = EC.text_to_be_present_in_element(locator, text)
            text_not_present = EC.none_of(text_present)
            WebDriverWait(self.driver, timeout).until(text_not_present)
        except TimeoutException:
            print(f"Timed out waiting for {text} to not be in {locator}")

    def wait_for_url(self, url_part: str) -> None:
        timeout = 10
        try:
            url_contains = EC.url_contains(url_part)
            WebDriverWait(self.driver, timeout).until(url_contains)
        except TimeoutException:
            print(f"Timed out waiting for url containing {url_part}")

    def is_polish(self) -> bool:
        self.wait_for_element(locator=(By.XPATH, SlowhopScrapper.LANGUAGE_XPATH))
        language = self.driver.find_element(
            By.XPATH, SlowhopScrapper.LANGUAGE_XPATH
        ).get_attribute("content")
        return language == "pl-PL"

    def set_polish(self) -> None:
        language_button_xpath = "/html/body/div/div/div/nav/div[2]/ul[3]/div/button"
        language_button = self.driver.find_element(By.XPATH, language_button_xpath)
        if DEBUG:
            self.driver.get_screenshot_as_file(
                f"{SCREENSHOTS_PATH}beforelanguagebuttonclick.png"
            )
        language_button.click()
        if DEBUG:
            self.driver.get_screenshot_as_file(f"{SCREENSHOTS_PATH}waitingformodal.png")
        self.wait_for_element((By.ID, "language-switcher-modal___BV_modal_outer_"))
        if DEBUG:
            self.driver.get_screenshot_as_file(f"{SCREENSHOTS_PATH}modalloaded.png")
        language_field = self.driver.find_element(
            By.XPATH, "/ html / body / div[2] / div[1] / div / div / div / div"
        )
        polish = language_field.find_element(By.CSS_SELECTOR, 'img[alt="pl"]')
        polish_a = polish.find_element(By.XPATH, "./..")
        if DEBUG:
            self.driver.get_screenshot_as_file(
                f"{SCREENSHOTS_PATH}beforeclickingpolish.png"
            )
        polish_a.click()
        self.wait_for_element_attribute(
            locator=(By.XPATH, SlowhopScrapper.LANGUAGE_XPATH),
            attribute="content",
            value="pl-PL",
        )

    def load_region_hints(self, region_search: str) -> None:
        region_filter = self.search_bar.find_element(By.CSS_SELECTOR, "input#whare")
        if DEBUG:
            self.driver.get_screenshot_as_file(
                f"{SCREENSHOTS_PATH}enter_region_filter.png"
            )
        region_filter.send_keys(region_search)
        time.sleep(2)
        if DEBUG:
            self.driver.get_screenshot_as_file(f"{SCREENSHOTS_PATH}hints.png")

    def get_region_phrase(self, region_search: str) -> str:
        self.search_bar = self.driver.find_element(By.CSS_SELECTOR, "div.search-bar")
        self.load_region_hints(region_search)
        result_links = self.search_bar.find_element(By.CSS_SELECTOR, "div.result-links")
        result_links_list = result_links.find_element(
            By.CSS_SELECTOR, "ul.result-links__list"
        )
        best_hint = result_links_list.find_element(By.CSS_SELECTOR, 'a[href="#"]')
        best_hint.click()
        self.wait_for_url(url_part="?")
        return self.driver.current_url.split("?")[1]

    def make_url_parameters(self, query: Query) -> None:
        self.url_parameters = ""
        self.url_parameters += self.get_region_phrase(query.region)
        self.url_parameters += f"&adults={query.adults}"
        self.url_parameters += f"&children={query.children + query.infants}"
        children_age = ["12"] * query.children + ["1"] * query.infants
        str_children_age = ",".join(children_age)

        self.url_parameters += f"&children_age={str_children_age}"
        self.url_parameters += f"&start_date=2023-07-22"
        self.url_parameters += f"&end_date=2023-07-29"

    def scrap(self):
        self.results = []
        url = self.BASE_URL + "?" + self.url_parameters
        self.driver.get(url)
        guest_input_xpath = (
            '// *[ @ id = "content-wrapper"] / div / div / div / div / div[1] / div[2] / div[3] '
            "/ button / span[2]"
        )
        self.wait_for_not_text(locator=(By.XPATH, guest_input_xpath), text="Liczba")
        time.sleep(2)
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        places = soup.find_all("div", class_="catalog-tile", limit=10)
        if DEBUG:
            self.driver.get_screenshot_as_file(f"{SCREENSHOTS_PATH}results.png")
        for place in places:
            content = place.find_all("div", class_="catalog-tile__content")[0]
            result = Place()
            result.address = clean_text(content.address.string)
            result.name = content.find_all(class_="catalog-tile__name")[0].string
            result.description = clean_text(
                content.find_all(class_="catalog-tile__description")[0].string
            )
            price_as_list = content.find_all("span", class_="minimal-price__value")
            if price_as_list:
                result.price = float(price_as_list[0].string.split(" ")[0])
            else:
                result.price = 0.0
            link = place.find_all("a")[0]["href"]
            result.url = self.HOME_URL + link.split("?")[0]
            self.results.append(result)

    def run(self, query: Query) -> list[Place]:
        self.driver.get(self.BASE_URL)
        if not self.is_polish():
            self.set_polish()
        self.make_url_parameters(query)
        self.scrap()
        self.driver.close()

        return self.results


if __name__ == "__main__":
    scrapper = SlowhopScrapper()
    query = Query(
        region="Mazury",
        adults=8,
        children=3,
        infants=1,
        start_date=datetime(2023, 7, 20),
        end_date=datetime(2023, 7, 27),
    )
    results = scrapper.run(query)
    for result in results:
        print(result)
