# Script upload latest tagged version to Heroku and writes tag info to env vars
latest_tag_str=$(git describe --tags --abbrev=0)
latest_tag_date_str=$(git log -1 --format=%ai $latest_tag_str)

# Push latest master commit to heroku
git push heroku master

# Run any new migrations
heroku run python manage.py migrate --settings settings.production

# Set vars from .env file except DJANGO_SETTINGS_MODULE
heroku config:set APP_VERSION=$latest_tag_str
heroku config:set APP_LAST_UPDATE=$latest_tag_date_str
heroku config:set $(grep -v 'DJANGO_SETTINGS_MODULE' .env | xargs)
