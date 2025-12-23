from __future__ import annotations
from datetime import date as date_cls, datetime
import json
from functools import lru_cache
from pathlib import Path
from typing import Optional

### Input validations
def validate_date(input_date):
    try:
        date = datetime.strptime(input_date, "%Y-%m-%d").date()
        today = date_cls.today()
        if date > today:
            print("\nWARNING: the entered date is in the future.\n")
        return True
    except ValueError:
        return False
    


### Importing default people for days and place
def _weekday(date_str: str) -> str:
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")


def _norm_city(city: str) -> str:
    return city.strip().lower()


@lru_cache(maxsize=1)
def _load_who_defaults() -> dict:
    path = Path(__file__).with_name("who_defaults.json")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def default_who(city: str, date_str: str) -> Optional[str]:
    data = _load_who_defaults()
    c = _norm_city(city)
    city_rules = data.get(c)
    if not isinstance(city_rules, dict):
        return None

    wd = _weekday(date_str)
    who = city_rules.get(wd)
    if isinstance(who, str):
        return who

    who = city_rules.get("*")
    if isinstance(who, str):
        return who

    return None