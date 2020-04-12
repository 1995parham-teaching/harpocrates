import os
import smtplib
from _stat import S_IWUSR

import numpy as np
import pandas as pd
students= pd.read_csv('TEST1.csv')
names=students['نام'].to_list()
lastnames=students['نام خانوادگی'].to_list()
for i in range(len(names)):
    names[i]=(names[i]+" "+lastnames[i]).replace('\u200c'," ")
    names[i]=names[i].replace('\u200d',"")

print(names)
grades = students['نمره'].to_list()
print(grades)
emails = students['ایمیل'].to_list()
print(emails)
smtp_server = input("Enter your smtp server address")
gmail_user = input("Enter you email address")
gmail_password = input("Enter your email password")
# os.chmod('/usr/lib/python3.6/smtplib.py', S_IWUSR) # This makes the file read/write for the owner

sent_from = gmail_user
for i in range(len(names)):
    to = [emails[i]]
# for i in range(len(to)):
    subject = 'midterm grade'
    body = f' your grade in midterm exam is {grades[i]}. '

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)
    SUBJECT = "نمره تمرین دوم"
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
# try:
    server = smtplib.SMTP(smtp_server, 587)
    server.ehlo()
    print("1")
    server.starttls()
    print("2")
    server.login(gmail_user, gmail_password)
    print("3")
    server.sendmail(sent_from, to[0], msg)
    print("4")
    server.close()

    print('Email sent!')
# except:
    print('failed!')