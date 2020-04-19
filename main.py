import smtplib
import click
import pandas as pd
from jinja2 import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

# getting information from csv file and returning them as lists.


def get_info_from_csv(csv_file):
    students = pd.read_csv(csv_file)  # reading csv file
    student_names = students[
        "نام"
    ].to_list()  # getting students' names and adding them to a list.
    lastname = students["نام خانوادگی"].to_list()  # getting students' lastnames.
    for i in range(len(student_names)):
        student_names[i] = student_names[i] + " " + lastname[i]
    student_grades = students["نمره"].to_list()  # getting grades from csv
    email = students[
        "ایمیل"
    ].to_list()  # getting students' emails and converting them to a list
    return student_names, student_grades, email


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
    names, grades, emails = get_info_from_csv(input)

    # making server
    mail_server = run_server(cfg.email.server, cfg.email.username, cfg.email.password)

    # reading subject of emails from txt file.
    subject = subject.read()

    # sending emails to each student one by one.
    body = body.read()

    for i in range(len(names)):
        to = emails[i]

        message = MIMEMultipart("alternative")
        message["Subject"] = f"{cfg.course.name} - {cfg.course.semester}: {subject}"
        message["From"] = cfg.email.username
        message["To"] = to

        # Text of email
        tmpl = Template(body)
        body = tmpl.render(name=names[i], grade=grades[i])

        message.attach(MIMEText(body, "html"))

        # sending email to each student
        mail_server.sendmail(cfg.email.username, to, message.as_string())
        print(f"Email number {i + 1} sent to {names[i]}!")

    mail_server.close()
    print("Finished.")


if __name__ == "__main__":
    main()
