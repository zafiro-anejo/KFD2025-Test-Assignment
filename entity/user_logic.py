from dataclasses import dataclass, field

from entity.time_management import TimeManagement
from entity.borrow_logic import BorrowRecord


@dataclass
class User:
    _name: str
    _user_id: str
    _email: str
    _max_books: int
    _max_borrow_days: int
    _borrowed_books: list = field(default_factory=list)
    _borrow_history: list = field(default_factory=list)

    @property
    def name(self):
        return self._name

    @property
    def user_id(self):
        return self._user_id

    @property
    def email(self):
        return self._email

    @property
    def max_books(self):
        return self._max_books

    @property
    def max_borrow_days(self):
        return self._max_borrow_days

    @property
    def borrowed_books(self):
        return self._borrowed_books

    @property
    def borrow_history(self):
        return self._borrow_history

    def can_borrow_more(self):
        count = 0

        for record in self._borrowed_books:

            if not record.returned:
                count += 1

        return count < self._max_books

    def borrow_book(self, isbn):
        if not self.can_borrow_more():
            return None

        time_ = TimeManagement()
        current_time = time_.to_get_borrowed_date()
        due_date = time_.to_get_overdue_date(self._max_borrow_days)

        record = BorrowRecord(isbn, current_time, due_date)

        self._borrowed_books.append(record)
        self._borrow_history.append(record)

        return record

    def return_book(self, isbn):
        time_ = TimeManagement()
        current_time = time_.to_get_borrowed_date()

        for record in self._borrowed_books:
            if record.book_isbn == isbn and not record.returned:

                record.returned = True
                record.return_date = current_time

                return True

        return False

    def get_current_borrowed_books(self):
        current_books = []

        for record in self._borrowed_books:

            if not record.returned:
                current_books.append(record)

        return current_books

    def get_overdue_books(self):
        time_ = TimeManagement()
        overdue_books = []

        for record in self._borrowed_books:

            if not record.returned:
                is_overdue = time_.to_overdue_check(record.due_date)

                if is_overdue:
                    overdue_books.append(record)

        return overdue_books


class Student(User):
    def __init__(self, name, user_id, email):
        super().__init__(name, user_id, email, 3, 14)


class Faculty(User):
    def __init__(self, name, user_id, email):
        super().__init__(name, user_id, email, 10, 30)


class Guest(User):
    def __init__(self, name, user_id, email):
        super().__init__(name, user_id, email, 1, 7)
