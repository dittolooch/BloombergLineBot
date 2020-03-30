import requests
from bs4 import BeautifulSoup
from Database import EconomistDB
from Article import Article


class EconomistCrawler:
    baseUrl = "https://www.economist.com/printedition/"

    def __init__(self):
        self.response = requests.get(self.baseUrl)
        self.redirectedUrl = self.response.url
        self.parser = BeautifulSoup(self.response.text)
        print(self.parser)
        self.db = EconomistDB()

    def existsInDB(self):
        currentDate = self.redirectedUrl.split("/")[-1]
        return self.db.dateDownloaded(currentDate)

    def _getArticlesUrlsFrom(self, parser):
        listItems = parser.findAll("div", class_="list__item")
        for li in listItems:
            aTags = li.findAll("a")
            for a in aTags:
                href = a.get("href")
                title = a.find("span").text
                print(title)
                print(href)

    def run(self, verbose=True):
        self.vernose = verbose
        if self.existsInDB():
            print("existed")
            return

        articlesUrls = self._getArticlesUrlsFrom(self.parser)
        # for url in articlesUrls:
        #     articleParser = self._getParserFrom(self.BaseUrl + url)
        #     article = Article(url, articleParser) if articleParser else None
        #     self.articles.append(article)
        #     logging.info(article.titleSlug)
        #     time.sleep(5)

        # self.db.save(self.articles)


if __name__ == "__main__":
    crawler = EconomistCrawler()
    crawler.run()
