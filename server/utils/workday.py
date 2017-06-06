from datetime import date
from datetime import datetime, timedelta

class WorkDay():
    @staticmethod
    def easter(year):
        "Returns Easter as a date object."
        a = year % 19
        b = year // 100
        c = year % 100
        d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
        e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
        f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
        month = f // 31
        day = f % 31 + 1
        return datetime(year, month, day)

    @staticmethod
    def getFrenchHolidays(year):
        easter = WorkDay.easter(year)

        return sorted([
            datetime(year, 1, 1),
            datetime(year, 5, 1),
            datetime(year, 5, 8),
            datetime(year, 7, 14),
            datetime(year, 8, 15),
            datetime(year, 11, 1),
            datetime(year, 11, 11),
            datetime(year, 12, 25),
            easter,
            easter + timedelta(days=1),
            easter + timedelta(days=39),
            easter + timedelta(days=50)
        ])

if __name__ == '__main__':
    print WorkDay.getFrenchHolidays(2017)
