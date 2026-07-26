from library_manager import LibraryManager


def display_menu():
    print("""
========== Library Management ==========

1. Add Book
2. View Books
3. Search Book
4. Update Book
5. Delete Book
6. Borrow Book
7. Return Book
8. View Borrowed Books
9. Generate Report
10. Exit

========================================
""")


def main():

    library = LibraryManager()

    while True:

        display_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            library.add_book()

        elif choice == "2":
            library.view_books()

        elif choice == "3":
            library.search_book()

        elif choice == "4":
            library.update_book()

        elif choice == "5":
            library.delete_book()

        elif choice == "6":
            library.borrow_book()

        elif choice == "7":
            library.return_book()

        elif choice == "8":
            library.view_borrowed_books()

        elif choice == "9":
            library.generate_report()

        elif choice == "10":
            print("Thank you for using Library Management System.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()