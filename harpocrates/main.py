import smtplib
import csv
import itertools
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict

import click
from jinja2 import Template

import config
import model

# getting information from csv file and returning them as lists.

FIRST_NAME_COLUMN = "نام"
LAST_NAME_COLUMN = "نام خانوادگی"
STUDENT_ID_COLUMN = "شماره دانشجویی"
EMAIL_COLUMN = "ایمیل"
NOTE_COLUMN = "توضیحات"
SKIPPED_ROWS = 2
# please note that other columns consider as grades


def get_info_from_csv(file) -> List[model.Student]:
    students: List[model.Student] = []

    reader = csv.DictReader(file)
    for row in itertools.islice(reader, SKIPPED_ROWS, None):
        row.pop(STUDENT_ID_COLUMN)
        name = row.pop(FIRST_NAME_COLUMN) + " " + row.pop(LAST_NAME_COLUMN)
        email = row.pop(EMAIL_COLUMN)

        note = ""
        if NOTE_COLUMN in row:
            note = row.pop(NOTE_COLUMN)

        grades: Dict[str, float] = {}
        for problem, grade in row.items():
            grades[problem] = float(grade)

        students.append(model.Student(name, email, grades, note))

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
@click.option(
    "--dry-run",
    "-d",
    default=False,
    help="do not really send emails",
    type=bool,
    is_flag=True,
)
def main(input, body, subject, dry_run):
    # getting user's data and logging in to user's email
    cfg = config.load()

    # getting data from our csv file
    students = get_info_from_csv(input)

    # making server
    mail_server = None
    if dry_run is False:
        mail_server = run_server(
            cfg.email.server, cfg.email.username, cfg.email.password
        )

    # reading subject of emails from txt file.
    subject = subject.read()

    # sending emails to each student one by one.
    body = body.read()

    for student in students:
        to = student.email

        message = MIMEMultipart("alternative")
        message[
            "Subject"
        ] = f"{cfg.course.name} - {cfg.course.semester}: {subject}"
        message["From"] = cfg.email.username
        message["To"] = to

        # Text of email
        tmpl = Template(body)
        rbody = tmpl.render(
            name=student.name, grades=student.grades, note=student.note
        )

        message.attach(MIMEText(rbody, "html"))

        # sending email to each student
        if dry_run is False:
            mail_server.sendmail(cfg.email.username, to, message.as_string())
            print(f"Email sent to {student.name}!")
        else:
            print(student)
            print()
            print(rbody)

    if dry_run is False:
        mail_server.close()
    print("Finished.")


if __name__ == "__main__":
    main()
