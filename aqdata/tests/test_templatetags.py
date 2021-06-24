import pytest

from aqdata.templatetags import aqdata_tags


class TestShowTrend:
    '''
    Tests for the `show_trend` template tag
    '''
    @pytest.mark.parametrize(
        'test_input,expected',
        [
            (1, 'Rising'),
            (0, 'Flat'),
            (-1, 'Falling'),
        ]
    )
    def test_returns_correct_html(self, client, test_input, expected):
        '''
        `show_trend` tag should translate input 1, 0 or -1 into a upwards arrow, nothing or
        downwards arrow to should that readings are rising, flat or falling
        '''
        return_html_str = aqdata_tags.show_trend(test_input)

        assert expected in return_html_str


class TestTempColourMap:
    '''
    Tests for the `temp_colour_map` template tag
    '''
    @pytest.mark.parametrize(
        'test_input,expected',
        [
            (-30.501, ''),  # Robustness for large -tve value
            (-30.000, 'color: rgb(14, 14, 21);'),
            (-29.999, 'color: rgb(14, 14, 21);'),
            (0.000, 'color: rgb(247, 249, 252);'),
            (None, ''),  # Robustness for `None`
            ('my string', ''),  # Robustness for a string
            (1, 'color: rgb(255, 250, 234);'),  # Robustness for integer
            (9.499, 'color: rgb(254, 218, 109);'),
            (9.501, 'color: rgb(254, 215, 102);'),
            (10.000, 'color: rgb(254, 215, 102);'),
            (10.501, 'color: rgb(254, 210, 99);'),
            (49.999, 'color: rgb(33, 11, 16);'),
            (50.000, 'color: rgb(33, 11, 16);'),
            (50.501, ''),  # Robustness for large +tve value
        ]
    )
    def test_function_returns_correct_temp_map_colour(self, test_input, expected):
        '''
        `temp_colour_map` tag should return a rgb to use to colour the temp reading based on the
        temperature value
        Normal values
        '''
        assert aqdata_tags.temp_colour_map(test_input) == expected
