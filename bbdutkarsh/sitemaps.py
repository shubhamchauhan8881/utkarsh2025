from django.contrib.sitemaps import Sitemap
from django.contrib import sitemaps
from django.urls import reverse



class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = "never"

    def items(self):
        return ["homepage"]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    # def items(self):
    #     return Entry.objects.filter(is_draft=False)

    # def lastmod(self, obj):
    #     return obj.pub_date