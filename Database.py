import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from ChatHandler import PostbackIntent
SECRET = "/BloombergLineBot/Crawler/secret.json" if os.uname()[
    0] != "Darwin" else "/Users/warrencheng/BloombergLineBot/secret.json"


class Database:
    cred = credentials.Certificate(SECRET)
    firebase_admin.initialize_app(cred, {
        'projectId': "bloomberglinebot",
    })

    def __init__(self):
        self.db = firestore.client()

    def save(self, articles):
        raise NotImplementedError

    def getArticles(self, dateString=None, articleType=None):
        raise NotImplementedError

    def getArticle(self, titleSlug):
        raise NotImplementedError


class BloombergDB(Database):
    def save(self, articles):
        for article in articles:
            try:
                doc_ref = self.db.collection(
                    article.publishTime).document(article.titleSlug)
                documentDict = {
                    "time": article.publishTime,
                    "url": article.cleanUrl,
                    "type": article.contentType,
                    "image": article.imageSource,
                    "title": article.title,
                    "titleSlug": article.titleSlug
                }
                doc_ref.set(documentDict)
                html_ref = self.db.collection(
                    'html').document(article.titleSlug)
                html_ref.set({"html": article.html, "title": article.title})
            except Exception as e:
                print(e)
                print("Failed to save: {}".format(article.title))

    def getArticles(self, dateString=None, articleType=None, size=None):
        size = size if size else 10
        day = datetime.datetime.today().date() + datetime.timedelta(
            days=1) if not dateString else datetime.datetime.strptime(dateString, "%Y-%m-%d")
        articles = []
        while len(articles) < size:
            day = day + datetime.timedelta(days=-1)
            ref = self.db.collection(dateString if dateString else str(day))
            if articleType:
                ref = ref.where("type", "==", articleType)
            docs = ref.stream()
            streamCounter = 0
            for doc in docs:
                streamCounter += 1
                articles.append(doc.to_dict())
            if not streamCounter:
                print("no stream")
                break
        return articles[:size]

    def getArticle(self, titleSlug):
        ref = self.db.collection("html").document(titleSlug)
        try:
            doc = ref.get()
            return doc.to_dict()
        except:
            return None


class EconomistDB(Database):
    economist = "economist"

    def __init__(self):
        super().__init__()
        self.db = self.db.collection(self.economist)

    def save(self, articles):
        pass

    def getArticles(self, dateString=None, articleType=None):
        pass

    def getArticle(self, titleSlug):
        pass

    def dateDownloaded(self, dateString):
        ref = self.db.document(dateString)
        try:
            doc = ref.get()
            return True
        except:
            return False


if __name__ == "__main__":
    db = BloombergDB()
    articles = db.getArticles(
        size=10, articleType="OPINION", dateString="2019-01-01")
    print(len(articles))
