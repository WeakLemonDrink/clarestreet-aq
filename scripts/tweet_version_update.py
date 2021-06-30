from django.conf import settings

import tweepy


def run():
    '''
    Posts a update status to @AirBs5 to publicise the web app has been updated

    Run using the django-extensions `runscript` command
    '''
    # Perform authentication
    auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    # Construct the status
    status_str = (
        'air-bs5 ' + settings.APP_VERSION + ' has been released! Check out'
        ' ' + settings.BASE_URL + ' for live air quality readings in Bristol BS5. #AirQuality'
        ' #AirPollution #Bristol'
    )

    # Post the status update to twitter
    api.update_status(status_str)
