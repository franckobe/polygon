import re
import urllib3
from lxml import html

from polygonSearch.models import PagesGetter

toto = PagesGetter("http://footips.fr")
print(toto.links)

