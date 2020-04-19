import yaml


class Config:
    def __init__(self, email=None, course=None):
        self.email: Email = email
        self.course: Course = course


class Email:
    def __init__(self, username, password, server="stmp.gmail.com"):
        self.username: str = username
        self.password: str = password
        self.server: str = server


class Course:
    def __init__(self, name="", semester=""):
        self.name: str = name
        self.semester: str = semester


def load() -> Config:
    cfg = {
        "email": {"server": "", "username": "", "password": ""},
        "course": {"name": "", "semester": ""},
    }
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.Loader)

    return Config(
        email=Email(
            username=cfg["email"]["username"],
            password=cfg["email"]["password"],
            server=cfg["email"]["server"],
        ),
        course=Course(name=cfg["course"]["name"], semester=cfg["course"]["semester"]),
    )
