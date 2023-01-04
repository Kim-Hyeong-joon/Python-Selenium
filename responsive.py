from math import ceil
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get("https://nomadcoders.co")
browser.maximize_window()

max_width = browser.get_window_size().get("width")
max_height = browser.get_window_size().get("height")

sizes = [480, 960, 1366, 1920, max_width]

sizes.sort()

for size in sizes:
    if size <= max_width:
        browser.set_window_size(size, max_height)
        browser.execute_script("window.scrollTo(0,0)")
        time.sleep(3)
        scroll_size = browser.execute_script("return document.body.scrollHeight")
        total_sections = ceil(scroll_size / max_height)
        for section in range(total_sections):
            browser.execute_script(f"window.scrollTo(0, {(section+1) * max_height})")
            time.sleep(2)