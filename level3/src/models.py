"""Data models — to be implemented in EXP-2."""
from dataclasses import dataclass , asdict
from typing import Any
@dataclass
class Expense:
    id: int
    amount: float
    category: str
    date: str  # ISO "YYYY-MM-DD"
    def __post_init__(self) -> None:
        self.amount = round(float(self.amount), 2)
        self.category = self.category.strip().lower()
    def to_dict(self) -> dict:
        return asdict(self)
    @classmethod 
    def from_dict(cls, data: dict[str, Any]) -> "Expense":
        """Build an Expense from a dict, coercing types defensively."""
        return cls(
            id=int(data["id"]),
            amount=round(float(data["amount"]), 2),
            category=str(data["category"]).strip().lower(),
            date=str(data["date"]),
        )
