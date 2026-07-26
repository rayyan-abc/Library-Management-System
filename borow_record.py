class BorrowRecord:
    def __init__(
        self,
        borrow_id,
        book_id,
        book_title,
        borrower_name,
        borrow_date,
        return_date=None,
        status="Borrowed"
    ):
        self.borrow_id = borrow_id
        self.book_id = book_id
        self.book_title = book_title
        self.borrower_name = borrower_name
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.status = status

    def to_dict(self):
        return {
            "borrow_id": self.borrow_id,
            "book_id": self.book_id,
            "book_title": self.book_title,
            "borrower_name": self.borrower_name,
            "borrow_date": self.borrow_date,
            "return_date": self.return_date,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["borrow_id"],
            data["book_id"],
            data["book_title"],
            data["borrower_name"],
            data["borrow_date"],
            data["return_date"],
            data["status"]
        )