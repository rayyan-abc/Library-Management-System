class Book:
    def __init__(
        self,
        book_id,
        title,
        author,
        category,
        publication_year,
        total_copies,
        available_copies=None
    ):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.publication_year = publication_year
        self.total_copies = total_copies
        self.available_copies = (
            total_copies if available_copies is None else available_copies
        )

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "publication_year": self.publication_year,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["book_id"],
            data["title"],
            data["author"],
            data["category"],
            data["publication_year"],
            data["total_copies"],
            data["available_copies"]
        )