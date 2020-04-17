import smtplib
import pandas as pd
import yaml


# getting information from csv file and returning them as lists.


def get_info_from_csv(csv_file):
    students = pd.read_csv(csv_file)  # reading csv file
    student_names = students[
        "نام"
    ].to_list()  # getting students' names and adding them to a list.
    lastname = students["نام خانوادگی"].to_list()  # getting students' lastnames.
    for i in range(len(student_names)):
        student_names[i] = (student_names[i] + " " + lastname[i]).replace("\u200c", " ")
        student_names[i] = student_names[i].replace("\u200d", "")
    student_grades = students["نمره"].to_list()  # getting grades from csv
    email = students[
        "ایمیل"
    ].to_list()  # getting students' emails and converting them to a list
    return student_names, student_grades, email


# running smtp server and logging in to user's email account.
def run_server(smtp_address, id, password):
    smtp = smtplib.SMTP(smtp_address, 587)
    smtp.ehlo()
    smtp.starttls()
    print("Server started.")
    smtp.login(id, password)
    print("Logged in to {user}".format(user=id))
    return smtp


def login(config_file):
    with open(config_file, "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.Loader)
    smtp_address = cfg["configs"]["smtp_address"]
    email_id = cfg["configs"]["email_address"]
    email_passwd = cfg["configs"]["password"]
    return smtp_address, email_id, email_passwd


if __name__ == "__main__":
    # getting user's data and logging in to user's email
    smtp_server, email_user, email_password = login('config.yml')

    sent_from = email_user
    # getting data from our csv file
    names, grades, emails = get_info_from_csv("sample.csv")

    # making server
    server = run_server(smtp_server, email_user, email_password)

    # reading subject of emails from txt file.
    with open("subject.txt") as subject_file:
        SUBJECT = subject_file.read()

    # sending emails to each student one by one.
    for i in range(len(names)):
        with open("body.txt") as body_file:
            TEXT = body_file.read()
        to = [emails[i]]
        # Text of email
        TEXT = TEXT.format(name=names[i], grade=grades[i])
        msg = "Subject: {}\n\n{}".format(SUBJECT, TEXT).encode("UTF_8")
        # sending email to each student
        server.sendmail(sent_from, to[0], msg)
        print(f"Email number {i + 1} sent!")
    server.close()
    print("Finished.")
