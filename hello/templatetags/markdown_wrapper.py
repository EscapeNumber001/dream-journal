from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(is_safe=True)
def markdown2html(value):
    return mark_safe(markdown.markdown(value))