import csv
from dotenv import load_dotenv
import os
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class InstaHashtagMinior:
    def __init__(self, initial_hashtag):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.initial_hashtag = initial_hashtag
        self.counted_hashtags = []
        load_dotenv()

    def login(self):
        INSTAGRAM_ID = os.environ.get("INSTA_ID")
        INSTAGRAM_PASSWORD = os.environ.get("INSTA_PASSWORD")


        self.browser.get("https://www.instagram.com/accounts/login/")

        WebDriverWait(self.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_ab3b")))

        id_input = self.browser.find_element_by_name("username")
        password_input = self.browser.find_element_by_name("password")

        id_input.send_keys(INSTAGRAM_ID)
        password_input.send_keys(INSTAGRAM_PASSWORD)

        password_input.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_aa55")))

    def make_report(self):
        file = open(f"{self.initial_hashtag}-report.csv", "w")
        writer = csv.writer(file)
        writer.writerow(["Hastag", "Post Count"])

        for hashtag in self.counted_hashtags:
            writer.writerow(hashtag)

    def start(self):
        self.login()
        self.browser.get("https://www.instagram.com")

        WebDriverWait(self.browser, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "._a9-z > ._a9_1")))

        button = self.browser.find_element_by_css_selector("._a9-z > ._a9_1")
        button.click()

        self.browser.set_window_size(755, 800)
        search_bar = self.browser.find_element_by_css_selector("._aawg > input")
        search_bar.send_keys(self.initial_hashtag)
        WebDriverWait(self.browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".x12dtdjy > div:nth-child(5)")))
        related_keywords = self.browser.find_elements_by_css_selector(".x12dtdjy > div")

        for related_keyword in related_keywords:
            keyword_text = self.browser.execute_script(
                """
            const keyword = arguments[0];
            return keyword.innerText;
            """,
            related_keyword,
            )
            counted_hashtag = keyword_text.split("\n")
            hashtag_name = counted_hashtag[0][1:]
            post_count_float = float(re.findall("\d+.\d+",counted_hashtag[1].replace("게시물 ", ""))[0])
            post_count_unit = counted_hashtag[1].strip()[-1]
            post_count = 0
            if post_count_unit == "억":
                post_count = int(post_count_float * 100000000)
            elif post_count_unit == "만":
                post_count = int(post_count_float * 10000)
            else:
                post_count = int(post_count_float)

            self.counted_hashtags.append((hashtag_name, post_count))

        self.browser.quit()
        self.make_report()

            
hashtag_minor = InstaHashtagMinior("#dog")
hashtag_minor.start()