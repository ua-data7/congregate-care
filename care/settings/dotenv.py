import os
import sys

from dotenv import load_dotenv

from . import SETTINGS_DIR

DOTENV_FILE = SETTINGS_DIR.parents[2] / '.env'
ENV_IMPORTED = False
__all__ = ['ENV_IMPORTED']
# print(f"->{DOTENV_FILE}")
if(os.path.exists(DOTENV_FILE)):
    ENV_IMPORTED = True
    load_dotenv(verbose=True, dotenv_path=DOTENV_FILE)
    import_vars = [
        'DEBUG', 'PROJECT_NAME', 'DJANGO_SRC_NAME', 'DEPLOY_TYPE', 'WEBAPP_ROOT',
        'VARWWW_ROOT', 'PROJECT_WWW', 'BACKUP_ROOT', 'PRIVATE_ROOT', 'PROJECT_DATA',
        'PROJECT_ROOT', 'DJANGO_PROJECT_ROOT', 'DJANGO_SETTINGS_MODULE',
        'SECRET_KEY', 'DJANGO_DB_NAME', 'DJANGO_DB_USER', 'DJANGO_DB_PASS',
        'DJANGO_DB_HOST', 'DJANGO_DB_PORT', 'STATIC_PATH', 'STATIC_ROOT',
        'MEDIA_PATH', 'MEDIA_ROOT', 'PROTECTED_PATH', 'PROTECTED_ROOT',
        'TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'SENTRY_DSN_URL', 'ROOT_LOG_LEVEL',
        'DJANGO_LOG_LEVEL', 'DJANGO_REQUEST_LOG_LEVEL', 'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN', 'GOOGLE_RECAPTCHA_SECRET_KEY',
    ]
    for v in import_vars:
        globals()[v] = os.getenv(v, default=None)
        if globals()[v] == 'true':
            globals()[v] = True
        elif globals()[v] == 'false':
            globals()[v] = False
        # print(f"{v} = {globals()[v]}")
        __all__.append(v)

    # @TODO: Add a check for the fields that cannot be empty, ie SECRET_KEY etc...
    # for v in important_import_vars:
    # try:
    #     globals()[v]
    # except NameError:
    #     ISSUE
    # else:
    #     ISSUE if globals()[v] is unset..

