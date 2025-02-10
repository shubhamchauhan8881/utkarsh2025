from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from . import sitemaps
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    "static": sitemaps.StaticViewSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('old', include("website.urls")),
    path('', include("app.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    )

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)