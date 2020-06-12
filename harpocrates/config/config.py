import yaml
import dataclasses
import typing


@dataclasses.dataclass
class Email:
    username: str
    password: str
    server: str


@dataclasses.dataclass
class Course:
    name: str
    semester: str


@dataclasses.dataclass
class Config:
    email: typing.Union[Email, None] = None
    course: typing.Union[Course, None] = None


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
        course=Course(
            name=cfg["course"]["name"], semester=cfg["course"]["semester"]
        ),
    )
