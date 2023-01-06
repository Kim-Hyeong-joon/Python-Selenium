from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class YoutubeCommentCollector:
    def __init__(self):
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        #self.options.add_argument("--headless")
        self.service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=self.service, options=self.options)
    
    def start(self, url, word):
        self.browser.get(url)

        WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "placeholder-area")))
        # 스크롤 내리면 댓글이 또 생겨나서 끝까지 스크롤 하는 코드
        current_scroll_size = 0
        while True:
            get_scroll_size = self.browser.execute_script("return document.getElementById('columns').scrollHeight")
            if not get_scroll_size == current_scroll_size:
                self.browser.execute_script(f"window.scrollTo(0, {get_scroll_size})")
                sleep(3)
            else:
                break
            current_scroll_size = get_scroll_size
        # 유튜브 프리미엄 광고창 끄기
        try:
            self.browser.find_element(By.XPATH,"/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/yt-mealbar-promo-renderer/div")
            button = self.browser.find_element(By.XPATH, "/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/yt-mealbar-promo-renderer/div/div[2]/yt-button-renderer[1]/yt-button-shape/button")
            button.click()
        except:
            pass

        #자세히 버튼 클릭
        more_buttons = self.browser.find_elements(By.CSS_SELECTOR, "#more > .more-button")

        for more_button in more_buttons:
            if more_button.text == "자세히 보기":
                self.browser.execute_script(
                    """
                    const moreButton = arguments[0];
                    moreButton.click();
                """, more_button
                )

        #댓글 스크린샷
        comments = self.browser.find_elements(By.ID, "comment-content")

        for index, comment in enumerate(comments):
            if word in comment.text:
                comment.screenshot(f"screenshots/youtube/comment-{index}.png")
        
        self.browser.quit()

url = "https://www.youtube.com/watch?v=TzBXBRX6hd4&t=210s"
youtube_collector = YoutubeCommentCollector()
youtube_collector.start(url, "엑셀")