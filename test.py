import urllib3
from lxml import html

class PagesGetter:
    url = ''
    pageResult = ''
    links = []
    title = ''
    tags = []

    def __init__(self, url):
        self.url = url

    def getPage(self):
        http = urllib3.PoolManager()
        r = http.request('GET', self.url)
        if r.status == 200:
            self.pageResult = r.data
            self.pageResult = html.fromstring(self.pageResult)
            self.getLinks()
            self.getTags()

    def removeBadWords(self):
        print("aa")

    def getTags(self):
        self.getTag('h1')
        self.getTag('h2')
        self.getTag('h3')

    def getTag(self, tag):
        i = 0
        for tag in self.pageResult.xpath("//"+tag):
            self.tags[tag + i] = str(tag.text)
            i = i+1

    def getLinks(self):
        for link in self.pageResult.xpath("//a"):
            self.links[link.text] = str(link.get("href"))


toto = PagesGetter("http://footips.fr")
toto.getPage()
