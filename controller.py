from model import Model
from view import View
from data_fill import Data
import time

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.data_fill = Data()

# ---- Menu

# -------- Main menu
    def main_run(self):
        while True:
            choice = self.show_main_menu()
            if choice == '1':
                self.users_menu()
            elif choice == '2':
                self.arts_menu()
            elif choice == '3':
                self.search_menu()

            elif choice == '4':
                break

    def show_main_menu(self):
        self.view.show_message("\nMenu:")
        self.view.show_message("1. User")
        self.view.show_message("2. Work of art")
        self.view.show_message("3. Search")

        self.view.show_message("4. Quit")
        return input("Enter your choice: ")

# -------- User
    def users_menu(self):
        while True:
            choice = self.show_users_menu()
            if choice == '1':
                self.artist_menu()
            elif choice == '2':
                self.collector_menu()
            elif choice == '3':
                self.show_all_users()

            elif choice == '4':
                break

    def show_users_menu(self):
        self.view.show_message("\nUsers:")
        self.view.show_message("1. Artist")
        self.view.show_message("2. Collector")
        self.view.show_message("3. Show all users")

        self.view.show_message("4. back")

        return input("Enter your choice: ")

# ------- Artist

    def artist_menu(self):
        while True:
            choice = self.show_artist_menu()
            if choice == '1':
                self.artist_show_menu()
            elif choice == '2':
                self.add_artist()
            elif choice == '3':
                self.edit_artist()
            elif choice == '4':
                self.remove_artist()
            elif choice == '5':
                self.rand_fill_artist()
            elif choice == '6':
                self.show_artists_arts()

            elif choice == '7':
                break

    def show_artist_menu(self):
        self.view.show_message("\nUsers.Artist:")
        self.view.show_message("1. show")
        self.view.show_message("2. add")
        self.view.show_message("3. edit")
        self.view.show_message("4. remove")
        self.view.show_message("5. random fill")
        self.view.show_message("6. show artist`s arts")

        self.view.show_message("7. back")

        return input("Enter your choice: ")

    def artist_show_menu(self):
        while True:
            choice = self.show_artist_show_menu()
            if choice == '1':
                self.show_current_artist()
            elif choice == '2':
                self.show_all_artists()

            elif choice == '3':
                break

    def show_artist_show_menu(self):
        self.view.show_message("\nUsers.Artist.show")
        self.view.show_message("1. show current artist")
        self.view.show_message("2. show all artists")

        self.view.show_message("3. back")

        return input("Enter your choice: ")

# -------- Collector
    def collector_menu(self):
        while True:
            choice = self.show_collector_menu()
            if choice == '1':
                self.collector_show_menu()
            elif choice == '2':
                self.add_collector()
            elif choice == '3':
                self.edit_collector()
            elif choice == '4':
                self.remove_collector()
            elif choice == '5':
                self.rand_fill_collector()
            elif choice == '6':
                self.show_collectors_collection()

            elif choice == '7':
                break

    def show_collector_menu(self):
        self.view.show_message("\nUsers.Collector:")
        self.view.show_message("1. show")
        self.view.show_message("2. add")
        self.view.show_message("3. edit")
        self.view.show_message("4. remove")
        self.view.show_message("5. random fill")
        self.view.show_message("6. show collector`s collection")

        self.view.show_message("7. back")

        return input("Enter your choice: ")

    def collector_show_menu(self):
        while True:
            choice = self.show_collector_show_menu()
            if choice == '1':
                self.show_current_collector()
            elif choice == '2':
                self.show_all_collectors()

            elif choice == '3':
                break

    def show_collector_show_menu(self):
        self.view.show_message("\nUsers.Collector.show")
        self.view.show_message("1. show current collector")
        self.view.show_message("2. show all collectors")

        self.view.show_message("3. back")

        return input("Enter your choice: ")

# -------- Work of art
    def arts_menu(self):
        while True:
            choice = self.show_art_menu()
            if choice == '1':
                self.art_show_menu()
            elif choice == '2':
                self.add_art()
            elif choice == '3':
                self.edit_art()
            elif choice == '4':
                self.remove_art()
            elif choice == '5':
                self.rand_fill_arts()
            elif choice == '6':
                self.buy_art()

            elif choice == '7':
                break

    def show_art_menu(self):
        self.view.show_message("\nWork of art:")
        self.view.show_message("1. show")
        self.view.show_message("2. add")
        self.view.show_message("3. edit")
        self.view.show_message("4. remove")
        self.view.show_message("5. random fill")
        self.view.show_message("6. buy")

        self.view.show_message("7. back")

        return input("Enter your choice: ")

    def art_show_menu(self):
        while True:
            choice = self.show_art_show_menu()
            if choice == '1':
                self.show_current_art()
            elif choice == '2':
                self.show_all_arts()

            elif choice == '3':
                break

    def show_art_show_menu(self):
        self.view.show_message("\nWork of art.show")
        self.view.show_message("1. show current work of art")
        self.view.show_message("2. show all works of art")

        self.view.show_message("3. back")

        return input("Enter your choice: ")

# -------- Search
    def search_menu(self):
        while True:
            choice = self.show_search_menu()
            if choice == '1':
                self.filter_by_price_style_genre()
            elif choice == '2':
                self.filter_by_country_price()
            elif choice == '3':
                self.filter_by_most_exp_in_country()
            elif choice == '4':
                break

    def show_search_menu(self):
        self.view.show_message("\nSearch:")
        self.view.show_message("1. search by style, genre, price")
        self.view.show_message("2. search by country, availability, price")
        self.view.show_message("3. search for each country's most expensive work of art")

        self.view.show_message("4. back")

        return input("Enter your choice: ")

# ---- Operations

# -------- User
    def show_all_users(self):
        users = self.model.get_all_users()
        if users:
            self.view.show_users(users)
        else:
            self.view.show_message("There is no users!")

# -------- Artist

    def show_current_artist(self):
        user_id = self.view.get_user_id()
        artist = self.model.get_artist(user_id)
        if artist:
            self.view.show_user(artist)
        else:
            self.view.show_message("There is no artist with this id!")

    def show_all_artists(self):
        artists = self.model.get_all_artists()
        if artists:
            self.view.show_users(artists)
        else:
            self.view.show_message("There are no artists!")

    def add_artist(self):
        name, country, info = self.view.get_user_input()
        self.model.add_artist(name, country, info)
        self.view.show_message("Artist added successfully!")

    def edit_artist(self):
        user_id = self.view.get_user_id()
        if not self.model.get_artist(user_id):
            self.view.show_message("There is no artist with this id!")
            return
        name, country, info = self.view.get_user_input()
        self.model.edit_user(user_id, name, country, info)
        self.view.show_message("Artist edited successfully!")

    def remove_artist(self):
        user_id = self.view.get_user_id()
        if not self.model.get_artist(user_id):
            self.view.show_message("There is no artist with this id!")
            return
        self.model.remove_artist(user_id)
        self.view.show_message("Artist deleted successfully!")

    def rand_fill_artist(self):
        count = self.view.get_count()
        self.model.rand_fill_artist(count)
        self.view.show_message(f"{count} artists added successfully!")

    def show_artists_arts(self):
        user_id = self.view.get_user_id()
        if not self.model.get_artist(user_id):
            self.view.show_message("There is no artist with this id!")
            return
        arts = self.model.show_artists_arts(user_id)
        if arts:
            self.view.show_artists_arts(arts)
        else:
            self.view.show_message("This artist has no works of art!")

# -------- Collector
    def show_current_collector(self):
        user_id = self.view.get_user_id()
        collector = self.model.get_collector(user_id)
        if collector:
            self.view.show_user(collector)
        else:
            self.view.show_message("There is no collector with this id!")

    def show_all_collectors(self):
        collectors = self.model.get_all_collectors()
        if collectors:
            self.view.show_users(collectors)
        else:
            self.view.show_message("There are no collectors!")

    def add_collector(self):
        name, country, info = self.view.get_user_input()
        self.model.add_collector(name, country, info)
        self.view.show_message("Collector added successfully!")

    def edit_collector(self):
        user_id = self.view.get_user_id()
        if not self.model.get_collector(user_id):
            self.view.show_message("There is no collector with this id!")
            return
        name, country, info = self.view.get_user_input()
        self.model.edit_user(user_id, name, country, info)
        self.view.show_message("Collector edited successfully!")

    def remove_collector(self):
        user_id = self.view.get_user_id()
        if not self.model.get_collector(user_id):
            self.view.show_message("There is no collector with this id!")
            return
        self.model.remove_collector(user_id)
        self.view.show_message("Collector deleted successfully!")

    def rand_fill_collector(self):
        count = self.view.get_count()
        self.model.rand_fill_collector(count)
        self.view.show_message(f"{count} collectors added successfully!")

    def show_collectors_collection(self):
        user_id = self.view.get_user_id()
        if not self.model.get_collector(user_id):
            self.view.show_message("There is no collector with this id!")
            return
        arts = self.model.show_collectors_collection(user_id)
        if arts:
            self.view.show_collectors_collection(arts)
        else:
            self.view.show_message("This collector has no works of art!")

# -------- Work of art
    def show_current_art(self):
        art_id = self.view.get_art_id()
        art = self.model.get_art(art_id)
        if art:
            self.view.show_art(art)
        else:
            self.view.show_message("There is no art with this id!")

    def show_all_arts(self):
        arts = self.model.get_all_arts()
        if arts:
            self.view.show_arts(arts)
        else:
            self.view.show_message("There are no arts!")

    def add_art(self):
        name, price, style, genre = self.view.get_art_input()
        creatorID = self.view.get_creator_id()
        if not self.model.get_artist(creatorID):
            self.view.show_message("There is no artist with this id!")
            return
        self.model.add_art(name, price, style, genre, creatorID)
        self.view.show_message("Art added successfully!")

    def edit_art(self):
        art_id = self.view.get_art_id()
        if not self.model.get_art(art_id):
            self.view.show_message("There is no art with this id!")
            return
        name, price, style, genre = self.view.get_art_input()
        creatorID = self.view.get_creator_id()
        if not self.model.get_artist(creatorID):
            self.view.show_message("There is no artist with this id!")
            return
        buyerID = self.view.get_buyer_id()
        if buyerID and not self.model.get_collector(creatorID):
            self.view.show_message("There is no collector with this id!")
            return
        self.model.edit_art(art_id, name, price, style, genre, buyerID, creatorID)
        self.view.show_message("Art edited successfully!")

    def remove_art(self):
        art_id = self.view.get_art_id()
        if not self.model.get_art(art_id):
            self.view.show_message("There is no art with this id!")
            return
        self.model.remove_art(art_id)
        self.view.show_message("Art deleted successfully!")

    def buy_art(self):
        art_id = self.view.get_art_id()
        if not self.model.get_art(art_id):
            self.view.show_message("There is no art with this id!")
            return

        if self.model.get_arts_buyer(art_id):
            self.view.show_message("This art is already bought!")
            return

        buyer_id = self.view.get_buyer_id()
        if self.model.get_collector(buyer_id):
            self.model.buy_art(buyer_id, art_id)
            self.view.show_message("Art was bought successfully!")
        else:
            self.view.show_message("There is no collector with this id!")

    def rand_fill_arts(self):
        count = self.view.get_count()
        artists = self.model.get_all_artists()
        if not artists:
            self.view.show_message("Works of art cannot be added because there are no artists!")
            return

        self.model.rand_fill_arts(count)
        self.view.show_message(f"{count} works of art added successfully!")

# -------- Search
    def sort_by_price(self):
        price_from, price_to = self.view.get_price_range()
        arts = self.model.sort_by_price(price_from, price_to)
        self.view.show_arts(arts)

    def filter_by_price_style_genre(self):
        style = self.view.get_style()
        genre = self.view.get_genre()
        price_from, price_to = self.view.get_price_range()
        start_time = time.time()
        arts = self.model.filter_by_price_style_genre(style, genre, price_from, price_to)
        if not arts:
            self.view.show_message("There are no works of art with those parameters!")
            return
        end_time = time.time()
        self.view.show_arts_filtered_by_price_style_genre(arts)
        execution_time = (end_time - start_time) * 1000
        self.view.show_message(f"Час виконання запиту: {execution_time:.4f} мс")

    def filter_by_country_price(self):
        country = self.view.get_country()
        price_from, price_to = self.view.get_price_range()
        availability = self.view.get_availability()
        start_time = time.time()
        arts = self.model.filter_by_country_price(country, price_from, price_to, availability)
        if not arts:
            self.view.show_message("There are no works of art with those parameters!")
            return

        end_time = time.time()
        self.view.show_arts_filtered_by_country_price(arts, country)


        execution_time = (end_time - start_time) * 1000
        self.view.show_message(f"Час виконання запиту: {execution_time:.4f} мс")

    def filter_by_most_exp_in_country(self):
        start_time = time.time()
        arts = self.model.filter_by_most_exp_in_country()
        if not arts:
            self.view.show_message("There are no works of art with those parameters!")
            return

        end_time = time.time()
        self.view.show_arts_filtered_by_most_exp_in_country(arts)

        execution_time = (end_time - start_time) * 1000
        self.view.show_message(f"Час виконання запиту: {execution_time:.4f} мс")

# -------- Getters
    def get_style(self):
        j = 5
        for i, value in enumerate(self.data_fill.styles):
            print(f"{i+1}. {value}   ", end="")
            j = j - 1
            if j == 0:
                j = 5
                print()

        while True:
            choice = int(input("Enter your choice: "))
            if choice < 1 or choice > len(self.data_fill.styles):
                self.view.show_message("Wrong value!")
            else:
                return self.data_fill.styles[choice - 1]
