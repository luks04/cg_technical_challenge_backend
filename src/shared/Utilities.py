import datetime

class Utilities:
    @staticmethod
    def serialize_date_format(date: str, date_format: str) -> str:
        """Return the same date with an standard date format"""
        return datetime.datetime.strptime(date, date_format).strftime('%d-%m-%Y')
