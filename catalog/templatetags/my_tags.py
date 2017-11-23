from django import template


register = template.Library()


@register.inclusion_tag('_breadcrumbs.html')
def breadcrumbs(category, product_title=False):
    pages = [i for i in category.get_ancestors(ascending=False, include_self=True)]
    context = dict()

    if product_title:
        context['pages'] = pages
        context['product'] = product_title
    else:
        context['pages'] = pages[:-1]
        context['product'] = pages[-1]

    return context
