import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from lxml import html


class PagesGetter:
    url = ''
    pr = ''
    links = {}
    title = ''
    tags = []
    bwl = []

    def __init__(self, url):
        self.url = url
        self.initializeBadWordsList()

    def getPage(self):
        http = urllib3.PoolManager()
        r = http.request('GET', self.url)
        if r.status == 200:
            self.pr = r.data
            self.pr = html.fromstring(self.pr)
            self.getLinks()
            self.getTags()

    def initializeBadWordsList(self):
        self.bwl = ['je',
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
                    'ces',
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
                    'm',
                    'c',
                    's',
                    'ces']

    def getTags(self):
        self.getTag('h1')
        self.getTag('h2')
        self.getTag('h3')
        self.getTag('h4')
        self.getTag('p')

    def getTag(self, tagName):
        for tag in self.pr.xpath("//" + tagName):
            txt = str(tag.text)
            wl = re.sub("[^\w]", " ", txt.lower()).split()
            # iterate each word
            for word in wl:
                # check if word is in stop words
                if word not in self.bwl:
                    #check if already exist, if yes, we add weight
                    j = self.getWordIndex(word)
                    if j == -1:
                        self.tags.append({'text': str(word), 'weight': str(self.getWeight(tagName))})
                    else:
                        self.tags[j]['weight'] = str(int(self.tags[j]['weight']) + int(self.getWeight(tagName)))

    def getWordIndex(self, word):
        for i in range(len(self.tags)):
            if self.tags[i]['text'] == word:
                return i
        return -1

    def getLinks(self):
        for link in self.pr.xpath("//a"):
            if "href" in link.attrib:
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