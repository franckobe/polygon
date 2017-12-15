import re
import urllib3
from lxml import html

class PagesGetter:
    url = ''
    pageResult = ''
    links = {}
    title = ''
    tags = []
    badWordsList = []

    def __init__(self, url):
        self.url = url
        self.initializeBadWordsList()

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

    def initializeBadWordsList(self):
        self.badWordsList = ['je',
                             'tu',
                             'il',
                             'elle',
                             'elles',
                             'nous',
                             'vous',
                             'ils',
                             'on',
                             'un',
                             'une',
                             'de',
                             'des',
                             'le',
                             'la',
                             'les',
                             'l\'',
                             'ce',
                             'cette',
                             'ces'
                             'en',
                             'n\'',
                             'ne',
                             'mais',
                             'ou',
                             'où',
                             'et',
                             'donc',
                             'ni',
                             'car',
                             'du',
                             'or',
                             'y',
                             'pour',
                             'quand',
                             'par',
                             'à',
                             'mon',
                             'ma',
                             'mes',
                             'mien',
                             'ton',
                             'ta',
                             'tes',
                             'tien',
                             'son',
                             'sa',
                             'ses',
                             'sien',
                             'notre',
                             'nôtres',
                             'nos',
                             'votre',
                             'vôtres',
                             'vos',
                             'leur',
                             'leurs',
                             'd\'',
                             'se',
                             's\'',
                             'alors',
                             'au',
                             'aucuns',
                             'aussi',
                             'autre',
                             'avant',
                             'avec',
                             'ceux',
                             'chaque',
                             'ci',
                             'comme',
                             'comment',
                             'dans',
                             'dedans',
                             'dehors',
                             'depuis',
                             'devrait',
                             'doit',
                             'début',
                             'encore',
                             'est',
                             'eu',
                             'fait',
                             'faites',
                             'fois',
                             'font',
                             'hors',
                             'ici',
                             'juste',
                             'là',
                             'maintenant',
                             'même',
                             'parce',
                             'pas',
                             'peut',
                             'peu',
                             'plupart',
                             'pour',
                             'pourquoi',
                             'quand',
                             'que',
                             'quel',
                             'quelle',
                             'quelles',
                             'quels',
                             'qui',
                             'seulement',
                             'si',
                             'sont',
                             'soyez',
                             'sujet',
                             'sur',
                             'tandis',
                             'tellement',
                             'tels',
                             'tous',
                             'tout',
                             'trop',
                             'très',
                             'voient',
                             'vont',
                             'vu',
                             'ça',
                             'étaient',
                             'état',
                             'étions',
                             'être',
                             'a',
                             'n',
                             'd',
                             'l',
                             'm']

    def getTags(self):
        self.getTag('h1')
        self.getTag('h2')
        self.getTag('h3')
        self.getTag('h4')
        self.getTag('p')

    def getTag(self, tagName):
        i = 0
        for tag in self.pageResult.xpath("//"+tagName):
            wordsList = re.sub("[^\w]", " ", tag.text.lower()).split()
            # iterate each word
            for word in wordsList:
                # check if word is in stop words
                if word not in self.badWordsList:
                    self.tags.append({'tag': str(tagName), 'text': str(word), 'weight': str(self.getWeight(tagName))})
            i = i+1

    def getLinks(self):
        for link in self.pageResult.xpath("//a"):
            self.links[link.text] = str(link.attrib['href'])

    def getWeight(self, tagName):
        if tagName == 'h1':
            return 40
        elif tagName == 'h2':
            return 30
        elif tagName == 'h3':
            return 20
        elif tagName == 'h4':
            return 10
        elif tagName == 'p':
            return 1


toto = PagesGetter("http://footips.fr")
toto.getPage()
for tag in toto.tags:
    print(tag)
        # for word
        # print(word.tag + ' - ' + word.text + ' - ' + word.weight)

