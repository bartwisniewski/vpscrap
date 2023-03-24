import os
import sys

from selenium import webdriver

from django.conf import settings


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Driver(metaclass=SingletonMeta):
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--no-sandbox")
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument("--remote-debugging-port=9222")
        self.options.add_argument('--headless')
        self.options.add_argument("--lang=pl-PL")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_experimental_option('prefs', {'intl.accept_languages': 'pl,pl_PL'})
        self.options.page_load_strategy = 'none'

        host = os.environ.get('SELENIUM_HOST', '')
        port = os.environ.get('SELENIUM_PORT', '')

        print("init driver", flush=True)
        # self.driver = Chrome(options=self.options, service=self.service)
        self.driver = webdriver.Remote(f"http://{host}:{port}/wd/hub", options=self.options)
        print("done", flush=True)
        self.driver.implicitly_wait(5)


if __name__ == "__main__":
    # The client code.

    d1 = Driver()
    d2 = Driver()

    if id(d1) == id(d2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")
