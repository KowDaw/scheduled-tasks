import os
import smtplib
import pandas
import datetime as dt
from random import randint

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

def get_today_month_and_today_day():
    current_date = dt.datetime.now()
    return (current_date.month, current_date.day)

def get_data_from_row(row, keyword):
    splitted_row = row.split(",")

    if keyword == "name":
        return splitted_row[0]
    elif keyword == "email_address":
        return splitted_row[1]
    else:
        return None

def format_row(row):
    return f"{row["name"]},{row["email"]},{row["year"]},{row["month"]},{row["day"]}"

def read_birthdays(file_path):
    try:
        data = pandas.read_csv(file_path)
        new_dict = {(row["month"], row["day"]): format_row(row) for (index, row) in data.iterrows()}
        return new_dict
    except FileNotFoundError:
        print("File Not Found")
        return {}
    
def read_letter_template(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            letter_template = file.read()

        return letter_template
    except FileNotFoundError:
        print("File Not Found")
        return []

def create_personal_birthday_letter(name, random_letter_template):
    personal_birthday_letter = random_letter_template.replace("[NAME]", name)
    return personal_birthday_letter

def send_birthday_letter_via_email(to_email, personal_birthday_letter):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=to_email,
                msg=f"Subject:Happy Birthday!\n\n{personal_birthday_letter}"
            )

            print("Email sending was successful!")
    except:
        print("The connection was wrong!")

def check_birthdays(birthdays, letter_template):
    for birthday_key in birthdays:
        (birthday_month, birthday_day) = birthday_key
        (today_month, today_day) = get_today_month_and_today_day()

        if birthday_month == today_month and birthday_day == today_day:
            name = get_data_from_row(birthdays[birthday_key], "name")
            to_email = get_data_from_row(birthdays[birthday_key], "email_address")
            personal_birthday_letter = create_personal_birthday_letter(name, letter_template)

            send_birthday_letter_via_email(to_email, personal_birthday_letter)

def run_app():
    birthdays = read_birthdays("birthdays.csv")
    random_letter_template = read_letter_template(f"letter_templates/letter_{randint(1, 4)}.txt")
    check_birthdays(birthdays, random_letter_template)

run_app()
