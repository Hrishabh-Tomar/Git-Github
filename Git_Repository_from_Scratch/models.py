"""Data model for the task tracker."""

from dataclasses import dataclass, asdict

VALID_PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    """A single to-do item."""

    id: int
    title: str
    priority: str = "medium"
    done: bool = False

    def __post_init__(self):
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(
                f"priority must be one of {VALID_PRIORITIES}, got {self.priority!r}"
            )

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)