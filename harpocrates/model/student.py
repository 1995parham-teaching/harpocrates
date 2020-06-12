"""
Student model
"""
from typing import Dict
import dataclasses


@dataclasses.dataclass(frozen=True, repr=True)
class Student:
    """
    Student contains information about each student
    """

    name: str
    email: str
    grades: Dict[str, float] = dataclasses.field(default_factory=dict)
    note: str = ""
