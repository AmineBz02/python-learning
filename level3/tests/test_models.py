import pytest
from src.models import Expense


def test_round_trip():
    e = Expense(id=1, amount=12.5, category="food", date="2025-01-15")
    assert Expense.from_dict(e.to_dict()) == e


def test_round_trip_coerces_types():
    raw = {"id": "7", "amount": "3.999", "category": "  TRAVEL ", "date": "2025-02-01"}
    e = Expense.from_dict(raw)
    assert e.id == 7
    assert e.amount == 4.0          # rounded to 2 dp
    assert e.category == "travel"   # trimmed + lowercased
    assert e.date == "2025-02-01"


def test_missing_field_raises():
    with pytest.raises(KeyError):
        Expense.from_dict({"id": 1, "amount": 2.0, "category": "food"})  # no date