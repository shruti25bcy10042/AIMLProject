# Fetches book data from a given URL (assuming JSON format) and returns a list of book dictionaries
# Handles potential HTTP request and JSON parsing errors

import requests
import json

# Fetches book data from a given URL
def load_books_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        books_data = response.json()
        print(f"Successfully fetched {len(books_data)} books from {url}")
        return books_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {url}: {e}")
        return []


# Program of Library Management System
print("")
print("Execution of program starts from here : ")
print("")
class Book:
    # Initializes a new Book object with a title, author, and ISBN.
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False

    # Returns a string representation of the Book object.
    def __str__(self):
        status = "(Borrowed)" if self.is_borrowed else "(Available)"
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) {status}"

class Member:
    # Initializes a new Member object with a name and member ID.
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    # Returns a string representation of the Member object.
    def __str__(self):
        return f"Member: {self.name} (ID: {self.member_id}) - Borrowed Books: {len(self.borrowed_books)}"

class Library:
    # Initializes a new Library object with a name.
    def __init__(self, name):
        self.name = name
        self.books = {}
        self.members = {}

    # Adds a book to the library.
    def add_book(self, book):
        if book.isbn in self.books:
            print(f"Error: Book with ISBN {book.isbn} already exists.")
        else:
            self.books[book.isbn] = book
            print(f"Added book: {book.title}")

    # Removes a book from the library by its ISBN.
    def remove_book(self, isbn):
        if isbn in self.books:
            book = self.books.pop(isbn)
            print(f"Removed book: {book.title}")
        else:
            print(f"Error: Book with ISBN {isbn} not found.")

    # Adds a member to the library.
    def add_member(self, member):
        if member.member_id in self.members:
            print(f"Error: Member with ID {member.member_id} already exists.")
        else:
            self.members[member.member_id] = member
            print(f"Added member: {member.name}")

    # Removes a member from the library by their ID.
    def remove_member(self, member_id):
        if member_id in self.members:
            member = self.members.pop(member_id)
            print(f"Removed member: {member.name}")
        else:
            print(f"Error: Member with ID {member_id} not found.")

    # Allows a member to borrow a book.
    def borrow_book(self, member_id, isbn):
        member = self.members.get(member_id)
        book = self.books.get(isbn)

        if not member:
            print(f"Error: Member with ID {member_id} not found.")
        elif not book:
            print(f"Error: Book with ISBN {isbn} not found.")
        elif book.is_borrowed:
            print(f"Error: '{book.title}' is already borrowed.")
        else:
            book.is_borrowed = True
            member.borrowed_books.append(book)
            print(f"'{book.title}' borrowed by {member.name}.")

    # Allows a member to return a borrowed book.
    def return_book(self, member_id, isbn):
        member = self.members.get(member_id)
        book = self.books.get(isbn)

        if not member:
            print(f"Error: Member with ID {member_id} not found.")
        elif not book:
            print(f"Error: Book with ISBN {isbn} not found.")
        elif not book.is_borrowed:
            print(f"Error: '{book.title}' was not borrowed.")
        elif book not in member.borrowed_books:
            print(f"Error: '{book.title}' was not borrowed by {member.name}.")
        else:
            book.is_borrowed = False
            member.borrowed_books.remove(book)
            print(f"'{book.title}' returned by {member.name}.")

    # Lists all books in the library.
    def list_all_books(self):
        print("\n--- All Books ---")
        if not self.books:
            print("No books in the library.")
        for book in self.books.values():
            print(book)

    # Lists all available books in the library.
    def list_available_books(self):
        print("\n--- Available Books ---")
        available_books = [book for book in self.books.values() if not book.is_borrowed]
        if not available_books:
            print("No books currently available.")
        for book in available_books:
            print(book)

    # Lists all borrowed books in the library.
    def list_borrowed_books(self):
        print("\n--- Borrowed Books ---")
        borrowed_books = [book for book in self.books.values() if book.is_borrowed]
        if not borrowed_books:
            print("No books currently borrowed.")
        for book in borrowed_books:
            print(book)

    # Lists all members and their borrowed books.
    def list_all_members(self):
        print("\n--- All Members ---")
        if not self.members:
            print("No members registered.")
        for member in self.members.values():
            print(member)
            if member.borrowed_books:
                print("  Borrowed:")
                for book in member.borrowed_books:
                    print(f"    - {book.title}")

# Runs the main interactive library system menu.
def run_library_system():
    library_name = input("Enter the name of the library: ")
    my_library = Library(library_name)

    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Add Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. List All Books")
        print("6. List Available Books")
        print("7. List Borrowed Books")
        print("8. List All Members")
        print("9. Remove Book")
        print("10. Remove Member")
        print("11. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            new_book = Book(title, author, isbn)
            my_library.add_book(new_book)
        elif choice == '2':
            name = input("Enter member name: ")
            member_id = input("Enter member ID: ")
            new_member = Member(name, member_id)
            my_library.add_member(new_member)
        elif choice == '3':
            member_id = input("Enter member ID: ")
            isbn = input("Enter book ISBN to borrow: ")
            my_library.borrow_book(member_id, isbn)
        elif choice == '4':
            member_id = input("Enter member ID: ")
            isbn = input("Enter book ISBN to return: ")
            my_library.return_book(member_id, isbn)
        elif choice == '5':
            my_library.list_all_books()
        elif choice == '6':
            my_library.list_available_books()
        elif choice == '7':
            my_library.list_borrowed_books()
        elif choice == '8':
            my_library.list_all_members()
        elif choice == '9':
            isbn = input("Enter ISBN of the book to remove: ")
            my_library.remove_book(isbn)
        elif choice == '10':
            member_id = input("Enter ID of the member to remove: ")
            my_library.remove_member(member_id)
        elif choice == '11':
            print("Exiting Library Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    run_library_system()


# ARJUN MISHRA 25BCY10063