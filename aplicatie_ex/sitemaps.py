from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Mancare

class MancareSitemap(Sitemap):
    # Frecventa de modificare (ex: daily, weekly)
    changefreq = "monthly"  
    # Prioritatea (1.0 = cea mai mare)
    priority = 0.8        

    def items(self):
        # Returneaza obiectele care vor fi incluse in sitemap
        return Mancare.objects.all()

    def lastmod(self, obj):
        # Returneaza data ultimei modificari pentru fiecare obiect
        return obj.actualizat_la


class VederiStaticeSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        # Numele view-urilor statice
        return ['afisare_main', 'aboutus', 'contact']

    def location(self, item):
        # Returneaza URL-ul pentru fiecare item
        # Atentie, acestea trebuie sa aiba name specificat in urls.py
        return reverse(item)

