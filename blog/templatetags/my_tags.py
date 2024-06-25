from django import template

register = template.Library()


# Создание тега
@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"
