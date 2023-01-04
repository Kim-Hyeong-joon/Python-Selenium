import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get("https://nomadcoders.co")
browser.maximize_window()

max_width = browser.get_window_size().get("width")

sizes = [320, 480, 960, 1366, 1920, max_width]

sizes.sort()

for size in sizes:
    if size <= max_width:
        browser.set_window_size(size, 944)
        time.sleep(5)