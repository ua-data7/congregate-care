from django.conf import settings
import json
import os


CLUSTER_DAILY_FILENAME = 'cluster_facilities_daily.json'
CLUSTER_WEEKLY_FILENAME = 'cluster_no_submit_weekly.json'
NON_CLUSTER_WEEKLY_FILENAME = 'non_cluster_weekly.json'
MESSAGE_TPL_PATH = os.path.join(settings.BASE_DIR, 'sms', 'templates', 'messages')

def get_message_template(filename):
    path = os.path.join(MESSAGE_TPL_PATH, filename)
    with open(path) as f:
        return json.loads(f.read())

CLUSTER_DAILY_TPL = get_message_template(CLUSTER_DAILY_FILENAME)
CLUSTER_WEEKLY_TPL = get_message_template(CLUSTER_WEEKLY_FILENAME)
NON_CLUSTER_WEEKLY_TPL = get_message_template(NON_CLUSTER_WEEKLY_FILENAME)
