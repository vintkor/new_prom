from django.conf.urls import url
from catalog.views import CatalogList, CatalogDetail, CatalogSearch


urlpatterns = [
    url(r'^$', CatalogList.as_view(), name='all-catalog'),
    url(r'^search/$', CatalogSearch.as_view(), name='search-catalog'),
    url(r'^(?P<pk>\d+)$', CatalogDetail.as_view(), name='single-product'),
]