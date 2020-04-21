# Harpocrates
>  The god of silence, secrets and confidentiality

[![Drone (cloud)](https://img.shields.io/drone/build/aut-ce/harpocrates.svg?style=flat-square)](https://cloud.drone.io/aut-ce/harpocrates)

## Introduction

This is a python code to send each student's grade privately using
`smtplib` to send emails from python and `csv` to deal with csv file
of grades and students' names.

There are two sample csv files that you can see [sample.csv](sample.csv).

## send one grade

 As you can see in [sample.csv](sample.csv) you should have a sheet like
 this(if your column names are different feel free to change them in code) and then
 you can fill [subject.txt](subject.txt) and [body.txt](body.txt) with the text that
 you want yo send as your email subject and its body. You can change the text format
 but you should put {name} and {grade} where you want the student's name and grade to be.

## send more than one grade

Sometimes you want to send minor grades of an exercise or exam in addition to overall
score. In this case you can use [more_grades.py](more_grades.py) with a sheet like
[sample_more.csv](sample_more.csv). Here you should enter index of columns that you
want to get grades from them in the code and then after editing subject and body text in
[subject.txt](subject.txt) and [more_body.txt](more_body.txt) you can run the program.
The code writes each grade in a separate line in email text so dont worry.

## Enter smtp and email address

After fixing sheets and changing txt files run the program and enter your smtp address
and after that your email address and its password.

Note that if you use gmail you must go to your google account and change
*Less secure app access* [here](https://myaccount.google.com/lesssecureapps) by turning on
8Allow less secure apps8. Otherwise you need to use [application-specific passwords](https://support.google.com/accounts/answer/185833?hl=en).

## Installation

You just need to install pandas using [pip](https://pip.pypa.io/en/stable/) to run this program.

```bash
pip install .
```

## Examples
Here you can see some examples of emails I sent from sample csv files:

![example](img/example.png)

![example](img/more_example.png)
