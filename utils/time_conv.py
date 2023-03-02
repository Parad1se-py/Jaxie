import datetime
import time


def seconds_to_dhms(time):
    seconds_to_minute   = 60
    seconds_to_hour     = 60 * seconds_to_minute
    seconds_to_day      = 24 * seconds_to_hour

    days    =   time // seconds_to_day
    time    %=  seconds_to_day

    hours   =   time // seconds_to_hour
    time    %=  seconds_to_hour

    minutes =   time // seconds_to_minute
    time    %=  seconds_to_minute

    seconds = time

    return [days, hours, minutes, seconds]

def convert_to_unix_time(date: datetime.datetime, days: int=0, hours: int=0, minutes: int=0, seconds: int=0) -> str:
    # Get the end date
    end_date = date + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    # Get a tuple of the date attributes
    date_tuple = (end_date.year, end_date.month, end_date.day, end_date.hour, end_date.minute, end_date.second)

    # Convert to unix time
    return f'<t:{int(time.mktime(datetime.datetime(*date_tuple).timetuple()))}:R>'
