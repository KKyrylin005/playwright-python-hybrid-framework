from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class User:
    username: str
    password: str = field(repr=False)  # keep secrets out of logs and Allure parameters
