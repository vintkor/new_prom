from django.conf.urls import url
from partners.views import get_providers, get_branch


urlpatterns = [
    url(r'^providers/$', get_providers, name='ajax-get-providers'),
    url(r'^branch/$', get_branch, name='ajax-get-branch'),
]
