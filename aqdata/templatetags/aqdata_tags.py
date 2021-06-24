import json
import os
from functools import cache

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe


register = template.Library()


def set_text_colour(warning_threshold, danger_threshold, value):
    '''
    Sets the bootstrap class to `text-success` (green), `text-warning` (orange) or `text-danger`
    (red) depending on input thresholds
    '''
    if isinstance(value, float):
        if value < warning_threshold:
            text_class = 'text-success'
        elif warning_threshold <= value <= danger_threshold:
            text_class = 'text-warning'
        else:
            text_class = 'text-danger'
    else:
        # If not a float suitable for comparison, just set the text_class to a default
        text_class = 'text-body'

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


@cache
def temp_colour_map_json():
    '''
    Loads dictionary mapping temperature values to rgb colours and stores in memory for further
    use
    '''
    with open(os.path.join(settings.BASE_DIR, 'doc', 'temp_colour_map.json')) as f: # pylint:disable=invalid-name
        return json.load(f)


@register.simple_tag
def temp_colour_map(value):
    '''
    Return a rgb colour based on the input temperature `value`
    '''
    # Load the map values from the json file
    colour_map = temp_colour_map_json()
    return_str = ''

    if value is not None:
        # Round the input float to an int
        value = int(round(value))

        # Make value str for searching through valid dict and then returned the mapped value
        rgb_values = colour_map.get(str(value), None)

        if rgb_values:
            bg_colour_rgb = rgb_values.get('background-color', None)
            text_colour_rgb = rgb_values.get('color', None)

            # Build the return string
            if bg_colour_rgb:
                return_str += f'background-color: {bg_colour_rgb};'

            # Only apply style to text colour if it is necessary (i.e the background colour clashes with
            # the default black text used on the rest of the site)
            if text_colour_rgb:
                return_str += f' color: {text_colour_rgb};'

    return mark_safe(return_str)
