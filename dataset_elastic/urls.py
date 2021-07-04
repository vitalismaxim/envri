from django.conf.urls import url,include
from dataset_elastic import views,models
from DSSaaS import settings
from django.conf.urls.static import static


urlpatterns = [
	#url(r'^index', views.index, name='index'),
    url(r'^home', views.home, name='home'),
    url(r'^result', views.home, name='result'),
    url(r'^search', views.search_index, name='search_index'),
    url(r'^rest', views.rest, name='rest')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)