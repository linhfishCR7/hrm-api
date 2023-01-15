from django import template


register = template.Library()


@register.filter()
def divide(n1, n2):
    try:
        return n1 / n2
    except ZeroDivisionError:
        return None


@register.filter()
def percentof(amount, total):
    try:
        if not total or not amount:
            return None
        return '{:.1f}%'.format(amount / total * 100)
    except ZeroDivisionError:
        return None
