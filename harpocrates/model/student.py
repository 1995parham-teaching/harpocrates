from typing import Dict
import dataclasses


@dataclasses.dataclass(frozen=True, repr=True)
class Student:
    name: str
    email: str
    grades: Dict[str, float] = dataclasses.field(default_factory=dict)
