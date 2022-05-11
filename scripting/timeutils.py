import datetime
from datetime import timezone
from dateutil import parser
import parsedatetime

def str_timestamp_to_epoch(ts: str) -> int:
    time = parser.parse(ts)
    return datetime_to_epoch(time)

def human_input_to_epoch(time: str) -> int:
    cal = parsedatetime.Calendar()
    datetime_obj, _ = cal.parseDT(datetimeString=time)
    return datetime_to_epoch(datetime_obj)


def datetime_to_epoch(time: datetime) -> int:
    return int(time.timestamp())