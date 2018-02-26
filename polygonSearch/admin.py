from django.contrib import admin

# Register your models here.
from polygonSearch.models import Website_link_to_visit, Search_history, Website_owner, Domain_category_website, \
    Website_category, Website_page, Website_word, Website_domain

admin.site.register(Website_domain)
admin.site.register(Website_word)
admin.site.register(Website_page)
admin.site.register(Website_category)
admin.site.register(Website_owner)
admin.site.register(Search_history)
admin.site.register(Website_link_to_visit)
