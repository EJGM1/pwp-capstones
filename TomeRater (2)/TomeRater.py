class User(object):
    def __init__(self, name, email):
        if type(name) == str:
            self.name = name
        else:
            print("Name must be a string")
        if type(email) == str:
            if "@" not in email:
                print("Invalid email address")
            else:
                self.email = email
        else: print("Email must be a string")
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("The email address for {} has been updated to {}".format(self.name, self.email))

    def __repr__(self):
        return """User: {}
email: {}
Books read: {}""".format(self.name, self.email, self.books)

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

    def read_book(self, book, rating=None):
        self.books[book] = rating
    
    def get_average_rating(self):
        total = 0
        count = 0.0
        for value in self.books.values():
            if value != None:
                total += value
                count += 1
        if count > 0:
            return total / count
        else:
            print("User has not rated any books")
            return 0


class Book(object):
    def __init__(self, title, isbn):
        if type(title) == str:
            self.title = title
        else:
            print("Title must be a string")
        if type(isbn) == int:
            self.isbn = isbn
        else:
            print("ISBN must be a number")
        self.ratings = []
    
    def get_title(self):
        return self.title
    
    def get_isbn(self):
        return self.isbn
    
    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("The ISBN for {} has been updated to {}".format(self.title, self.isbn))

    def add_rating(self, rating):
        if rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid rating")
    
    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def get_average_rating(self):
        total = 0
        count = 0
        for item in self.ratings:
            total += item
            count += 1
        if count > 0:
            return total / count
        else:
            print("No ratings for this book")
            return 0

    def __hash__(self):
        return hash((self.title, self.isbn))
        
    def __repr__(self):
        return self.title


class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        if type(author) == str:
            self.author = author
        else:
            print("Author must be string")

    def get_author(self):
        return self.author
    
    def __repr__(self):
        return "{} by {}".format(self.title, self.author)


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        if type(subject) == str:
            self.subject = subject
        else:
            print("Subject must be a string")
        if type(level) == str:
            self.level = level
        else:
            print("Level  must be a string e.g. Advanced")
    
    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{}, a {} manual on {}".format(self.title, self.level, self.subject)


class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}
        self.password = "Password123"

    def create_book(self, title, isbn):
        book_instance = Book(title, isbn)
        return book_instance

    def create_novel(self, title, author, isbn):
        novel_instance = Fiction(title, author, isbn)
        return novel_instance

    def create_non_fiction(self, title, subject, level, isbn):
        non_fiction_instance = Non_Fiction(title, subject, level, isbn)
        return non_fiction_instance

    def add_book_to_user(self, book, email, rating=None):
        if email not in self.users.keys():
            print("No user with email {}".format(email))
        else:
            user_instance = self.users.get(email)
            user_instance.read_book(book, rating)
            if rating != None:
                book.add_rating(rating)
            if book in self.books.keys():
                self.books[book] = (self.books[book] + 1)
            else:
                self.books[book] = 1

    def add_user(self, name, email, user_books=None):
        if email in self.users.keys():
            connected_user = self.users[email]
            entered_password = input("This email is already connected to a user, to reveal the connected user please enter password: ")
            # This allows anyone with the password to view the User's name, the default Password is Password123, I've added a method to change the password
            if entered_password == self.password:
                print(connected_user.name)
            else:
                print("Incorrect password entered")
        else:
            new_user = User(name, email)
            self.users[email] = new_user
            if user_books != None:
                for item in user_books:
                    self.add_book_to_user(item, email)

    def print_catalog(self):
        for key in self.books.keys():
            print(key.title)
    
    def print_users(self):
        for value in self.users.values():
            print(value.name)

    def most_read_book(self):
        number_read = 0
        title = ""
        for key,value in self.books.items():
            if value > number_read:
                number_read = value
                title = key.title
            elif value == number_read:
                title = title + " and " + key.title
        print(title)

    def highest_rated_book(self):
        highest_rating = 0
        title = ""
        for key in self.books.keys():
            rating = key.get_average_rating()
            if rating > highest_rating:
                highest_rating = rating
                title = key.title
            elif rating == highest_rating:
                title = title + " and " + key.title
        print(title)

    def most_positive_user(self):
        highest_rating = 0
        user = ""
        for value in self.users.values():
            rating = value.get_average_rating()
            if rating > highest_rating:
                highest_rating = rating
                user = value.name
            elif rating == highest_rating:
                user = user + " and " + value.name
        print(user)

    def change_password(self):
        old_password = input("To change your password, please enter your current password: ")
        if old_password == self.password:
            new_pass1 = input("Please enter your new password: ")
            new_pass2 = input("Please re-enter your new password: ")
            if new_pass1 == new_pass2:
                self.password = new_pass1
                print("Your password has been updated")
            else:
                print("The passwords did not match, your password has not been updated")
        else:
            print("Incorrect password entered")

    def get_n_most_read_books(self, n):
        ordered = sorted(self.books, key=self.books.__getitem__, reverse=True)
        index = 0 
        while index < n:
            print(ordered[index])
            index += 1

