"""
Configuration module load configuration from config.yml.
"""

import dataclasses

import yaml


@dataclasses.dataclass
class Email:
    """
    Email SMTP client configuration.
    """

    username: str
    password: str
    server: str


@dataclasses.dataclass
class Course:
    """
    Course configuration.
    """

    name: str
    semester: str


@dataclasses.dataclass
class Config:
    """
    Configuration structure.
    """

    email: Email
    course: Course


def load() -> Config:
    """
    Load configuration from config.yml into Config structure.
    """
    cfg = {
        "email": {"server": "", "username": "", "password": ""},
        "course": {"name": "", "semester": ""},
    }
    with open("config.yml", "r", encoding='utf8') as ymlfile:
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
