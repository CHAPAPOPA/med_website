from django import template

register = template.Library()


@register.filter()
def mediapath(values):
    if values:
        return f"/media/{values}"


@register.simple_tag
def mediapath(values):
    if values:
        return f"/media/{values}"
