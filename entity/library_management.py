from datetime import datetime

from entity.book_management import BookManagerInterface
from entity.user_management import UserManagerInterface


class LibraryInterface:
    def __init__(self):
        self.book_manager = BookManagerInterface()
        self.user_manager = UserManagerInterface()

    def add_book(self, title, author, isbn):
        return self.book_manager.add_book(title, author, isbn)

    def remove_book(self, isbn):
        book = self.book_manager.get_book(isbn)

        if book and not book.available:
            return False

        return self.book_manager.remove_book(isbn)

    def register_user(self, user_type, name, user_id, email):
        return self.user_manager.register_user(user_type, name, user_id, email)

    def remove_user(self, user_id):
        return self.user_manager.remove_user(user_id)

    def borrow_book(self, user_id, isbn):
        user = self.user_manager.get_user(user_id)
        book = self.book_manager.get_book(isbn)

        if not user or not book:
            return False

        if not book.available:
            return False

        if not user.can_borrow_more():
            return False

        record = user.borrow_book(isbn)

        if record and self.book_manager.mark_as_borrowed(isbn, user_id):
            return True

        return False

    def return_book(self, user_id, isbn):
        user = self.user_manager.get_user(user_id)

        if not user:
            return False

        success = user.return_book(isbn) and self.book_manager.mark_as_returned(isbn)

        return success

    def search_books_by_title(self, title):
        return self.book_manager.search_by_title(title)

    def search_books_by_author(self, author):
        return self.book_manager.search_by_author(author)

    def search_books_by_isbn(self, isbn):
        return self.book_manager.search_by_isbn(isbn)

    def get_user_borrowed_books(self, user_id):
        user = self.user_manager.get_user(user_id)

        if not user:
            return []

        return user.get_current_borrowed_books()

    def get_overdue_books(self):
        all_overdue = []
        current_time = datetime.now()  # Получаем текущее время

        for user in self.user_manager.get_all_users():
            user_overdue_books = []

            for record in user.borrowed_books:

                if not record.returned and current_time > record.due_date:
                    user_overdue_books.append(record)

            all_overdue.extend(user_overdue_books)

        return all_overdue

    def get_all_books(self):
        return self.book_manager.get_all_books()

    def get_all_users(self):
        return self.user_manager.get_all_users()
