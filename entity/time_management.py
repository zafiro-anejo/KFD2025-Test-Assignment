from datetime import datetime, timedelta


class TimeManagement:

    @staticmethod
    def to_get_borrowed_date():
        borrowed_date = datetime.now()

        return borrowed_date

    def to_get_overdue_date(self, max_borrow_period):
        overdue_date = self.to_get_borrowed_date() + timedelta(days=max_borrow_period)

        return overdue_date

    @staticmethod
    def to_overdue_check(overdue_date):
        overdue_status = False if (overdue_date - datetime.now()).days < 0 else True

        return overdue_status
