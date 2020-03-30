import datetime
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Database import BloombergDB
import time
import logging
import os
from Article import Article
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
logging.basicConfig(filename=dir_path+'/test.log', level="INFO")


class BloombergCrawler:
    BaseUrl = "https://www.bloomberg.com"

    def __init__(self):
        self.driver = None
        self.verbose = True
        self.articles = []
        self.db = BloombergDB()

    def _initiateDriver(self):
        chrome_options = Options()
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("user-agent={}".format(user_agent))
        chrome_options.add_experimental_option(
            "prefs", {'profile.managed_default_content_settings.javascript': 2})
        mobile_emulation = {"deviceName": "iPhone 6"}
        chrome_options.add_experimental_option(
            "mobileEmulation", mobile_emulation)
        driver = webdriver.Chrome(
            "/Users/warrencheng/BloombergLineBot/chromedriver", options=chrome_options)
        self.driver = driver

    def _getParserFrom(self, url):
        self.driver.get(url)
        return BeautifulSoup(self.driver.page_source)

    def _getArticlesUrlsFrom(self, frontPageParser):
        articleClasses = [
            "single-story-module__headline-link",
            "single-story-module__related-story-link",
            "story-package-module__story__headline-link",
        ]
        articleTags = frontPageParser.findAll(True, {"class": articleClasses})
        return [tag.get("href") for tag in articleTags]

    def run(self, verbose=True):
        self.vernose = verbose
        if not self.driver:
            self._initiateDriver()
        frontPageParser = self._getParserFrom(self.BaseUrl)
        articlesUrls = self._getArticlesUrlsFrom(frontPageParser)
        for url in articlesUrls:
            articleParser = self._getParserFrom(self.BaseUrl + url)
            article = Article(url, articleParser) if articleParser else None
            self.articles.append(article)
            logging.info(article.titleSlug)
            time.sleep(5)

        self.db.save(self.articles)
        # self.driver.quit()


if __name__ == "__main__":
    logging.info("start")
    crawler = BloombergCrawler()
    crawler.run()
    logging.info("finish {}".format(datetime.datetime.now()))
