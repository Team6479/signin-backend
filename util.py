from datetime import datetime, date, time

def fsec(secs: int) -> str:
    hours, remainder = divmod(secs, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours + ':' + minutes + ':' + seconds

def ftime_from_date(ts: int) -> str:
    t = datetime.fromtimestamp(ts).time()
    return t.strftime('%H:%M:%S')