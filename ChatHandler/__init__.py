import linebot.models as models
from Crawler.Database import Database

db = Database()


class PostbackIntent:
    GET_NEWS = "News"
    GET_OPINIONS = "Opinion"


class ChatHandler:
    UNSUPPORTED_MESSAGE = "Your device does not support chatbots..."

    def __init__(self, db):
        self.db = db
        self.api_url = "https://timmy.rent/api"

    def getButtonsTemplateForNewsTypeSelection(self):
        actions = [
            models.PostbackAction(label=PostbackIntent.GET_NEWS,
                                  data=PostbackIntent.GET_NEWS, display_text=PostbackIntent.GET_NEWS),
            models.PostbackAction(label=PostbackIntent.GET_OPINIONS,
                                  data=PostbackIntent.GET_OPINIONS, display_text=PostbackIntent.GET_OPINIONS)
        ]
        return models.ButtonsTemplate(text="What do you want to read?", title="From Bloomberg.com", actions=actions)

    def getCarouselTemplateFor(self, articles):
        columns = []
        for article in articles:
            destinationUrl = self.api_url + article.cleanUrl
            action = models.URIAction(
                label="Read It", uri=destinationUrl, alt_uri=destinationUrl)
            columns.append(models.CarouselColumn(text=article.title, title=article.title,
                                                 thumbnail_image_url=article.imageSource, actions=[action]))
        carousel = models.CarouselTemplate(
            columns=columns, image_aspect_ratio="rectangle", image_size="cover")
        return carousel

    def handleMessageText(self, api, event):
        api.reply_message(
            event.reply_token,
            # TextSendMessage(text=articles),
            models.TemplateSendMessage(alt_text=self.UNSUPPORTED_MESSAGE,
                                       template=self.getButtonsTemplateForNewsTypeSelection())
        )

    def handlePostback(self, api, event):
        if event.postback.data in [PostbackIntent.GET_OPINIONS, PostbackIntent.GET_NEWS]:
            articles = self.db.getArticles(
                articleType=event.postback.data)[:10]
            api.reply_message(
                event.reply_token, models.TemplateSendMessage(
                    alt_text=self.UNSUPPORTED_MESSAGE, template=self.getCarouselTemplateFor(articles))
            )
