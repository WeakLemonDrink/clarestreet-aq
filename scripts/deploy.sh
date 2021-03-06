# Script upload latest tagged version to Heroku and writes tag info to env vars
latest_tag_str=$(git describe --tags --abbrev=0)
latest_tag_date_str=$(git log -1 --format=%ai $latest_tag_str)

# Push latest master commit to heroku
git push heroku master

# Run any new migrations
heroku run python manage.py migrate

# Set vars from .env file except DJANGO_SETTINGS_MODULE
heroku config:set APP_VERSION=$latest_tag_str APP_LAST_UPDATE="$latest_tag_date_str" $(grep -v 'DJANGO_SETTINGS_MODULE' .env | xargs)

# Run script to tweet a new version has been released
heroku run python manage.py runscript tweet_version_update
