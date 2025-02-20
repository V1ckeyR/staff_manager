import random
from django import template

register = template.Library()

@register.filter
def random_choice(value):
    return random.choice(value) if value else None
