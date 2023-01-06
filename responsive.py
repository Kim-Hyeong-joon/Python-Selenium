import os
from math import ceil
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class ResponsiveTester:

    def __init__(self, urls):
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        #self.options.add_argument("--headless")
        self.service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=self.service, options=self.options)
        self.browser.maximize_window()
        self.urls = urls
        self.max_width = self.browser.get_window_size().get("width")
        self.max_height = self.browser.get_window_size().get("height")
        self.max_inner_height = self.browser.execute_script("return window.innerHeight - 64")
        self.sizes = [480, 960, 1366, 1920, self.max_width]

    def screenshot(self,url,dir_name):
        self.browser.get(url)
        self.sizes.sort()
        for size in self.sizes:
            self.browser.set_window_size(size, self.max_height)
            self.browser.execute_script("window.scrollTo(0,0)")
            time.sleep(3)
            scroll_size = self.browser.execute_script("return document.body.scrollHeight")
            total_sections = ceil(scroll_size / self.max_inner_height)
            for section in range(total_sections+1):
                self.browser.execute_script(f"window.scrollTo(0, {(section) * self.max_inner_height})")
                self.browser.save_screenshot(f"screenshots/{dir_name}/{size}x{section}.png")
                time.sleep(2)

    def start(self):
        for url in self.urls:
            dir_name = url.split("https://")[1].split(".")[0]
            try:
                if not os.path.exists(dir_name):
                    os.makedirs(f"screenshots/{dir_name}")
            except:
                pass
            self.screenshot(url, dir_name)


tester = ResponsiveTester(["https://nomadcoders.co","https://google.com"])
tester.start()