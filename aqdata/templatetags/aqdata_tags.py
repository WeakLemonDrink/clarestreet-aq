from django import template
from django.utils.safestring import mark_safe


register = template.Library()


def set_text_colour(warning_threshold, danger_threshold, value):
    '''
    Sets the bootstrap class to `text-success` (green), `text-warning` (orange) or `text-danger`
    (red) depending on input thresholds
    '''
    if value < warning_threshold:
        text_class = 'text-success'
    elif warning_threshold <= value <= danger_threshold:
        text_class = 'text-warning'
    else:
        text_class = 'text-danger'

    return text_class


@register.simple_tag
def p1_colour_limit(value):
    '''
    Sets the bootstrap text class depending on PM 10 limits
    warning_threshold = 20.0
    danger_threshold = 40.0
    '''
    return set_text_colour(20.0, 40.0, value)


@register.simple_tag
def p2_colour_limit(value):
    '''
    Sets the bootstrap text class depending on PM 2.5 limits
    warning_threshold = 10.0
    danger_threshold = 20.0
    '''
    return set_text_colour(10.0, 20.0, value)


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
