from django.conf.urls import url
from catalog.views import CatalogList, CatalogDetail


urlpatterns = [
    url(r'^$', CatalogList.as_view(), name='all-catalog'),
    url(r'^(?P<pk>\d+)$', CatalogDetail.as_view(), name='single-product'),
]