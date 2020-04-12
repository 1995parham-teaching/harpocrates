import smtplib
import pandas as pd
# reading csv file
students= pd.read_csv('TEST1.csv')
# getting students' names and adding them to a list
names=students['نام'].to_list()
lastnames=students['نام خانوادگی'].to_list()
for i in range(len(names)):
    names[i]=(names[i]+" "+lastnames[i]).replace('\u200c'," ")
    names[i]=names[i].replace('\u200d',"")
print(names)
# getting students' names and converting them to a list
grades = students['نمره'].to_list()
print(grades)
# getting students' emails and converting them to a list
emails = students['ایمیل'].to_list()
print(emails)
#getting user's data
smtp_server = input("Enter your smtp server address")
gmail_user = input("Enter you email address")
gmail_password = input("Enter your email password")

sent_from = gmail_user
#making server and logging in to user's email
server = smtplib.SMTP(smtp_server, 587)
server.ehlo()
print("1")
server.starttls()
print("2")
server.login(gmail_user, gmail_password)
print("3")
#starting to send emails
for i in range(len(names)):
    to = [emails[i]]
#subject of email
    SUBJECT = "نمره تمرین دوم"
#body text of email
    TEXT=f"""
    با سلام
    دانشجوی عزیز  {names[i]}
    نمره‌ی تمرین دوم شما :
    میباشد.{grades[i]}
    موفق باشید.
    در صورت هرگونه اعتراضی با ایمیل زیر در تماس باشید.
    kiankr79@gmail.com
    """
    msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT).encode('UTF_8')
#
#sending email to each student
    server.sendmail(sent_from, to[0], msg)
    print("4")

    print(f'Email number {i+1} sent!')
#     print('failed!')
server.close()