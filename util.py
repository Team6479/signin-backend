from datetime import datetime, date, time

def fsec(secs: int) -> str:
    hours, remainder = divmod(secs, 3600)
    minutes, seconds = divmod(remainder, 60)
    return str(hours) + ':' + str(minutes) + ':' + str(seconds)

def ftime_from_dt(ts: int) -> str:
    t = datetime.fromtimestamp(ts).time()
    return t.strftime('%H:%M:%S')

def fdate_from_dt(ts: int) -> str:
    d = datetime.fromtimestamp(ts).date()
    return d.strftime('%a, %d %b %Y')