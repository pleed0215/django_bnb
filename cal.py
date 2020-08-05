import calendar
import datetime
from django.utils import timezone


class Day:
    def __init__(self, day, past):
        self.day = day
        self.past = past


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ("Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun",)
        self.months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",)
        #self.firstweekday = 6

    def get_month(self):
        # cf. firstweekday = 0, default:0, means monday is the first of week, value:6 means sunday is firstday of weekd.
        return self.months[self.month-1]

    def get_days(self):
        weeks =  self.monthdays2calendar(self.year, self.month)
        days = []
        #now = datetime.datetime.now()
        now = timezone.now()
        this_month = now.month
        this_day= now.day
        past = False

        for week in weeks:
            for day, week_day in week:
                if day != 0:
                    past = False
                    if this_month == self.month:
                        if day <= this_day:
                            past = True
                    days.append(Day(day, past))
                else:
                    days.append(Day(day, True))
        
        return days