import csv
import itertools

import model

# getting information from csv file and returning them as lists.

FIRST_NAME_COLUMN = "نام"
LAST_NAME_COLUMN = "نام خانوادگی"
STUDENT_ID_COLUMN = "شماره دانشجویی"
EMAIL_COLUMN = "ایمیل"
NOTE_COLUMN = "توضیحات"
SKIPPED_ROWS = 2
# please note that other columns consider as grades


def get_info_from_csv(file) -> list[model.Student]:
    """
    parse given csv file to gather student information.
    """
    students: list[model.Student] = []

    reader = csv.DictReader(file)
    for row in itertools.islice(reader, SKIPPED_ROWS, None):
        row.pop(STUDENT_ID_COLUMN)
        name = row.pop(FIRST_NAME_COLUMN) + " " + row.pop(LAST_NAME_COLUMN)
        email = row.pop(EMAIL_COLUMN)

        note = ""
        if NOTE_COLUMN in row:
            note = row.pop(NOTE_COLUMN)

        grades: dict[str, float] = {}
        for problem, grade in row.items():
            grades[problem] = float(grade)

        students.append(model.Student(name, email, grades, note))

    return students
