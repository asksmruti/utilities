import holidays
import datetime


def find_holidays(country, current_state, current_year):
    cnt = 0
# Reference - https://github.com/dr-prodigy/python-holidays
    for date, name in sorted(country(state=current_state, years=current_year).items()):
        row = "|" + name.ljust(width) + "|" + str(date.strftime('%A').ljust(width)) + "|" + str(date) + "|"
        print(sep*len(row))
        print(row)
        cnt += 1
    print(sep*len(row))
    print("Total holidays :", cnt)


if __name__ == "__main__":
    now = datetime.datetime.now()
    state = "None"
    width = 30
    sep = '-'
    holidays_country = holidays.DE
    find_holidays(holidays_country, state, now.year)

