<h1 align="center">
Harpocrates 🙊
</h1>
<h6 align="center">The god of silence, secrets and confidentiality</h6>

<p align="center">
  <img src="https://img.shields.io/github/actions/workflow/status/1995parham-teaching/harpocrates/ci.yml?label=ci&logo=github&style=for-the-badge&branch=main" alt="GitHub Workflow Status">
  <img alt="GitHub" src="https://img.shields.io/github/license/1995parham-teaching/harpocrates?logo=gnu&style=for-the-badge">
  <img alt="Python version" src="https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2F1995parham-teaching%2Fharpocrates%2Fmain%2Fpyproject.toml&logo=python&style=for-the-badge">
  <img alt="GitHub release (latest SemVer including pre-releases)" src="https://img.shields.io/github/v/release/1995parham-teaching/harpocrates?include_prereleases&logo=github&style=for-the-badge">
</p>

## Introduction

This is a python code to send each student's grade privately using
`smtplib` to send emails from python and `csv` to deal with CSV file
of grades and students' names.

## Send Grades

As you can see in [sample.csv](sample.csv) you should have a sheet like
this (if your column names are different feel free to change them in code):

```python
FIRST_NAME_COLUMN = "نام"
LAST_NAME_COLUMN = "نام خانوادگی"
STUDENT_ID_COLUMN = "شماره دانشجویی"
EMAIL_COLUMN = "ایمیل"
NOTE_COLUMN = "توضیحات"
SKIPPED_ROWS = 2
```

Then you can fill [subject.txt](subject.txt) and [body.html](body.html) with the text that
you want to send as your email subject and its body. e.g.

```html
<html>
  <body dir="rtl">
    <p>
      با سلام<br />
      دانشجوی عزیز {{ name }}<br />
      نمره تمرین شما
    </p>
    <table>
      <tbody>
        {% for name, grade in grades.items() %}
        <tr>
          <td>{{ name }}</td>
          <td>{{ grade }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    <p>
      در صورت هرگونه اعتراض یا مشکلی با ایمیل زیر در تماس باشید.<br />

      <a href="mailto:parham.alvani@gmail.com">Pahram Alvani</a>
    </p>
  </body>
</html>
```

As you can see, this is a Jinja template, and you have variables that is set for each student.
Please note that you can check the emails before actually sending them with `--dry-run` flag.

## Enter SMTP/Email Address

After fixing sheets and changing TXT files, run the program and enter your SMTP address
and after that your email address and its password in configuration file. e.g.

```yaml
---
email:
  server: smtp.gmail.com
  username: parham.alvani@gmail.com
  password: secret
```

Note that if you use Gmail you must go to your Google account and change
_Less secure app access_ [here](https://myaccount.google.com/lesssecureapps) by turning on
_Allow less secure apps_. Otherwise, you need to use
[application-specific passwords](https://support.google.com/accounts/answer/185833?hl=en).

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency and environment management.

```bash
uv sync
cp config.example.yml config.yml
uv run harpocrates
```

## Examples

Here you can see some examples of emails I sent from sample CSV files:

<p align="center">
<img src=".github/assets/example.png" alt="example" />

<img src=".github/assets/more_example.png" alt="example" />

</p>
