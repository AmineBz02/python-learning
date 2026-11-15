"""Data models — to be implemented in EXP-2."""
from dataclasses import dataclass

@dataclass
class Expense:
    id: int
    amount: float
    category: str
    date: str  # ISO "YYYY-MM-DD"

    def to_dict(self) -> dict:
        return {"id": self.id, "amount": self.amount,
                "category": self.category, "date": self.date}

    @classmethod
    def from_dict(cls, d: dict) -> "Expense":
        return cls(d["id"], float(d["amount"]), d["category"], d["date"])
