import datetime as dt
import pandas
import random
import os
import smtplib
# MY EMAIL and PASSWORD
MY_MAIL = "maneved19@gmail.com"
PASSWORD = "password"

# Check if today matches a birthday in the birthdays.csv

data = pandas.read_csv("birthdays.csv")

now = dt.datetime.now()
date = now.day
month = now.month

# Get a Today's Birthday
birthday = data.query(f'day == {date}' and f"month == {month}")
today_birthday = birthday.to_dict(orient="records")


# Pick the random Template
templates_path = os.listdir("letter_templates")
random_template = random.choice(templates_path)
file_path = os.path.join("letter_templates", random_template)

with open(file_path, "r") as file:
    lines = file.read()

for peoples in today_birthday:
    message = lines.replace("[NAME]", peoples["name"])
    # Send the letter
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_MAIL,
                         password=PASSWORD)
        connection.sendmail(from_addr=MY_MAIL,
                            to_addrs=peoples["email"],
                            msg=f"Subject:Happy Birthday!\n\n{message}")
