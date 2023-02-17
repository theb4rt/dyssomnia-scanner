import os
import time
from datetime import datetime, timezone
from ms import app

utc = timezone.utc
app_tz = app.config.get('APP_TIMEZONE', 'UTC')

os.environ['TZ'] = app_tz
time.tzset()


def now() -> datetime:
    return datetime.now(tz=utc)


def epoch_now() -> int:
    return int(time.time())


def datetime_to_epoch(date):
    return int(date.timestamp())
