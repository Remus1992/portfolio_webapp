from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def blog_image_or_default(blog):
    if blog.image:
        return mark_safe(
            '<img src="{}" class="blog_image" alt="{}">'.format(blog.image.url, blog.alt_text))
    return mark_safe('<img src="{}" class="blog_image" alt="Placeholder Image">'.format(
        '/static/R_E_M/img/generic.jpg'))