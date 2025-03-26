import random
from urllib.parse import urlencode

from django import template

register = template.Library()

@register.filter
def random_choice(value):
    return random.choice(value) if value else None

@register.simple_tag
def range_list(start, end):
    return list(range(start, end + 1))

@register.simple_tag(takes_context=True)
def querystring(context, key, value):
    """Modifies query parameters while keeping existing ones."""
    request = context['request']
    query_params = request.GET.copy()
    query_params[key] = '-' + value if key in query_params and query_params[key] == value else value
    return urlencode(query_params)

@register.simple_tag(takes_context=True)
def sort_indicator(context, key):
    """
    Returns ▲ for ascending and ▼ for descending based on the current ordering.
    """
    request = context['request']
    sorted_field = request.GET.get('ordering')
    if not sorted_field or key not in sorted_field:
        return ""
    elif sorted_field.startswith('-'):
        return "▼"
    else:
        return "▲"
