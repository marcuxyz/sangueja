from datetime import date

import pytest

from app.repositories.blood_center import BloodCenterRepository


@pytest.mark.parametrize(
    ("collected_at", "expected"),
    (
        ("2026-07-27T09:35:31-03:00", date(2026, 7, 27)),
        ("05/08/2026", date(2026, 8, 5)),
        ("12/04/21", date(2021, 4, 12)),
    ),
)
def test_normalize_collected_at(collected_at, expected):
    assert BloodCenterRepository._normalize_collected_at(collected_at) == expected


def test_normalize_collected_at_rejects_invalid_date():
    with pytest.raises(ValueError, match="Invalid collection date"):
        BloodCenterRepository._normalize_collected_at("not-a-date")
