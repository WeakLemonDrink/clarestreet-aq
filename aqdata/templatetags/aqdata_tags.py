from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def show_trend(trend):
    '''
    If `trend` is 1 (rising), show up arrow
    If `trend` is 0 (flat), show nothing
    If `trend` is -1 (falling), show down arrow
    '''
    if trend > 0:
        icon = '&uarr;'
        tooltip = 'Rising'
    elif trend < 0:
        icon = '&darr;'
        tooltip = 'Falling'
    else:
        icon = ''
        tooltip= 'Flat'

    return_str = f'<span data-toggle="tooltip" data-placement="top" title="{tooltip}">{icon}</span>'

    return mark_safe(return_str)
