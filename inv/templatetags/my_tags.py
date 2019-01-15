from django import template
register = template.Library()


@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name


@register.filter
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural


@register.simple_tag
def increase(val, inc):
    val = val + inc
    return val


@register.filter(is_safe=True)
def doc_name(obj):
    return obj._meta.model.__name__.lower()[3:]


@register.filter()
def doc_str(obj):
    return str(obj)
