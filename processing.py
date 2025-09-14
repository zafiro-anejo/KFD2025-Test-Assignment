from entity.library_management import LibraryInterface
from entity.time_management import TimeManagement


class LibraryConsoleInterface:
    def __init__(self):
        self.library = LibraryInterface()
        self.running = True

    @staticmethod
    def display_menu():
        print("\n\nБИБЛИОТЕЧНАЯ СИСТЕМА ИМО",
              "1. Добавить книгу",
              "2. Удалить книгу",
              "3. Зарегистрировать пользователя",
              "4. Удалить пользователя",
              "5. Взять книгу",
              "6. Вернуть книгу",
              "7. Поиск книг",
              "8. Показать все книги",
              "9. Показать просроченные книги",
              "10. Показать книги пользователя",
              "11. Выйти\n",
              sep="\n")

    def run(self):
        while self.running:
            self.display_menu()
            choice = input("Выберите опцию: ").strip()

            try:
                if choice == "1":
                    self.add_book()
                elif choice == "2":
                    self.remove_book()
                elif choice == "3":
                    self.register_user()
                elif choice == "4":
                    self.remove_user()
                elif choice == "5":
                    self.borrow_book()
                elif choice == "6":
                    self.return_book()
                elif choice == "7":
                    self.search_books()
                elif choice == "8":
                    self.show_all_books()
                elif choice == "9":
                    self.show_overdue_books()
                elif choice == "10":
                    self.show_user_books()
                elif choice == "11":
                    self.running = False
                else:
                    print("Неверный выбор. Попробуйте снова.")
            except Exception as error:
                print(f"Ошибка: {error}")

    def add_book(self):
        title = input("Название книги: ").strip()
        author = input("Автор: ").strip()
        isbn = input("ISBN: ").strip()

        if self.library.add_book(title, author, isbn):
            print("Книга успешно добавлена!")
        else:
            print("Ошибка: книга с таким ISBN уже существует.")

    def remove_book(self):
        isbn = input("ISBN книги для удаления: ").strip()
        if self.library.remove_book(isbn):
            print("Книга успешно удалена!")
        else:
            print("Ошибка: книга не найдена или сейчас взята читателем.")

    def register_user(self):
        print("Тип пользователя: student, faculty, guest")
        user_type = input("Тип: ").strip().lower()
        name = input("Имя: ").strip()
        user_id = input("ID пользователя: ").strip()
        email = input("Email: ").strip()

        if user_type not in ["student", "faculty", "guest"]:
            print("Неверный тип пользователя.")
            return

        if self.library.register_user(user_type, name, user_id, email):
            print("Пользователь успешно зарегистрирован!")
        else:
            print("Ошибка: пользователь с таким ID уже существует.")

    def remove_user(self):
        user_id = input("ID пользователя для удаления: ").strip()

        if self.library.remove_user(user_id):
            print("Пользователь успешно удален!")
        else:
            print("Ошибка: пользователь не найден или имеет взятые книги.")

    def borrow_book(self):
        user_id = input("ID пользователя: ").strip()
        isbn = input("ISBN книги: ").strip()

        if self.library.borrow_book(user_id, isbn):
            print("Книга успешно взята!")
        else:
            print("Ошибка: невозможно взять книгу.")

    def return_book(self):
        user_id = input("ID пользователя: ").strip()
        isbn = input("ISBN книги: ").strip()

        if self.library.return_book(user_id, isbn):
            print("Книга успешно возвращена!")
        else:
            print("Ошибка: невозможно вернуть книгу.")

    def search_books(self):
        print("Поиск по: 1 - названию, 2 - автору, 3 - ISBN")
        search_type = input("Выберите тип поиска: ").strip()
        query = input("Поисковый запрос: ").strip()

        books = []
        if search_type == "1":
            books = self.library.search_books_by_title(query)
        elif search_type == "2":
            books = self.library.search_books_by_author(query)
        elif search_type == "3":
            book = self.library.search_books_by_isbn(query)
            books = [book] if book else []
        else:
            print("Неверный тип поиска.")

        if not books:
            print("Книги не найдены.")
        else:
            for book in books:
                status = "Доступна" if book.available else "Взята"
                print(f"{book.title} - {book.author} ({book.isbn}) - {status}")

    def show_all_books(self):
        books = self.library.get_all_books()
        if not books:
            print("В библиотеке нет книг.")
        else:
            for book in books:
                status = "Доступна" if book.available else "Взята"
                print(f"{book.title} - {book.author} ({book.isbn}) - {status}")

    def show_overdue_books(self):
        overdue_books = self.library.get_overdue_books()

        if not overdue_books:
            print("Просроченных книг нет.")

        else:

            for record in overdue_books:
                user = self.library.user_manager.get_user_by_book(record.book_isbn)
                print(f"Книга {record.book_isbn} просрочена у пользователя {user.user_id if user else 'Unknown'}")

    def show_user_books(self):
        user_id = input("ID пользователя: ").strip()
        borrowed_books = self.library.get_user_borrowed_books(user_id)

        if not borrowed_books:
            print("У пользователя нет взятых книг.")
        else:
            time_management = TimeManagement()
            for record in borrowed_books:
                book = self.library.book_manager.get_book(record.book_isbn)
                if book:

                    overdue = time_management.to_overdue_check(record.due_date)
                    status = "Не просрочена" if overdue else "Просрочена"
                    due_date_str = record.due_date.strftime("%Y-%m-%d")

                    print(f"{book.title} - до {due_date_str} - {status}")