import os

from selenium import webdriver


class Driver:
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
        self.driver = webdriver.Remote(f"http://{host}:{port}/wd/hub", options=self.options)
        print("done", flush=True)
        self.driver.implicitly_wait(5)
