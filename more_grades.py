import smtplib

import pandas as pd
import yaml


# getting information from csv file and returning them as lists.
def get_info_from_csv(csv_file):
    all_grades = {}
    students = pd.read_csv(csv_file)  # reading csv file
    student_names = students.loc[
                    2:, "نام"
                    ].to_list()  # getting students' names and adding them to a list.
    lastname = students.loc[
               2:, "نام خانوادگی"
               ].to_list()  # getting students' lastnames.
    for i in range(len(student_names)):
        student_names[i] = (student_names[i] + " " + lastname[i]).replace("\u200c", " ")
        student_names[i] = student_names[i].replace("\u200d", "")
    grade = students.iloc[2:, 3:12].to_dict()
    email = students.loc[
            2:, "ایمیل"
            ].to_list()  # getting students' emails and converting them to a list
    for i in range(len(email)):
        a_grade = []
        for g in grade:
            a_grade.append(f"{g} : {grade[g][i + 2]}")
        all_grades[i] = a_grade
        # print(g, )
        # print(all_grades[i])
    return student_names, email, all_grades


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
    names, emails, grades = get_info_from_csv("sample_more.csv")

    # making server
    server = run_server(smtp_server, email_user, email_password)

    # reading subject of emails from txt file.
    with open("subject.txt") as subject_file:
        SUBJECT = subject_file.read()

    # sending emails to each student one by one.
    for i in range(len(names)):
        with open("more_body.txt") as body_file:
            TEXT = body_file.read()
        to = [emails[i]]
        g = ""
        for k in grades[i]:
            g += f"{k} \n"
        TEXT = TEXT.format(name=names[i], grade=g)
        msg = "Subject: {}\n\n{}".format(SUBJECT, TEXT).encode("UTF_8")
        # print(msg)
        # sending email to each student
        server.sendmail(sent_from, to[0], msg)
        print(f"Email number {i + 1} sent!")
    server.close()
    print("Finished.")
