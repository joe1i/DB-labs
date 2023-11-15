import psycopg2
from data_fill import Data

class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='Arts Platform',
            user='postgres',
            password='qwerty',
            host='localhost',
            port=5432
        )
        self.data_fill = Data()
        self.create_random_data_table("styles", self.data_fill.styles)
        self.create_random_data_table("genres", self.data_fill.genres)
        self.create_random_data_table("countries", self.data_fill.countries)
        self.create_random_data_table("names", self.data_fill.names)
        self.create_random_data_table("surnames", self.data_fill.surnames)
        self.create_random_data_table("adjectives", self.data_fill.adjectives)
        self.create_random_data_table("nouns", self.data_fill.nouns)
        self.create_random_data_table("verbs", self.data_fill.verbs)

# -------- User
    def add_user(self, name, country, info):
        c = self.conn.cursor()
        c.execute('INSERT INTO "User" ("name", country, "info") VALUES (%s, %s, %s) RETURNING "userID"', (name, country, info))
        user_id = c.fetchone()[0]
        self.conn.commit()
        return user_id

    def get_all_users(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "User" ORDER BY "userID" ASC ')
        return c.fetchall()

    def edit_user(self, user_id, name, country, info):
        c = self.conn.cursor()
        c.execute('UPDATE "User" SET "name"=%s, "country"=%s, "info"=%s WHERE "userID"=%s', (name, country, info, user_id))
        self.conn.commit()

    def remove_user(self, user_id):
        c = self.conn.cursor()

        if self.get_artist(user_id):
            c.execute('DELETE FROM "Work of art" WHERE "creatorID"=%s', (user_id,))
            c.execute('DELETE FROM "Artist" WHERE "userID"=%s', (user_id,))
        elif self.get_collector(user_id):
            c.execute('UPDATE "Work of art" SET "buyerID"=NULL WHERE "buyerID"=%s',(user_id,))
            c.execute('DELETE FROM "Collector" WHERE "userID"=%s', (user_id,))

        c.execute('DELETE FROM "User" WHERE "userID"=%s', (user_id,))
        self.conn.commit()

# -------- Artist
    def add_artist(self, name, country, info):
        c = self.conn.cursor()
        userID = self.add_user(name, country, info)
        c.execute('INSERT INTO "Artist" ("userID") VALUES (%s)', (userID,))
        self.conn.commit()

    def get_all_artists(self):
        c = self.conn.cursor()
        c.execute('''SELECT U."userID", U."name", U."country", U."info" FROM "User" AS U
                             INNER JOIN "Artist" ON U."userID" = "Artist"."userID"
                             ORDER BY "userID" ASC ;''')
        return c.fetchall()

    def get_artist(self, user_id):
        c = self.conn.cursor()
        c.execute('''SELECT U."userID", U."name", U."country", U."info" FROM "User" AS U
                                   INNER JOIN "Artist" ON U."userID" = "Artist"."userID"
                                   WHERE "Artist"."userID" = %s;''', (user_id,))
        artist = c.fetchone()
        return artist

    def remove_artist(self, user_id):
        c = self.conn.cursor()

        c.execute('DELETE FROM "Work of art" WHERE "creatorID"=%s', (user_id,))
        c.execute('DELETE FROM "Artist" WHERE "userID"=%s', (user_id,))

        c.execute('DELETE FROM "User" WHERE "userID"=%s', (user_id,))
        self.conn.commit()

    def rand_fill_artist(self, count):
        c = self.conn.cursor()

        c.execute(f'''
        DO $$ 
        DECLARE
            i INT := 1;
        BEGIN
            WHILE i <= {count} LOOP
            
                WITH inserted_user AS (
                    INSERT INTO "User" ("name", country, "info") 
                    VALUES(
                        (SELECT "name" FROM names ORDER BY random() LIMIT 1)
                        || ' ' || 
                        (SELECT "name" FROM surnames ORDER BY random() LIMIT 1)
                        ,
                        (SELECT "name" FROM countries ORDER BY random() LIMIT 1)
                        , 
                        chr(trunc(65 + random()*26)::int)||chr(trunc(65 + random()*26)::int)||chr(trunc(65 + random()*26)::int)
                    )
                    RETURNING "userID"
                )
                
                INSERT INTO "Artist" ("userID") VALUES ((SELECT "userID" FROM inserted_user));

                i := i + 1;
            END LOOP;
        END $$;
        ''')

        self.conn.commit()

    def show_artists_arts(self, userID):
        c = self.conn.cursor()
        c.execute('''
        SELECT "artID", "name", price, "style", "genre", "buyerID" FROM "Work of art" 
        INNER JOIN "Artist" ON "Work of art"."creatorID" = "Artist"."userID"
        WHERE "Artist"."userID" = %s;
        ''', (userID,))
        return c.fetchall()

# -------- Collector
    def add_collector(self, name, country, info):
        c = self.conn.cursor()
        userID = self.add_user(name, country, info)
        c.execute('INSERT INTO "Collector" ("userID") VALUES (%s)', (userID,))
        self.conn.commit()

    def get_all_collectors(self):
        c = self.conn.cursor()
        c.execute('''SELECT U."userID", U."name", U."country", U."info" FROM "User" AS U
                     INNER JOIN "Collector" ON U."userID" = "Collector"."userID"
                     ORDER BY "userID" ASC ;''')
        return c.fetchall()

    def get_collector(self, user_id):
        c = self.conn.cursor()
        c.execute('''SELECT U."userID", U."name", U."country", U."info" FROM "User" AS U
                           INNER JOIN "Collector" ON U."userID" = "Collector"."userID"
                           WHERE "Collector"."userID" = %s;''',(user_id,))
        collector = c.fetchone()
        return collector

    def remove_collector(self, user_id):
        c = self.conn.cursor()

        c.execute('UPDATE "Work of art" SET "buyerID"=NULL WHERE "buyerID"=%s', (user_id,))
        c.execute('DELETE FROM "Collector" WHERE "userID"=%s', (user_id,))

        c.execute('DELETE FROM "User" WHERE "userID"=%s', (user_id,))
        self.conn.commit()

    def rand_fill_collector(self, count):
        c = self.conn.cursor()

        c.execute(f'''
        DO $$ 
        DECLARE
            i INT := 1;
        BEGIN
            WHILE i <= {count} LOOP

                WITH inserted_user AS (
                    INSERT INTO "User" ("name", country, "info") 
                    VALUES(
                        (SELECT "name" FROM names ORDER BY random() LIMIT 1)
                        || ' ' || 
                        (SELECT "name" FROM surnames ORDER BY random() LIMIT 1)
                        ,
                        (SELECT "name" FROM countries ORDER BY random() LIMIT 1)
                        , 
                        chr(trunc(65 + random()*26)::int)||chr(trunc(65 + random()*26)::int)||chr(trunc(65 + random()*26)::int)
                    )
                    RETURNING "userID"
                )

                INSERT INTO "Collector" ("userID") VALUES ((SELECT "userID" FROM inserted_user));

                i := i + 1;
            END LOOP;
        END $$;
        ''')

        self.conn.commit()

    def show_collectors_collection(self, userID):
        c = self.conn.cursor()
        c.execute('''
         SELECT "artID", "name", price, "style", "genre", "creatorID" FROM "Work of art" 
         INNER JOIN "Collector" ON "Work of art"."buyerID" = "Collector"."userID"
         WHERE "Collector"."userID" = %s;
         ''', (userID,))
        return c.fetchall()

# -------- Work of art
    def add_art(self, name, price, style, genre, creatorID):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO "Work of art" ("name", price, "style", "genre", "buyerID", "creatorID") VALUES (%s, %s, %s, %s, null, %s)', (name, price, style, genre, creatorID))
            self.conn.commit()
        except self.conn.Error as e:
            print("Виникла помилка під час виконання SQL-запиту:", e)

    def get_all_arts(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Work of art" ORDER BY "artID" ASC ')
        return c.fetchall()

    def get_art(self, art_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Work of art" WHERE "artID"=%s',(art_id,))
        art = c.fetchone()
        return art

    def edit_art(self, art_id, name, price, style, genre, buyerID, creatorID):
        c = self.conn.cursor()

        c.execute('UPDATE "Work of art" SET "name"=%s, price=%s, "style"=%s, "genre"=%s, "creatorID"=%s WHERE "artID"=%s', (name, price, style, genre, creatorID, art_id))

        if not buyerID:
            c.execute('UPDATE "Work of art" SET "buyerID"=null WHERE "artID"=%s', (art_id,))
        else:
            c.execute('UPDATE "Work of art" SET "buyerID"=%s WHERE "artID"=%s', (buyerID, art_id))

        self.conn.commit()

    def remove_art(self, art_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM "Work of art" WHERE "artID"=%s', (art_id,))
        self.conn.commit()

    def buy_art(self, buyer_id, art_id):
        c = self.conn.cursor()
        c.execute('UPDATE "Work of art" SET "buyerID"=%s WHERE "artID"=%s', (buyer_id, art_id))
        self.conn.commit()

    def get_arts_buyer(self, art_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Work of art" WHERE "artID"=%s', (art_id,))
        buyer_id = c.fetchone()[5]
        return buyer_id

    def rand_fill_arts(self, count):
        c = self.conn.cursor()

        c.execute(f'''
        DO $$ 
        DECLARE
            i INT := 1;
        BEGIN
            WHILE i <= {count} LOOP

                INSERT INTO "Work of art" ("name", price, "style", "genre", "buyerID", "creatorID") 
                VALUES(
                    (SELECT "name" FROM adjectives ORDER BY random() LIMIT 1)
                    || ' ' || 
                    (SELECT "name" FROM nouns ORDER BY random() LIMIT 1)
                    || ' ' || 
                    (SELECT "name" FROM verbs ORDER BY random() LIMIT 1)
                    ,
                    trunc(random()*100000)::int
                    , 
                    (SELECT "name" FROM styles ORDER BY random() LIMIT 1)
                    , 
                    (SELECT "name" FROM genres ORDER BY random() LIMIT 1)
                    , 
                    CASE WHEN random() < 0.5
                        THEN (SELECT "userID" FROM "Collector" ORDER BY random() LIMIT 1)
                        ELSE null
                    END,
                    (SELECT "userID" FROM "Artist" ORDER BY random() LIMIT 1)
                    );
                i := i + 1;
            END LOOP;
        END $$;
        ''')

        self.conn.commit()

# -------- Search
    def sort_by_price(self, price_from, price_to):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Work of art" WHERE price >= %s AND price <= %s ORDER BY price ASC', (price_from, price_to))
        return c.fetchall()

    def filter_by_price_style_genre(self, style, genre, price_from, price_to):
        c = self.conn.cursor()
        c.execute('''SELECT "artID", "name", "buyerID", "creatorID", price FROM "Work of art"
                            WHERE style = %s AND genre = %s AND price >= %s AND price <= %s
                            ''',
                        (style, genre, price_from, price_to))
        return c.fetchall()

    def filter_by_country_price(self, country, price_from, price_to, availability):
        c = self.conn.cursor()
        c.execute(f'''SELECT WA."artID", WA."name", WA."style", WA."genre", A."userID", WA.price
                            FROM "Work of art" AS WA
                            INNER JOIN "Artist" AS A ON WA."creatorID" = A."userID"
                            INNER JOIN "User" AS U ON A."userID" = U."userID"
                            WHERE U.country = %s AND 
                            CASE 
                                WHEN {availability} = true THEN WA."buyerID" IS NULL 
                                ELSE WA."buyerID" IS NOT NULL 
                            END
                            AND price >= %s AND price <= %s;
                            ''',
                        (country, price_from, price_to))
        return c.fetchall()

    def filter_by_most_exp_in_country(self):
        c = self.conn.cursor()
        c.execute('''
        WITH ranked_artworks AS (
            SELECT
                U.country,
                WA."artID",
                WA."name",
                WA."style",
                WA."genre",
                A."userID",
                WA.price,
                ROW_NUMBER() OVER (PARTITION BY U.country ORDER BY WA.price DESC) AS rank
            FROM
                "Work of art" AS WA
            INNER JOIN
                "Artist" AS A ON WA."creatorID" = A."userID"
            INNER JOIN
                "User" AS U ON A."userID" = U."userID"
            WHERE
                U.country IS NOT NULL 
        )
        SELECT
            country,
            "artID",
            "name",
            "style",
            "genre",
            "userID",
            price
        FROM
            ranked_artworks
        WHERE
            rank = 1;                   
        ''',)
        return c.fetchall()

# -------- Fill data

    def create_random_data_table(self, name, data):
        c = self.conn.cursor()
        c.execute('''
                    SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_name = %s
                    );
                ''', (name,))
        table_exists = c.fetchone()

        if not table_exists[0]:
            # SQL-запит для створення таблиці
            c.execute(f'''
                CREATE TABLE {name} (
                    id INTEGER PRIMARY KEY,
                    name TEXT
                );
                ''')

            # SQL-запит для вставки даних в таблицю
            for i, value in enumerate(data):
                c.execute(f'INSERT INTO {name} (id, name) VALUES (%s, %s)', (i, value,))

            # Збереження змін та закриття підключення
            self.conn.commit()
            print(f"Таблицю {name} створено та заповнено.")
        else:
            print(f"Таблиця {name} вже існує.")


