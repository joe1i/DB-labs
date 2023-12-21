import psycopg2
from data_fill import Data
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'User'

    userID = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    info = Column(String)
    artist = relationship('ArtistModel', uselist=False, back_populates='user')
    collector = relationship('CollectorModel', uselist=False, back_populates='user')


class ArtistModel(Base):
    __tablename__ = 'Artist'

    userID = Column(Integer, ForeignKey('User.userID'), primary_key=True)
    user = relationship('UserModel', back_populates='artist')
    art_created = relationship('ArtModel', foreign_keys='ArtModel.creatorID', back_populates='creator')


class CollectorModel(Base):
    __tablename__ = 'Collector'

    userID = Column(Integer, ForeignKey('User.userID'), primary_key=True)
    user = relationship('UserModel', back_populates='collector')
    art_purchased = relationship('ArtModel', foreign_keys='ArtModel.buyerID', back_populates='buyer')


class ArtModel(Base):
    __tablename__ = 'Work of art'

    artID = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    style = Column(String)
    genre = Column(String)
    buyerID = Column(Integer, ForeignKey('Collector.userID'))
    creatorID = Column(Integer, ForeignKey('Artist.userID'))
    buyer = relationship('CollectorModel', foreign_keys=[buyerID], back_populates='art_purchased')
    creator = relationship('ArtistModel', foreign_keys=[creatorID], back_populates='art_created')


class Model:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
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

        # Підключення до бази даних з використанням SQLAlchemy
        self.engine = create_engine(
            f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}',
            echo=True
        )
        Base.metadata.create_all(self.engine)


# -------- User
    def add_user(self, name, country, info):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        new_user = UserModel(name=name, country=country, info=info)
        session.add(new_user)
        session.commit()

        return new_user.userID

    def get_all_users(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        users = session.query(UserModel.userID, UserModel.name, UserModel.country, UserModel.info).all()
        return users

    def edit_user(self, user_id, name, country, info):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        user_to_edit = session.query(UserModel).filter_by(userID=user_id).first()

        if user_to_edit:
            user_to_edit.name = name
            user_to_edit.country = country
            user_to_edit.info = info
            session.commit()

        session.close()

# -------- Artist
    def add_artist(self, name, country, info):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        new_user = UserModel(name=name, country=country, info=info)
        session.add(new_user)
        session.commit()

        new_artist = ArtistModel(user=new_user)
        session.add(new_artist)
        session.commit()

        return new_artist.userID

    def get_all_artists(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        artists = (
            session.query(UserModel.userID, UserModel.name, UserModel.country, UserModel.info)
            .join(ArtistModel, UserModel.userID == ArtistModel.userID)
            .order_by(UserModel.userID.asc())
            .all()
        )

        session.close()
        return artists

    def get_artist(self, user_id):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        artist = (
            session.query(UserModel.userID, UserModel.name, UserModel.country, UserModel.info)
            .join(ArtistModel, UserModel.userID == ArtistModel.userID)
            .filter(ArtistModel.userID == user_id)
            .first()
        )

        session.close()
        return artist

    def remove_artist(self, user_id):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        session.query(ArtModel).filter_by(creatorID=user_id).delete()
        session.query(ArtistModel).filter_by(userID=user_id).delete()
        session.query(UserModel).filter_by(userID=user_id).delete()

        session.commit()
        session.close()

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
        Session = sessionmaker(bind=self.engine)
        session = Session()

        new_user = UserModel(name=name, country=country, info=info)
        session.add(new_user)
        session.commit()

        new_collector = CollectorModel(user=new_user)
        session.add(new_collector)
        session.commit()

        return new_collector.userID

    def get_all_collectors(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        collectors = (
            session.query(UserModel.userID, UserModel.name, UserModel.country, UserModel.info)
            .join(CollectorModel, UserModel.userID == CollectorModel.userID)
            .order_by(UserModel.userID.asc())
            .all()
        )

        session.close()
        return collectors

    def get_collector(self, user_id):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        collector = (
            session.query(UserModel.userID, UserModel.name, UserModel.country, UserModel.info)
            .join(CollectorModel, UserModel.userID == CollectorModel.userID)
            .filter(CollectorModel.userID == user_id)
            .first()
        )

        session.close()
        return collector

    def remove_collector(self, user_id):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        session.query(ArtModel).filter_by(buyerID=user_id).update({ArtModel.buyerID: None})
        session.query(CollectorModel).filter_by(userID=user_id).delete()
        session.query(UserModel).filter_by(userID=user_id).delete()

        session.commit()
        session.close()

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
        Session = sessionmaker(bind=self.engine)
        session = Session()

        new_art = ArtModel(name=name, price=price, style=style, genre=genre, creatorID=creatorID, buyerID=None)
        session.add(new_art)
        session.commit()


    def get_all_arts(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        arts = session.query(
                ArtModel.artID,
                ArtModel.name,
                ArtModel.price,
                ArtModel.style,
                ArtModel.genre,
                ArtModel.buyerID,
                ArtModel.creatorID).all()

        session.close()
        return arts

    def get_art(self, art_id):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        art = session.query(
            ArtModel.artID,
            ArtModel.name,
            ArtModel.price,
            ArtModel.style,
            ArtModel.genre,
            ArtModel.buyerID,
            ArtModel.creatorID).filter_by(artID=art_id).first()

        session.close()
        return art

    def edit_art(self, art_id, name, price, style, genre, buyerID, creatorID):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        art = session.query(ArtModel).filter_by(artID=art_id).first()

        if art:
            art.name = name
            art.price = price
            art.style = style
            art.genre = genre
            art.creatorID = creatorID
            art.buyerID = buyerID

            session.commit()

        session.close()

    def remove_art(self, art_id):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        session.query(ArtModel).filter_by(artID=art_id).delete()

        session.commit()
        session.close()

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
            c.execute(f'''
                CREATE TABLE {name} (
                    id INTEGER PRIMARY KEY,
                    name TEXT
                );
                ''')

            for i, value in enumerate(data):
                c.execute(f'INSERT INTO {name} (id, name) VALUES (%s, %s)', (i, value,))

            self.conn.commit()
            print(f"Таблицю {name} створено та заповнено.")
        else:
            print(f"Таблиця {name} вже існує.")


