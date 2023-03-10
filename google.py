from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class GoogleKeywordScreenshooter:
    def __init__(self, keyword, screenshots_dir, max_page):
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        #self.options.add_argument("--headless")
        self.service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=self.service, options=self.options)
        self.keyword = keyword
        self.screenshots_dir = screenshots_dir
        self.max_page = max_page
        

    def start(self):
        self.browser.get("https://google.com")
        search_bar = self.browser.find_element(By.CLASS_NAME,"gLFyf")
        search_bar.send_keys(self.keyword)
        search_bar.send_keys(Keys.ENTER)
        n = 1
        while n <= self.max_page:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ULSxyf:nth-child(1)"))
            )
            try:
                shitty_elements = self.browser.find_elements(By.CLASS_NAME,"ULSxyf")
                self.browser.execute_script(
                    """
                const shittys = arguments[0];
                shittys.map((shitty)=>shitty.parentElement.removeChild(shitty))    
                """,
                    shitty_elements,
                )
            except Exception:
                pass
            search_results = self.browser.find_elements(By.CLASS_NAME,"MjjYud")
            for index, search_result in enumerate(search_results):
                search_result.screenshot(f"{self.screenshots_dir}/{self.keyword}xpage{n}x{index}.png")
            link_text = self.browser.find_element(By.LINK_TEXT,f"{n+1}")
            n = n + 1
            if n <= self.max_page:
                link_text.click()



    def finish(self):
        self.browser.quit()



domain_competitors = GoogleKeywordScreenshooter("buy domain", "screenshots", 2)
domain_competitors.start()
domain_competitors.finish()
python_competitors = GoogleKeywordScreenshooter("python book", "screenshots", 2)
python_competitors.start()
python_competitors.finish()