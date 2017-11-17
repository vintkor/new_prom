from django.shortcuts import render
from django.views.generic import ListView, DetailView
from catalog.models import Product, Feature
from partners.models import Region


def index(request):
    context = {'page_name': 'home'}
    return render(request, 'index.html', context)


class CatalogList(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'all-products.html'
    paginate_by = 50

    def get_queryset(self, **kwargs):
        queryset = Product.objects.prefetch_related('delivery_set').select_related(
            'category', 'currency').filter(active=True)
        return queryset


class CatalogDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'single-product.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogDetail, self).get_context_data(**kwargs)
        context['features'] = Feature.objects.filter(product=self.object)
        regions = set(Region.objects.filter(Regions__delivery__product=self.object).order_by('title'))
        context['regions'] = regions

        return context


class CatalogSearch(CatalogList):

    def get_queryset(self):
        return Product.objects.filter(code__icontains=self.request.GET.get('code'))
