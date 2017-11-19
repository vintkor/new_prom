from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from catalog.models import Product, Feature, Category
from partners.models import Region
from xlsxwriter import Workbook
from django.http import HttpResponse


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


class CatalogForPromXLSX(View):

    def get(self, request):
        queryset = Product.objects.select_related('category', 'unit').filter(active=True)
        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment; filename="prom.xlsx"'

        workbook = Workbook(response)
        worksheet = workbook.add_worksheet('Export Products Sheet')
        worksheet_2 = workbook.add_worksheet('Export Groups Sheet')

        header = (
            'Название_позиции',
            'Ключевые_слова',
            'Описание',
            'Тип_товара',
            'Цена',
            'Валюта',
            'Единица_измерения',
            'Ссылка_изображения',
            'Наличие',
            'Идентификатор_товара',
            'Идентификатор_группы',
            'Код_товара',
            'Номер_группы',
        )

        [worksheet.write(0, col, i) for col, i in enumerate(header)]

        for row, item in enumerate(queryset):
            worksheet.write(row + 1, 0, item.title)
            worksheet.write(row + 1, 1, item.category.title)
            worksheet.write(row + 1, 2, item.text.replace(chr(13), '').replace(chr(10), '').replace(
                'src="/media/uploads/', 'src="http://{}/media/uploads/'.format(self.request.META.get('HTTP_HOST'))))
            worksheet.write(row + 1, 3, 'r')
            worksheet.write(row + 1, 4, item.get_price_UAH())
            worksheet.write(row + 1, 5, item.get_currency_code())
            worksheet.write(row + 1, 6, item.get_unit())
            worksheet.write(row + 1, 7, '{}'.format(
                ''.join(['http://{}{}, '.format(request.META.get('HTTP_HOST'), img) for img in item.get_all_photo()])
            ))
            worksheet.write(row + 1, 8, '+')
            worksheet.write(row + 1, 9, item.code)
            worksheet.write(row + 1, 10, item.category.id)
            worksheet.write(row + 1, 11, item.code)
            worksheet.write(row + 1, 12, item.category.id)

        header_2 = (
            'Номер_группы',
            'Название_группы',
            'Идентификатор_группы',
            'Номер_родителя',
            'Идентификатор_родителя',
        )

        [worksheet_2.write(0, col, i) for col, i in enumerate(header_2)]

        for row, item in enumerate(Category.objects.all()):
            worksheet_2.write(row + 1, 0, item.id)
            worksheet_2.write(row + 1, 1, item.title)
            worksheet_2.write(row + 1, 2, item.id)
            worksheet_2.write(row + 1, 3, item.get_id())
            worksheet_2.write(row + 1, 4, item.get_id())

        return response
