# setting.py
   
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', ]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'EDIT ME BEFORE PRODUCTION'
# Twilio Settings (UA D7 currently):
# currently we can't programatically add numbers to Notify/Messaging services,
# so that will need to be done manually in Twilio Console.
# TWILIO_PHONE_NUMBERS = []
# TWILIO_ACCOUNT_SID = <REPLACE THIS>
# TWILIO_AUTH_TOKEN = <REPLACE THIS>