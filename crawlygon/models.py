import re
import urllib3
from django.db import models
from lxml import html
from django.utils.timezone import now

# Create your models here.
from polygonSearch.models import Website_domain, Website_page, Website_word, Website_link_to_visit, Website_owner

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PagesGetter:
    # url of the page
    url = ''
    # page results (content of the page)
    pr = ''
    # list of links
    links = []
    # title of the page
    title = ''
    # all weighted tags with words
    tags = []
    # bad words (not taken in list)
    bwl = []
    # the name of the domaine IE www.toto.com
    domainName = ''
    #author of the page
    author = ''


    def __init__(self, url):
        self.url = url
        # fills bad words array
        self.initializeBadWordsList()
        # get the page + fills tags, title and links
        self.getPage()
        self.saveThis()

    def saveThis(self):
        # saving author
        own = Website_owner(name=self.author, type='zob')
        try:
            own.save()
            own = Website_owner.objects.last()
        except:
            own = Website_owner.objects.get(name=self.author)

        # saving domains
        dom = Website_domain(name=self.domainName, is_allowed=1, id_owner_id=own.id_owner)
        try:
            dom.save()
            dom = Website_domain.objects.last()
        except:
            dom = Website_domain.objects.get(name=self.domainName)
        # saving pages
        page = Website_page(url=self.url, title=self.title, id_website_domain_id=dom.id_website_domain)
        try:
            page.save()
        except:
            #todo : en fait vérifier la date !!
            exit()
        page = Website_page.objects.last()
        # saving words + weights
        for tag in self.tags:
            ws = Website_word(word=tag.get('text'), weight=tag.get('weight'), url=self.url, id_website_page_id=page.id_website_page)
            ws.save()
        # saving links
        for link in self.links:
            li = Website_link_to_visit(url=link)
            try:
                li.save()
            except:
                pass

    def getPage(self):
        http = urllib3.PoolManager()
        r = http.request('GET', self.url)
        if r.status == 200:
            # todo : check if the meta robots is noodp
            self.getDomain()
            self.pr = r.data
            self.pr = html.fromstring(self.pr)
            self.getMeta()
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
            # only get words
            wl = re.sub("[^\w]", " ", txt.lower()).split()
            # iterate each word
            for word in wl:
                # check if word is in stop words
                if word not in self.bwl:
                    # check if already exist, if yes, we add weight
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
                if len(link.attrib['href']) > 0:
                    href = str(link.attrib['href'])
                    if not href[0] == '#':
                        # reformating links
                        # if link begins by /x we add it to the domain name
                        if href[0] == '/':
                            self.links.append(self.domainName + str(link.attrib['href']))
                            # if link begins by www, http:// we keep it
                        else:
                            self.links.append(link.attrib['href'])

    def getMeta(self):
        for meta in self.pr.xpath("//meta"):
            author = ''
            name = ''
            if "name" in meta.attrib:
                name = str(meta.attrib['name'])
                if name.lower() == "robots":
                    content = str(meta.attrib['content'])
                    #todo : gérer le cas du nofollow
                    if not content.lower().find('noindex') == -1:
                        exit()
                if name.lower() == "author":
                    author = str(meta.attrib['author'])
                    author = author.lower()
            self.author = author

    def getDomain(self):
        p = re.compile('^(https?:\/\/)?([\da-z\.-]+)')
        c = p.findall(self.url)
        self.domainName = str(c[0][0] + c[0][1])

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


class CrawlerInstructor:
    iterations = 200

    def __init__(self, nbIterations):
        self.iterations = nbIterations
        self.crawl()

    def crawl(self):
        # select the number of self.iterations of links to visit
        ltv = Website_link_to_visit.objects.all().filter(visited_at__isnull=True)[:self.iterations]

        for link in ltv:
            # Update the time
            link.visited_at = now()
            link.save()
            pg = PagesGetter(link.url)