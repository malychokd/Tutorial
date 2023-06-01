from datetime import datetime, timedelta

def get_birthdays_per_week(users):
    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())
    current_year = datetime.now().year

    week_birthdays = {}
    for user in users:
        name = user['name']
        birthday = user['birthday'].date()
        birthday_this_year = birthday.replace(year=current_year)

        days_until_birthday = (birthday_this_year - monday).days
    
        if days_until_birthday <= 7 and days_until_birthday > -1:
            birthday_date = monday + timedelta(days=days_until_birthday)
            day_of_week = birthday_date.strftime('%A')
            week_birthdays.setdefault(day_of_week, []).append(name)
        elif days_until_birthday > -3:   
            birthday_date = monday
            day_of_week = birthday_date.strftime('%A')
            week_birthdays.setdefault(day_of_week, []).append(name)
            
    for day, names in week_birthdays.items():
        names_str = ', '.join(names)
        print(f"{day}: {names_str}")

users = [
    {'name': 'Roma', 'birthday': datetime(1988, 5, 27)},
    {'name': 'Den', 'birthday': datetime(1988, 5, 28)},
    {'name': 'Tomy', 'birthday': datetime(1988, 5, 29)},
    {'name': 'Bill', 'birthday': datetime(1990, 5, 30)},
    {'name': 'Jill', 'birthday': datetime(1985, 6, 2)},
    {'name': 'Kim', 'birthday': datetime(1992, 6, 3)},
    {'name': 'Jan', 'birthday': datetime(1998, 5, 31)},
]

get_birthdays_per_week(users)
