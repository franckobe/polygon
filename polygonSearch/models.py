from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from lxml import html

'''
python manage.py makemigrations
python manage.py migrate

si migrate ne fonctionne pas : 
- Vider la table django_migrations
- Supprimer le dossier migrations
- Executer le makemigrations
- python manage.py migrate --fake-initial
'''


class Website_domain(models.Model):
    id_website_domain = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    is_allowed = models.IntegerField(default=-1)
    id_owner = models.ForeignKey('Website_owner', on_delete=models.CASCADE, default=-1)


class Website_word(models.Model):
    id_website_word = models.AutoField(primary_key=True)
    word = models.CharField(max_length=50)
    weight = models.IntegerField(default=1)
    url = models.CharField(max_length=255)
    id_website_page = models.ForeignKey('Website_page', on_delete=models.CASCADE, null=True)


class Website_page(models.Model):
    id_website_page = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=50)
    content = models.TextField
    id_website_domain = models.ForeignKey('Website_domain', on_delete=models.CASCADE)


class Website_category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name_category = models.CharField(max_length=50)


class Domain_category_website:
    id_category = models.ForeignKey('Website_category', primary_key=True, on_delete=models.SET_NULL, null=True)
    id_website_domain = models.ForeignKey('Website_domain', primary_key=True, on_delete=models.SET_NULL, null=True)


class Website_owner(models.Model):
    id_owner = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)


class Search_history(models.Model):
    id_search_history = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    id_website_page = models.ForeignKey('Website_page', on_delete=models.CASCADE)
    id_website_word = models.ForeignKey('Website_word', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


# This code is triggered whenever a new user has been created and saved​
# Create a token on user's creation.
# authenticate view
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


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
                href = str(link.attrib['href'])
                if not href[0] == '#':
                    # reformating links
                    #if link begins by /x we add it to the domain name
                    url = str(self.url)
                    if href[0] == '/':
                        p = re.compile('^(https?:\/\/)?([\da-z\.-]+)')
                        c = p.findall(url)
                        d = str(c[0][0] + c[0][1])
                        self.links[link.text] = d + str(link.attrib['href'])
                        # if link begins by www, http:// we keep it
                    else:
                        self.links[link.text] = link.attrib['href']

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
