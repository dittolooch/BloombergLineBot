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

    def getArticles(self, dateString=None, articleType=None):
        ref = self.db.collection(dateString if dateString else str(datetime.datetime.today().date()
                                                                   ))
        if articleType:
            ref = ref.where("type", "==", articleType)
        docs = ref.stream()
        articles = []
        for doc in docs:
            articles.append(doc.to_dict())
        return articles

    def getArticle(self, titleSlug):
        ref = self.db.collection("html").document(titleSlug)
        try:
            doc = ref.get()
            return doc.to_dict()
        except:
            return None


if __name__ == "__main__":
    db = Database()
    articles = db.getArticles(str(datetime.datetime.today().date()))
    print(len(articles))
    print(len([x for x in articles if x["type"] == "opinion"]))
