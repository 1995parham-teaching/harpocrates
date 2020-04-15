import smtplib
import pandas as pd


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


if __name__ == "__main__":
    # getting user's data
    smtp_server = input("Enter your smtp server address: ")
    gmail_user = input("Enter you email address: ")
    gmail_password = input("Enter your email password: ")
    sent_from = gmail_user
    # getting data from our csv file
    names, emails, grades = get_info_from_csv("sample_more.csv")

    # making server and logging in to user's email
    server = run_server(smtp_server, gmail_user, gmail_password)

    # reading subject of emails from txt file.
    with open("subject.txt") as subject_file:
        SUBJECT = subject_file.read()

    # sending emails to each student one by one.
    for i in range(len(names)):
        with open("more_body.txt") as body_file:
            TEXT = body_file.read()
        to = [emails[i]]
        # Text of email
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
