from entity.user_logic import Student, Faculty, Guest


class UserManagerInterface:
    def __init__(self):
        self.users = {}

    def register_user(self, user_type, name, user_id, email):
        if user_id in self.users:
            return False

        if user_type.lower() == "student":
            user = Student(name, user_id, email)
        elif user_type.lower() == "faculty":
            user = Faculty(name, user_id, email)
        elif user_type.lower() == "guest":
            user = Guest(name, user_id, email)
        else:
            return False

        self.users[user_id] = user

        return True

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_user_by_book(self, book_isbn):
        for user in self.users.values():
            for record in user.borrowed_books:

                if record.book_isbn == book_isbn and not record.returned:
                    return user

        return None

    def remove_user(self, user_id):
        if user_id not in self.users:
            return False

        user = self.users[user_id]
        has_borrowed_books = False

        for record in user.borrowed_books:
            if not record.returned:
                has_borrowed_books = True
                break

        if has_borrowed_books:
            return False

        del self.users[user_id]

        return True

    def get_all_users(self):
        return list(self.users.values())
