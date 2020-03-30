class Article:
    def __init__(self, url=None, parser=None):
        self.parser = parser
        self.url = url
        self.splitUrl = url.split("/")
        self.bbgLogo = "https://user-images.githubusercontent.com/44837996/77818163-3f5f2380-710b-11ea-80c4-f3dbf9344c45.jpg"

    @property
    def imageSource(self):
        imageClass = self.parser.find("div", class_="image")
        videoClass = self.parser.find("div", class_="video_player")
        url = None
        if imageClass:
            url = imageClass.find("img")["src"]
        elif videoClass:
            url = imageClass.find("img")["src"]
        if url:
            urlSplit = url.split("/")
            urlSplit[-1] = "600x-1.jpg"
            url = "/".join(urlSplit)
        return url if url else self.bbgLogo

    @property
    def html(self):
        return str(self.parser)

    @property
    def cleanUrl(self):
        questionMarkIndex = self.url.index("?")
        return self.url[:questionMarkIndex]

    @property
    def title(self):
        return self.parser.find("h1").contents[0]

    @property
    def titleSlug(self):
        return self.cleanUrl.split("/")[-1]

    @property
    def paragraphs(self):
        try:
            return self._paragraphs
        except:
            pTags = self.parser.find("div", class_="body-columns").findAll("p")
            self._paragraphs = "\n\n".join([tag.get_text() for tag in pTags])
            return self._paragraphs

    @property
    def contentType(self):
        return self.splitUrl[1].upper()

    @property
    def publishTime(self):
        return self.splitUrl[3]
