from django import template
from catalog.models import Category


register = template.Library()


@register.inclusion_tag('_breadcrumbs.html')
def business_part_nav(category_id):
    node = Category.objects.get(id=category_id)
    pages = node.get_ancestors(ascending=False, include_self=True)
    return {'pages': pages}
