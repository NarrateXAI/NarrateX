from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import Dict, List
# Import the necessary module
from dotenv import load_dotenv
import os

# Load environment variables from the .env file (if present)
load_dotenv()

import time
unix_time_plus_2_hours = int(time.time() + 2 * 60 * 60)

class XBot:
    def __init__(self, driver_path: str, base_url: str, cookie: str):
        self.driver = webdriver.Chrome(service=webdriver.ChromeService(executable_path=driver_path))
        self.base_url = base_url
        self.cookie = {
                            'domain': '.x.com',
                            'expiry': unix_time_plus_2_hours,
                            'httpOnly': True,
                            'name': 'auth_token',
                            'path': '/',
                            'sameSite': 'None',
                            'secure': True,
                            'value': cookie
                    }
    def login(self):
        self.driver.get(self.base_url)
        self.driver.add_cookie(self.cookie)
        self.driver.refresh()
    def base(self):
        self.driver.get(self.base_url)
    
    def wait_for_element(self, by: By, selector: str, timeout: int = 10):
        """Wait for an element to be present in the DOM."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )

    def upload_file(self, file_path: str):
        """Upload a file to the specified input field."""
        file_input = self.wait_for_element(By.CSS_SELECTOR, "input[data-testid='fileInput']")
        file_input.send_keys(file_path)

    def send_tweet(self, tweet_content: str):
        """Send a tweet with the given content."""
        tweet_box = self.wait_for_element(By.CSS_SELECTOR, "div[data-testid='tweetTextarea_0']")
        tweet_box.click()
        tweet_box.send_keys(tweet_content)
        time.sleep(3)
        post_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='tweetButtonInline']"))
        )
        post_button.click()
        time.sleep(3)

    def scrape_mentions(self, username: str) -> List[Dict]:
        """Scrape mentions of a given username on Twitter."""
        search_url = f"https://twitter.com/search?q=%40{username}&src=typed_query&f=live"
        self.driver.get(search_url)
        time.sleep(5)

        # Scroll to load more tweets
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Wait for content to load
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Extract tweets
        tweets_data = []
        username_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.r-18u37iz.r-1wvb978")
        href_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.css-175oi2r.r-18u37iz.r-1q142lx")
        tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")
        for tweet_element, href_element, username_element in zip(tweet_elements, href_elements, username_elements):
            try:
                tweet_text = tweet_element.find_element(By.CSS_SELECTOR, "div[data-testid='tweetText']").text
                anchor_element = href_element.find_element(By.TAG_NAME, "a")
                href_value = anchor_element.get_attribute("href")
                time_element = href_element.find_element(By.TAG_NAME, "time")
                datetime_value = time_element.get_attribute("datetime")
                username = username_element.find_element(By.TAG_NAME, "span").text
                tweets_data.append({
                    "href": href_value,
                    "datetime": datetime_value,
                    "username": username,
                    "tweet": tweet_text
                })
            except Exception as e:
                print(f"Error extracting tweet: {e}")
        return tweets_data

    def close(self):
        """Close the WebDriver session."""
        self.driver.quit()



TWITTER_COOKIES=os.getenv('TWITTER_COOKIES')
BASE_URL = os.getenv('BASE_URL')
DRIVER_PATH = os.getenv('DRIVER_PATH') # Update with your ChromeDriver path
FILE_PATH = "C:\\Users\\Alfian\\AppData\\Local\\Temp\\gradio\\8f54fafe71e36370d8e258df80931ca42aa0561b926f729c0ac7c773a66e7e65\\20250101_163450.mp4"
TWEET_CONTENT = (
    "Hello, X! 2 This is an automated tweet using Selenium with quote tweet.\n"
    "https://x.com/mdvx_test/status/1872580512684101664"
)

if __name__ == "__main__":
    automation = XBot(driver_path=DRIVER_PATH, base_url=BASE_URL, cookie=TWITTER_COOKIES)

    try:
        # Open URL and set cookie
        automation.login()
        # Upload file
        automation.upload_file(FILE_PATH)
        # Send tweet
        automation.send_tweet(
            TWEET_CONTENT
        )

        # Scrape mentions
        username = "MadivalVoyage"
        mentions = automation.scrape_mentions(username)
        for mention in mentions:
            print(mention)

    except Exception as e:
        print(f"An error occurred: {e}")
