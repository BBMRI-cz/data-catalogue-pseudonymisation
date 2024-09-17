from datetime import datetime


def covert_str_to_datetime(date_string) -> datetime:
    date_format = '%a, %d %b %Y %H:%M:%S %Z'
    return datetime.strptime(date_string, date_format)
