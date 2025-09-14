from dataclasses import dataclass
from typing import Optional


@dataclass
class Book:
    _title: str
    _author: str
    _isbn: str
    _available: bool = True
    _borrowed_by: Optional[str] = None

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def isbn(self):
        return self._isbn

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, value):
        self._available = value

    @property
    def borrowed_by(self):
        return self._borrowed_by

    @borrowed_by.setter
    def borrowed_by(self, value):
        self._borrowed_by = value
