from django.conf.urls import url
from catalog.views import CatalogList, CatalogDetail, CatalogSearch, CatalogForPromXLSX, CatalogCategoryList


urlpatterns = [
    url(r'^$', CatalogList.as_view(), name='all-catalog'),
    url(r'^search/$', CatalogSearch.as_view(), name='search-catalog'),
    url(r'^(?P<pk>\d+)$', CatalogDetail.as_view(), name='single-product'),
    url(r'^category/(?P<pk>\d+)$', CatalogCategoryList.as_view(), name='category'),
    url(r'^prom-xlsx/$', CatalogForPromXLSX.as_view(), name='catalog-prom'),
]