
## Basic Setup ##


conda create --name care python=3          (or any py3 Virtual env, but must be > Python 3.6)

conda activate covid

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser --email admin@example.com --username admin

## .env usage and application

This is only needed for deployment, can be safely ignored if using local.py instead. This will require adopting a layout like:

    /var/webapps/PROJECT_NAME-DEPLOY_TYPE/DJANGO_SRC_NAME

Where the Django git repo lives as DJANGO_SRC_NAME

So to start: `git clone git@bitbucket.org:BCF_ARL/ncov19-django.git /var/webapps/<PROJECT_NAME>-<DEPLOY_TYPE>/<DJANGO_SRC_NAME>`

Next, copy the example.env up one directory from django source i.e.
`cp example.env ../.env`

Edit file .env file:

    # If this is a public facing service, set to false!*
    DEBUG=true
     # Name of our "service"
    PROJECT_NAME=covsms
    # Project directory
    DJANGO_SRC_NAME=covid
    # Abbreviated deployment type, as in staging:stg, production:prd, development:dev, quality assurance: qa
    DEPLOY_TYPE=dev 

Important vars to edit during a new deploy are:

    DEBUG, DEPLOY_TYPE, SECRET_KEY, DJANGO_DB_NAME, DJANGO_DB_USER, DJANGO_DB_PASS, DJANGO_DB_HOST, DJANGO_DB_PORT, SENTRY_DSN_URL, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

## local.py

    ## NOTE: This file has global access to everything in base.py

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = <REPLACE THIS>
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', ]

    DATABASES = {
         "default": {
             # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
             'ENGINE': 'django.db.backends.postgresql_psycopg2',
             # DB name or path to database file if using sqlite3.
             "NAME": <REPLACE THIS>,
             # Not used with sqlite3.
             "USER": <REPLACE THIS,
             # Not used with sqlite3.
             "PASSWORD": <REPLACE THIS>,
             # Set to empty string for localhost. Not used with sqlite3.
             "HOST": "localhost",
             # Set to empty string for default. Not used with sqlite3.
             "PORT": "5432",
         }
     }
    # redcap api token:
    REDCAP_TOKEN = <REPLACE THIS>

    # Twilio Settings (UA D7 currently):
    # currently we can't programatically add numbers to Notify/Messaging services,
    # so that will need to be done manually in Twilio Console.
    TWILIO_PHONE_NUMBERS = []
    TWILIO_ACCOUNT_SID = <REPLACE THIS>
    TWILIO_AUTH_TOKEN = <REPLACE THIS>
    REDCAP_TOKEN = {
        'en': '<TOKEN HERE>',
        'es': '<TOKEN HERE>',
    }	

    # Google recaptcha
    GOOGLE_RECAPTCHA_SECRET_KEY = <REPLACE THIS>


This uses an old import trick so beware, it 'loads' itself into the `/settings/__init__.py` so that base/local/dotenv can be combined into one voltron setting module.
