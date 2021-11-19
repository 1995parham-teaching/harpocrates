"""
Test import from csv
"""
from importer import get_info_from_csv


def test_import():
    """
    Test import function with sample.csv
    """
    with open("sample.csv", "r") as file:
        students = get_info_from_csv(file)
        assert len(students) == 1
        assert students[0].name == "کیان کشفی پور"
        assert students[0].email == "parham.alvani@gmail.com"
        assert students[0].grades == {
            "سوال ۱": 100.0,
            "سوال ۲": 100.0,
            "سوال ۳": 100.0,
            "سوال ۴": 100.0,
            "سوال ۵": 100.0,
            "سوال ۶": 100.0,
            "سوال ۷ - امتیازی": 100.0,
            "سوال ۸ - امتیازی": 100.0,
            "مجموع": 125.0,
        }
        assert students[0].note == "این دانشجو بسیار خوب است"
