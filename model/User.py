from dataclasses import dataclass


@dataclass
class User:
    first: str
    last: str
    email: str
    id: int = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            first=data.get('first'),
            last=data.get('last'),
            email=data.get('email')
        )