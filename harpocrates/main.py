import smtplib
import click
import csv
from jinja2 import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

import config
import model

# getting information from csv file and returning them as lists.

FIRST_NAME_COLUMN = "نام"
LAST_NAME_COLUMN = "نام خانوادگی"
STUDENT_ID_COLUMN = "شماره دانشجویی"
EMAIL_COLUMN = "ایمیل"
SKIPPED_ROWS = 2
# please note that other columns consider as grades


def get_info_from_csv(file) -> List[model.Student]:
    students = []
    c = 0

    reader = csv.DictReader(file)
    for row in reader:
        if c < SKIPPED_ROWS:
            c += 1
            continue

        row.pop(STUDENT_ID_COLUMN)
        name = row.pop(FIRST_NAME_COLUMN) + " " + row.pop(LAST_NAME_COLUMN)
        email = row.pop(EMAIL_COLUMN)
        students.append(model.Student(name, email, row))

    return students


def run_server(address, username, password):
    """
    running smtp server and logging in to user's email account.
    """

    smtp = smtplib.SMTP(address, 587)
    smtp.ehlo()
    smtp.starttls()
    print("Server started.")
    smtp.login(username, password)
    print(f"Logged in to {address} with {username}")
    return smtp


@click.command()
@click.option(
    "--input",
    "-i",
    default="sample.csv",
    help="path to input csv file",
    type=click.File(mode="r"),
)
@click.option(
    "--body",
    "-b",
    default="body.html",
    help="email's body in html",
    type=click.File(mode="r"),
)
@click.option(
    "--subject",
    "-s",
    default="subject.txt",
    help="email's subject",
    type=click.File(mode="r"),
)
def main(input, body, subject):
    # getting user's data and logging in to user's email
    cfg = config.load()

    # getting data from our csv file
    students = get_info_from_csv(input)

    # making server
    mail_server = run_server(cfg.email.server, cfg.email.username, cfg.email.password)

    # reading subject of emails from txt file.
    subject = subject.read()

    # sending emails to each student one by one.
    body = body.read()

    for student in students:
        to = student.email

        message = MIMEMultipart("alternative")
        message["Subject"] = f"{cfg.course.name} - {cfg.course.semester}: {subject}"
        message["From"] = cfg.email.username
        message["To"] = to

        # Text of email
        tmpl = Template(body)
        body = tmpl.render(name=student.name, grades=student.grades)

        message.attach(MIMEText(body, "html"))

        # sending email to each student
        mail_server.sendmail(cfg.email.username, to, message.as_string())
        print(f"Email sent to {student.name}!")

    mail_server.close()
    print("Finished.")


if __name__ == "__main__":
    main()
