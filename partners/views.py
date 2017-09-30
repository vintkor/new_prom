from django.shortcuts import render
from partners.models import Provider, Branch, File
from catalog.models import Product, Delivery


def get_providers(request):
    if request.is_ajax():
        product_id = request.GET.get('product')
        region_id = int(request.GET.get('region'))

        product = Product.objects.get(id=int(product_id))
        branches = Branch.objects.filter(delivery__product=product, region_for_work=region_id).select_related('parent_provider')
        context = {
            'branches': branches,
            'region': region_id,
            'product_id': product_id,
        }
        return render(request, 'providers.html', context)


def get_branch(request):
    if request.is_ajax():
        product_id = int(request.GET.get('product'))
        branch_id = int(request.GET.get('branch'))

        delivery = Delivery.objects.get(product_id=product_id, branch_id=branch_id)
        branch = Branch.objects.get(id=branch_id)
        prices = File.objects.filter(provider__branch=branch)

        context = {
            'branch': branch,
            'deliveries': product_id,
            'delivery': delivery,
            'prices': prices,
        }
        return render(request, 'branch.html', context)
