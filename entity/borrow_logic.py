from dataclasses import dataclass
from datetime import datetime


@dataclass
class BorrowRecord:
    _book_isbn: str
    _borrow_date: datetime
    _due_date: datetime
    _returned: bool = False
    _return_date: datetime = None

    @property
    def book_isbn(self):
        return self._book_isbn

    @property
    def borrow_date(self):
        return self._borrow_date

    @property
    def due_date(self):
        return self._due_date

    @property
    def returned(self):
        return self._returned

    @returned.setter
    def returned(self, value):
        self._returned = value

    @property
    def return_date(self):
        return self._return_date

    @return_date.setter
    def return_date(self, value):
        self._return_date = value
