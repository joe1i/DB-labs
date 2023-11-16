import sys
from prettytable import PrettyTable


class View:

    def show_message(self, message):
        print(message)

    def get_user_input(self):
        name = self.input_text("Enter user name: ", True, 25)
        country = self.input_text("Enter user country: ", True, 25)
        info = self.input_arbitrary("Enter user info: ", True, 50)
        return name, country, info

    def get_art_input(self):
        name = self.input_arbitrary("Enter art name: ", True, 50)
        price = self.input_digit("Enter art price: ", True, sys.maxsize)
        style = self.input_text("Enter art style: ", True, 50)
        genre = self.input_text("Enter art genre: ", True, 50)
        return name, price, style, genre

    def show_users(self, users):
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Country", "Information"]
        for user in users:
            table.add_row([user[0], user[1], user[2], user[3]])
        print(table)

    def show_user(self, user):
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Country", "Information"]
        table.add_row([user[0], user[1], user[2], user[3]])
        print(table)

    def show_arts(self, arts):
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Price", "Style", "Genre", "Customer", "Author"]
        for art in arts:
            table.add_row([art[0], art[1], art[2], art[3], art[4], art[5], art[6]])
        print(table)

    def show_art(self, art):
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Price", "Style", "Genre", "Customer", "Author"]
        table.add_row([art[0], art[1], art[2], art[3], art[4], art[5], art[6]])
        print(table)

    def show_artists_arts(self, arts):
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Price", "Style", "Genre", "Customer"]
        for art in arts:
            table.add_row([art[0], art[1], art[2], art[3], art[4], art[5]])
        print(table)

    def show_collectors_collection(self, arts):
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Price", "Style", "Genre", "Author"]
        for art in arts:
            table.add_row([art[0], art[1], art[2], art[3], art[4], art[5]])
        print(table)

    def get_user_id(self):
        return self.input_digit("Enter user ID: ", True, sys.maxsize)

    def get_creator_id(self):
        return self.input_digit("Enter creator ID: ", True, sys.maxsize)

    def get_buyer_id(self):
        return self.input_digit("Enter buyer ID: ", False, sys.maxsize)

    def get_art_id(self):
        return self.input_digit("Enter art ID: ", True, sys.maxsize)

    def get_count(self):
        return self.input_digit("Enter count: ", True, sys.maxsize)

    def get_price_range(self):
        price_from = self.input_digit("Enter lowest price: ", True, sys.maxsize)
        price_to = self.input_digit("Enter highest price: ", True, sys.maxsize)
        return  price_from, price_to

    def get_genre(self):
        genre = self.input_text("Enter genre: ", True, 50)
        return genre

    def get_style(self):
        style = self.input_text("Enter style: ", True, 50)
        return style

    def get_country(self):
        country = self.input_text("Enter country: ", True, 25)
        return country

    def get_availability(self):
        availability = self.get_bool("Is available?")
        return availability

    def show_arts_filtered_by_price_style_genre(self, arts):
        print("Works of art:")
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Customer", "Author", "Price"]
        for art in arts:
            table.add_row([art[0], art[1], art[2], art[3], art[4]])
        print(table)

    def show_arts_filtered_by_country_price(self, arts, country):
        print("Works of art in " + country + ":")
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Style", "Genre", "Author", "Price"]
        for art in arts:
            table.add_row([art[0], art[1], art[2], art[3], art[4], art[5]])
        print(table)

    def show_arts_filtered_by_most_exp_in_country(self, arts):
        table = PrettyTable()
        table.field_names = ["Country", "ID", "Name", "Style", "Genre", "Author", "Price"]
        for art in arts:
            table.add_row([art[0], art[1], art[2], art[3], art[4], art[5], art[6]])
        print(table)

    def input_text(self, message, notnull, length):
        while True:
            text = input(message)
            if len(text) > length:
                print("Input data is too long! Try again.")
                continue
            if self.is_alpha_with_space(text) or (not text and notnull is False):
                return text
            print("Wrong input data! Try again.")

    def input_digit(self, message, notnull, length):
        while True:
            digits = input(message)
            if len(digits) > length:
                print("Input data is too long! Try again.")
                continue
            if digits.isdigit():
                return int(digits)
            elif not digits and notnull is False:
                return None
            print("Wrong input data! Try again.")

    def input_arbitrary(self, message, notnull, length):
        while True:
            text = input(message)
            if len(text) > length:
                print("Input data is too long! Try again.")
                continue
            if not text and notnull is True:
                print("Wrong input data! Try again.")
                continue
            return text

    def is_alpha_with_space(self, text):
        return all(char.isalpha() or char.isspace() for char in text)

    def get_bool(self, message):
        while True:
            print(message)
            print("1. True")
            print("2. False")
            choice = input("Enter your choice: ")
            if choice == '1':
                return True
            elif choice == '2':
                return False
            print("Wrong input data! Try again.")
