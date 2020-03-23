from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Database import Database
import time


class Article:
    def __init__(self, url, parser):
        self.parser = parser
        self.url = url

    @property
    def title(self):
        return self.parser.find("h1").contents[0]

    @property
    def paragraphs(self):
        try:
            return self._paragraphs
        except:
            pTags = self.parser.findAll("p")
            self._paragraphs = "".join([str(tag) for tag in pTags])
            return self._paragraphs

    @property
    def publishTime(self):
        return self.parser.find("time").find("noscript").contents[0]


class BloombergCrawler:
    BaseUrl = "https://www.bloomberg.com"

    def __init__(self):
        self.driver = None
        self.verbose = True
        self.articles = []
        self.db = Database()

    def _initiateDriver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option(
            "prefs", {'profile.managed_default_content_settings.javascript': 2})
        driver = webdriver.Chrome(
            "./chromedriver", chrome_options=chrome_options)
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
            time.sleep(5)
        self.db.save(self.articles)
        self.driver.quit()


if __name__ == "__main__":
    crawler = BloombergCrawler()
    crawler.run()
