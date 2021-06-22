import pytest

from aqdata.templatetags.aqdata_tags import show_trend


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
        return_html_str = show_trend(test_input)

        assert expected in return_html_str
