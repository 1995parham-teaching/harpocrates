"""
Harpocrates entry point
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from rich import pretty
import click
from jinja2 import Template

import config
import importer


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
    "--information",
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
def main(information, body, subject, dry_run):
    """
    Main command of harpocrates that warps everything up.
    """
    pretty.install()

    cfg = config.load()
    pretty.pprint(cfg)

    # getting data from our csv file
    students = importer.get_info_from_csv(information)

    # making server
    mail_server = None
    if not dry_run:
        mail_server = run_server(
            cfg.email.server, cfg.email.username, cfg.email.password
        )

    # reading subject of emails from txt file.
    subject = subject.read()

    # sending emails to each student one by one.
    body = body.read()

    for student in students:
        destination = student.email

        message = MIMEMultipart("alternative")
        message[
            "Subject"
        ] = f"{cfg.course.name} - {cfg.course.semester}: {subject}"
        message["From"] = cfg.email.username
        message["To"] = destination

        # Text of email
        tmpl = Template(body)
        rbody = tmpl.render(
            name=student.name, grades=student.grades, note=student.note
        )

        message.attach(MIMEText(rbody, "html"))

        # sending email to each student
        if mail_server is not None:
            mail_server.sendmail(
                cfg.email.username, destination, message.as_string()
            )
            print(f"Email sent to {student.name}!")
        else:
            pretty.pprint(student)
            pretty.pprint(rbody)

    if mail_server is not None:
        mail_server.close()
    print("Finished.")


# pylint: disable=no-value-for-parameter
main()
