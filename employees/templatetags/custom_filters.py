import random
from django import template

register = template.Library()

@register.filter
def random_choice(value):
    return random.choice(value) if value else None

@register.simple_tag
def range_list(start, end):
    return list(range(start, end + 1))
