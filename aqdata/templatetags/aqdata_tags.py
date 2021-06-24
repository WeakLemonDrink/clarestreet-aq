import os
from functools import lru_cache

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from aqdata.helpers import load_json_from_file


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


@lru_cache()
def colour_map_json(reading):
    '''
    Loads dictionary mapping values to rgb colours and stores in memory for further use
    '''
    if reading == 'humidity':
        file_name = 'humidity_colour_map.json'
    elif reading == 'temperature':
        file_name = 'temp_colour_map.json'

    return load_json_from_file(os.path.join(settings.BASE_DIR, 'doc', file_name))


@register.simple_tag
def colour_map(reading, value):
    '''
    Loads a colour map from json based on the input `reading` and returns a rgb colour mapped to
    the nearest `value`
    '''
    return_str = ''

    if isinstance(value, (int, float)):
        # Load the map values from the json file
        map_dict = colour_map_json(reading)

        # Find the nearest value to the options available in the map
        keys = [int(key) for key in map_dict.keys()]
        nearest_value = min(keys, key=lambda x:abs(x - value))

        # Make value str for searching through dict and then return the mapped value
        rgb_values = map_dict.get(str(nearest_value), None)

        if rgb_values:
            text_colour_rgb = rgb_values.get('color', None)

            # Only apply style to text colour if it exists
            if text_colour_rgb:
                return_str += f'color: {text_colour_rgb};'

    return mark_safe(return_str)
