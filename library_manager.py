import json
from datetime import datetime
from collections import Counter
from book import Book
from borrow_record import BorrowRecord
class LibraryManager:
    def __init__(
        self,
        books_file="books.json",
        records_file="borrow_records.json"
    ):
        self.books_file = books_file
        self.records_file = records_file
        self.books = []
        self.borrow_records = []
        self.load_books()
        self.load_borrow_records()
    def load_books(self):
        try:
            with open(self.books_file, "r") as file:
                data = json.load(file)
                self.books = [
                    Book.from_dict(book)
                    for book in data
                ]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Error: books.json contains invalid JSON.")
            self.books = []

    def save_books(self):
        with open(self.books_file, "w") as file:
            json.dump(
                [book.to_dict() for book in self.books],
                file,
                indent=4
            )
    def load_borrow_records(self):
        try:
            with open(self.records_file, "r") as file:
                data = json.load(file)
                self.borrow_records = [
                    BorrowRecord.from_dict(record)
                    for record in data
                ]
        except FileNotFoundError:
            self.borrow_records = []

        except json.JSONDecodeError:
            print("Error: borrow_records.json contains invalid JSON.")
            self.borrow_records = []
    def save_borrow_records(self):
        with open(self.records_file, "w") as file:
            json.dump(
                [
                    record.to_dict()
                    for record in self.borrow_records
                ],
                file,
                indent=4
            )
    def add_book(self):
        try:
            book_id = input("Enter Book ID: ").strip()
            if any(book.book_id == book_id for book in self.books):
                raise ValueError("Book ID already exists.")
            title = input("Enter Title: ").strip()
            author = input("Enter Author: ").strip()
            category = input("Enter Category: ").strip()
            if not title or not author:
                raise ValueError("Title and Author cannot be empty.")
            publication_year = int(
                input("Enter Publication Year: ")
            )
            current_year = datetime.now().year
            if publication_year <= 0 or publication_year > current_year:
                raise ValueError("Invalid publication year.")
            total_copies = int(
                input("Enter Total Copies: ")
            )
            if total_copies < 0:
                raise ValueError("Copies cannot be negative.")
            book = Book(
                book_id,
                title,
                author,
                category,
                publication_year,
                total_copies
            )
            self.books.append(book)
            self.save_books()
            print("Book added successfully.")
        except ValueError as error:
            print(f"Error: {error}")
    def view_books(self):
        if not self.books:
            print("No books available.")
            return
        print("\n ALL BOOKS ")
        for book in self.books:
            print(f"""
Book ID: {book.book_id}
Title: {book.title}
Author: {book.author}
Category: {book.category}
Publication Year: {book.publication_year}
Total Copies: {book.total_copies}
Available Copies: {book.available_copies}
""")
    def search_book(self):
        search = input(
            "Enter Book ID or Title: "
        ).strip().lower()
        results = [
            book for book in self.books
            if book.book_id.lower() == search
            or search in book.title.lower()
        ]
        if not results:
            print("Book not found.")
            return
        for book in results:
            print(f"""
Book ID: {book.book_id}
Title: {book.title}
Author: {book.author}
Category: {book.category}
Available Copies: {book.available_copies}
""")
    def update_book(self):
        book_id = input("Enter Book ID to update: ").strip()
        book = next(
            (
                book for book in self.books
                if book.book_id == book_id
            ),
            None
        )
        if not book:
            print("Book not found.")
            return
        try:
            title = input(
                f"Enter new title [{book.title}]: "
            ).strip()
            author = input(
                f"Enter new author [{book.author}]: "
            ).strip()
            category = input(
                f"Enter new category [{book.category}]: "
            ).strip()
            year = input(
                f"Enter publication year [{book.publication_year}]: "
            ).strip()
            copies = input(
                f"Enter total copies [{book.total_copies}]: "
            ).strip()
            if title:
                book.title = title
            if author:
                book.author = author
            if category:
                book.category = category
            if year:
                new_year = int(year)
                if new_year <= 0 or new_year > datetime.now().year:
                    raise ValueError("Invalid publication year.")
                book.publication_year = new_year
            if copies:
                new_total = int(copies)
                borrowed_copies = (
                    book.total_copies -
                    book.available_copies
                )
                if new_total < borrowed_copies:
                    raise ValueError(
                        "Total copies cannot be less than borrowed copies."
                    )
                book.total_copies = new_total
                book.available_copies = (
                    new_total - borrowed_copies
                )

            self.save_books()

            print("Book updated successfully.")

        except ValueError as error:
            print(f"Error: {error}")



    def delete_book(self):
        book_id = input("Enter Book ID to delete: ").strip()

        book = next(
            (
                book for book in self.books
                if book.book_id == book_id
            ),
            None
        )

        if not book:
            print("Book not found.")
            return

        active_borrowed = any(
            record.book_id == book_id
            and record.status == "Borrowed"
            for record in self.borrow_records
        )

        if active_borrowed:
            print(
                "Book cannot be deleted while currently borrowed."
            )
            return

        self.books.remove(book)
        self.save_books()

        print("Book deleted successfully.")

    def borrow_book(self):
        book_id = input("Enter Book ID: ").strip()

        book = next(
            (
                book for book in self.books
                if book.book_id == book_id
            ),
            None
        )

        if not book:
            print("Book does not exist.")
            return

        if book.available_copies <= 0:
            print("No copies available.")
            return

        borrower_name = input(
            "Enter Borrower's Name: "
        ).strip()

        if not borrower_name:
            print("Borrower's name cannot be empty.")
            return

        borrow_id = len(self.borrow_records) + 1

        record = BorrowRecord(
            borrow_id=borrow_id,
            book_id=book.book_id,
            book_title=book.title,
            borrower_name=borrower_name,
            borrow_date=datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
        self.borrow_records.append(record)
        book.available_copies -= 1
        self.save_books()
        self.save_borrow_records()
        print("Book borrowed successfully.")
        print(f"Borrow ID: {borrow_id}")
    def return_book(self):
        try:
            borrow_id = int(
                input("Enter Borrow ID: ")
            )
            record = next(
                (
                    record
                    for record in self.borrow_records
                    if record.borrow_id == borrow_id
                ),
                None
            )
            if not record:
                print("Borrow record not found.")
                return
            if record.status == "Returned":
                print("This book has already been returned.")
                return
            book = next(
                (
                    book for book in self.books
                    if book.book_id == record.book_id
                ),
                None
            )
            if book:
                book.available_copies += 1
                record.return_date = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            record.status = "Returned"
            self.save_books()
            self.save_borrow_records()
            print("Book returned successfully.")
        except ValueError:
            print("Invalid Borrow ID.")
    def view_borrowed_books(self):
        borrowed = [
            record
            for record in self.borrow_records
            if record.status == "Borrowed"
        ]
        if not borrowed:
            print("No books are currently borrowed.")
            return
        print("\n BORROWED BOOKS")
        for record in borrowed:
            print(f"""
Borrow ID: {record.borrow_id}
Book ID: {record.book_id}
Book Title: {record.book_title}
Borrower: {record.borrower_name}
Borrow Date: {record.borrow_date}
Status: {record.status}
""")
    def generate_report(self):
        total_books = len(self.books)
        total_available = sum(
            book.available_copies
            for book in self.books
        )
        total_borrowed = sum(
            book.total_copies - book.available_copies
            for book in self.books
        )
        category_count = Counter(
            book.category
            for book in self.books
        )
        borrowed_count = Counter(
            record.book_title
            for record in self.borrow_records
        )
        most_borrowed = (
            borrowed_count.most_common(1)[0]
            if borrowed_count
            else ("None", 0)
        )
        active_borrowers = len(
            set(
                record.borrower_name
                for record in self.borrow_records
                if record.status == "Borrowed"
            )
        )
        report = f"""
 LIBRARY REPORT 
Total Number of Books: {total_books}
Total Available Books: {total_available}
Total Borrowed Books: {total_borrowed}
Books in Each Category:
"""
        for category, count in category_count.items():
            report += f"- {category}: {count}\n"
        report += f"""
Most Borrowed Book: {most_borrowed[0]}
Times Borrowed: {most_borrowed[1]}
Number of Active Borrowers: {active_borrowers}
Timestamp:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        with open("library_report.txt", "w") as file:
            file.write(report)
print("Library report generated successfully.")