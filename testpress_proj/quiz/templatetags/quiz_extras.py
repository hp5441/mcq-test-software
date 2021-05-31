from django import template
from django.utils.safestring import mark_safe

import json

register = template.Library()


@register.filter(name='addstr')
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))
