from main import get_info_from_csv


def test_import():
    with open("sample.csv", "r") as f:
        students = get_info_from_csv(f)
        assert len(students) == 1
        assert students[0].name == "کیان کشفی پور"
        assert students[0].email == "parham.alvani@gmail.com"
        assert students[0].grades == {
            "سوال ۱": "100",
            "سوال ۲": "100",
            "سوال ۳": "100",
            "سوال ۴": "100",
            "سوال ۵": "100",
            "سوال ۶": "100",
            "سوال ۷ - امتیازی": "100",
            "سوال ۸ - امتیازی": "100",
            "مجموع": "125",
        }
