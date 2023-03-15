from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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
        self.options.add_argument('--headless')
        self.options.add_argument("--lang=pl-PL")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_experimental_option('prefs', {'intl.accept_languages': 'pl,pl_PL'})
        self.options.page_load_strategy = 'none'
        self.path = ChromeDriverManager().install()
        self.service = Service(self.path)
        self.driver = Chrome(options=self.options, service=self.service)
        self.driver.implicitly_wait(5)


if __name__ == "__main__":
    # The client code.

    d1 = Driver()
    d2 = Driver()

    if id(d1) == id(d2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")
