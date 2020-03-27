import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
SECRET = "/BloombergLineBot/Crawler/secret.json" if os.uname()[
    0] != "Darwin" else "/Users/warrencheng/BloombergLineBot/Crawler/secret.json"


class Database:
    def __init__(self):
        cred = credentials.Certificate(SECRET)
        firebase_admin.initialize_app(cred, {
            'projectId': "bloomberglinebot",
        })

        self.db = firestore.client()

    def save(self, articles):
        for article in articles:
            try:
                doc_ref = self.db.collection(
                    article.publishTime).document(article.title)
                documentDict = {
                    "time": article.publishTime,
                    "content": article.paragraphs,
                    "url": article.cleanUrl,
                    "type": article.contentType
                }
                doc_ref.set(documentDict)
            except:
                print(article.title)

    def getArticles(self, dateString=None, articleType=None):
        ref = self.db.collection(dateString if dateString else str(datetime.datetime.today().date()
                                                                   ))
        if articleType == "news":
            ref = ref.where("type", "==", "news")
        elif articleType == "opinion":
            ref = ref.where("type", "==", "opinion")
        docs = ref.stream()
        articles = []
        for doc in docs:
            articles.append(doc.to_dict())
        return articles


if __name__ == "__main__":
    db = Database()
    articles = db.getArticles(str(datetime.datetime.today().date()))
    print(len(articles))
    print(len([x for x in articles if x["type"] == "opinion"]))
