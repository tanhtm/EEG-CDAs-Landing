from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from whiteneuron.base.sites import base_admin_site
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap


urlpatterns = []

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
else:
    # In production, static files are served by whitenoise
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
        path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
    ]

# Define base urlpatterns
urlpatterns += [
    path("", include("whiteneuron.base.urls")),
    path("", include("apps.sites.urls")),
]

if settings.UNFOLD['SHOW_LANGUAGES']:
    urlpatterns += [
        path("i18n/", include("django.conf.urls.i18n")),
        path("admin", base_admin_site.urls),
    ]
else:
    urlpatterns += [
        path("admin", base_admin_site.urls),
    ]