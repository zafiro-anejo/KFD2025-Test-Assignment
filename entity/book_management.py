from entity.book_logic import Book


class BookManagerInterface:
    def __init__(self):
        self.books = {}
        self.books_by_title = {}
        self.books_by_author = {}

    def add_book(self, title, author, isbn):
        if isbn in self.books:
            return False

        book = Book(title, author, isbn)
        self.books[isbn] = book

        if title not in self.books_by_title:
            self.books_by_title[title] = []

        self.books_by_title[title].append(book)

        if author not in self.books_by_author:
            self.books_by_author[author] = []

        self.books_by_author[author].append(book)

        return True

    def remove_book(self, isbn):

        if isbn not in self.books:
            return False

        book = self.books[isbn]

        if book.title in self.books_by_title:
            self.books_by_title[book.title] = [
                b
                for b in self.books_by_title[book.title]
                if b.isbn != isbn
            ]

            if not self.books_by_title[book.title]:
                del self.books_by_title[book.title]

        if book.author in self.books_by_author:
            self.books_by_author[book.author] = [
                b
                for b in self.books_by_author[book.author]
                if b.isbn != isbn
            ]

            if not self.books_by_author[book.author]:
                del self.books_by_author[book.author]

        del self.books[isbn]

        return True

    def get_book(self, isbn):
        return self.books.get(isbn)

    def search_by_title(self, title):
        return self.books_by_title.get(title, [])

    def search_by_author(self, author):
        return self.books_by_author.get(author, [])

    def search_by_isbn(self, isbn):
        return self.books.get(isbn)

    def mark_as_borrowed(self, isbn, user_id):
        if isbn not in self.books or not self.books[isbn].available:
            return False

        self.books[isbn].available = False
        self.books[isbn].borrowed_by = user_id

        return True

    def mark_as_returned(self, isbn):

        if isbn not in self.books or self.books[isbn].available:
            return False

        self.books[isbn].available = True
        self.books[isbn].borrowed_by = None

        return True

    def get_all_books(self):
        return list(self.books.values())
