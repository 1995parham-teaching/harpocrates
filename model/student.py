from typing import Dict


class Student:
    def __init__(self, name, email, grades={}):
        self.name: str = name
        self.email: str = email
        self.grades: Dict[str, int] = grades
