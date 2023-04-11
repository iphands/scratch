from datetime import timedelta, datetime
# from suntime import Sun, SunTimeException
from astral.sun import sun
from astral import LocationInfo

avl = LocationInfo("Asheville", "USA", "America/New_York",    35.5951, -82.5516)
sea = LocationInfo("Seattle",   "USA", "America/Los_Angeles", 47.6062, -122.3321)
eun = LocationInfo("Eunice",    "USA", "America/Chicago",     30.4944, -92.4176)

city = eun

t = datetime(2023, 1, 1)
for i in range(0, 365):
    s = sun(city.observer, date=t, tzinfo=city.timezone)
    sr = s["sunrise"]
    ss = s["sunset"]
    day_len = (ss-sr).total_seconds() / 60 / 60
    day = t.strftime("%Y-%d-%m")
    print(f"{day}, {day_len}")
    assert day_len > 0
    t = t + timedelta(days=1)
