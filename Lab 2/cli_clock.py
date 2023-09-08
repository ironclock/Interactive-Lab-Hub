from time import strftime, sleep
import datetime
while True:
    def days_in_month(month, year):
        """Return the number of days in the given month."""
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        elif month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 29
            else:
                return 28
        else:
            return 0

    def get_zodiac_sign_and_progress(day, month, year):
        sign_dates = {
            "Aries": ((3, 21), (4, 19)),
            "Taurus": ((4, 20), (5, 20)),
            "Gemini": ((5, 21), (6, 20)),
            "Cancer": ((6, 21), (7, 22)),
            "Leo": ((7, 23), (8, 22)),
            "Virgo": ((8, 23), (9, 22)),
            "Libra": ((9, 23), (10, 22)),
            "Scorpio": ((10, 23), (11, 21)),
            "Sagittarius": ((11, 22), (12, 21)),
            "Capricorn": ((12, 22), (1, 19)),
            "Aquarius": ((1, 20), (2, 18)),
            "Pisces": ((2, 19), (3, 20))
        }

        for sign, (start, end) in sign_dates.items():
            if (month, day) >= start and (month, day) <= end:
                # Calculate percentage through the sign
                start_month, start_day = start
                end_month, end_day = end

                total_days = (days_in_month(start_month, year) - start_day + 1) + (day - 1)
                if start_month != end_month:
                    total_days += sum(days_in_month(m, year) for m in range(start_month+1, end_month))

                percentage = (total_days / (total_days + days_in_month(end_month, year) - day)) * 100

                return sign, percentage

        return "Unknown", 0

    def current_zodiac_sign_and_progress():
        now = datetime.datetime.now()
        month = now.month
        day = now.day
        year = now.year
        return get_zodiac_sign_and_progress(day, month, year)

    if __name__ == "__main__":
        sign, progress = current_zodiac_sign_and_progress()
        print(f"We are {progress:.10f}% through being a {sign}.")