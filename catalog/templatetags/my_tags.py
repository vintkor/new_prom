from django import template


register = template.Library()


@register.inclusion_tag('_breadcrumbs.html')
def breadcrumbs(category, product_title):
    pages = category.get_ancestors(ascending=False, include_self=True)
    return {'pages': pages, 'product': product_title}
