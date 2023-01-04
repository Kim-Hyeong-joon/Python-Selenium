from dotenv import load_dotenv
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

INSTAGRAM_ID = os.environ.get("INSTA_ID")
INSTAGRAM_PASSWORD = os.environ.get("INSTA_PASSWORD")
browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get("https://www.instagram.com/accounts/login/")

WebDriverWait(browser, 10).until(
EC.presence_of_element_located((By.CLASS_NAME, "_ab3b")))

insta_id = browser.find_element_by_name("username")
insta_password = browser.find_element_by_name("password")

insta_id.send_keys(INSTAGRAM_ID)
insta_password.send_keys(INSTAGRAM_PASSWORD)

insta_password.send_keys(Keys.ENTER)

WebDriverWait(browser, 10).until(
EC.presence_of_element_located((By.CLASS_NAME, "_aa55")))

main_hashtag = "#dog"

browser.get("https://www.instagram.com")

WebDriverWait(browser, 15).until(
EC.presence_of_element_located((By.CSS_SELECTOR, "._a9-z > ._a9_1")))

button = browser.find_element_by_css_selector("._a9-z > ._a9_1")
button.click()

browser.set_window_size(755, 800)
search_bar = browser.find_element_by_css_selector("._aawg > input")
search_bar.send_keys(main_hashtag)
WebDriverWait(browser, 10).until(
EC.presence_of_element_located((By.CSS_SELECTOR, ".x12dtdjy > div:nth-child(5)")))
related_keywords = browser.find_elements_by_css_selector(".x12dtdjy > div")

hashtags_n_posts = []

for related_keyword in related_keywords:
    keyword_text = browser.execute_script(
        """
    const keyword = arguments[0];
    return keyword.innerText;
    """,
    related_keyword,
    )
    hashtag_n_post = keyword_text.split("\n")
    hashtags_n_posts.append(hashtag_n_post)

print(hashtags_n_posts)