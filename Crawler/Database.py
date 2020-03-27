import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Database:
    def __init__(self):
        cred = credentials.Certificate('./secret.json')
        firebase_admin.initialize_app(cred, {
            'projectId': "bloomberglinebot",
        })

        self.db = firestore.client()

    def save(self, articles):
        for article in articles:
            try:
                doc_ref = self.db.collection("article").document(article.title)
                doc_ref.set({
                    "time": article.publishTime,
                    "content": article.paragraphs
                })
            except:
                print(article.title)

    def getArticles(self):
        ref = self.db.collection('article')
        docs = ref.stream()
        articles = []
        for doc in docs:
            articles.append(doc.id)
        return articles


if __name__ == "__main__":
    db = Database()
    articles = db.getArticles()
    print(articles)
