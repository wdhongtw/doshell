import datetime


_day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def main_iso_week() -> None:
    year, week, day = datetime.date.today().isocalendar()

    print(f"{year} W{week} {_day_names[day - 1]}")
