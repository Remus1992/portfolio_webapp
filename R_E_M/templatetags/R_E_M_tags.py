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


@register.simple_tag
def movie_pdf_or_default(movie):
    if movie.movie_script:
        return mark_safe(
            '<object class ="script" data="{}" ><p>Your web browser doesn \'t have a PDF plugin. Instead you can <a href = "{}"> click here to download the PDF file.</a></p></object>'.format(
                movie.movie_script.url, movie.movie_script.url))
    return mark_safe('<div style="display:none"></div>')
