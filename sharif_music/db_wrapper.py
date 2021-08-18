import threading

from sharif_music.models import *
from datetime import datetime
import sqlite3


class DB:
    def get_connection(self) -> sqlite3.Connection:
        thread_id = threading.get_ident()
        if thread_id not in self.connections:
            self.connections[thread_id] = sqlite3.connect('/var/tmp/shm.db')
        return self.connections[thread_id]
    def __init__(self):
        self.connections = {}
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS all_users (
                ID INT PRIMARY KEY,
                name varchar(20) NOT NULL,
                username varchar(20) NOT NULL,
                password varchar(20) NOT NULL,
                description varchar(300) NOT NULL,
                email varchar(20) NOT NULL,
                is_account_premium varchar(20) NOT NULL,
                user_photo varchar(512),
                is_publisher varchar(3)
                )""")
        conn.commit()
        # is publisher: yes/no

        c.execute("""CREATE TABLE IF NOT EXISTS payment (
            date_of_payment date,
            payer_id INT PRIMARY KEY, 
            payment_group varchar(20) NOT NULL,
            description varchar(300) NOT NULL,
            FOREIGN KEY (payer_id) REFERENCES all_users(ID)
                )""")
        conn.commit()

        c.execute("""CREATE TABLE IF NOT EXISTS person_has_playlist (
            user_id INT, 
            playlist_id INT,
            PRIMARY KEY (user_id, playlist_id),
            FOREIGN KEY (user_id) REFERENCES all_users(ID),
            FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id)

        )""")
        conn.commit()

        c.execute("""CREATE TABLE IF NOT EXISTS playlist (
            playlist_id INT,
            creator_id INT NOT NULL,
            creation_date date NOT NULL,
            PRIMARY KEY(playlist_id),
            FOREIGN KEY (creator_id) REFERENCES all_users(ID)

        )""")
        conn.commit()

        c.execute("""CREATE TABLE IF NOT EXISTS music_in_playlist (
            music_id INT NOT NULL, 
            playlist_id INT NOT NULL,
            PRIMARY KEY (music_id, playlist_id),
            FOREIGN KEY (music_id) REFERENCES music(music_id),
            FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id)

        )""")
        conn.commit()

        c.execute("""CREATE TABLE IF NOT EXISTS music (
            music_id INT PRIMARY KEY,
            name varchar(20) NOT NULL,
            publisher_id INT NOT NULL,
            genre varchar(20) NOT NULL,
            date_of_creation date NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES all_users(ID)
        )""")
        conn.commit()

        c.execute("""CREATE TABLE IF NOT EXISTS playable_music (
            music_id INT NOT NULL,
            quality varchar(5) NOT NULL,
            file_address varchar(512) NOT NULL,
            FOREIGN KEY (music_id) REFERENCES music(music_id)
        )""")
        conn.commit()

        # c.execute("""CREATE TABLE publisher (
        #     user_id INT PRIMARY KEY,
        #     username varchar(20) NOT NULL,
        #     password varchar(20) NOT NULL
        # )""")
        # conn.commit()

        c.execute("""CREATE TABLE IF NOT EXISTS user_follow_publisher (
            user_id INT NOT NULL,
            publisher_id INT NOT NULL,
            date_of_following date NOT NULL,
            PRIMARY KEY (user_id, publisher_id),
           FOREIGN KEY (publisher_id) REFERENCES all_users(ID),
            FOREIGN KEY (user_id) REFERENCES all_users(ID)
        )""")
        conn.commit()

        c.execute("""
            CREATE TABLE IF NOT EXISTS files (
            id INT NOT NULL,
            mime varchar(300) NOT NULL,
            path varchar(300) NOT NULL,
            PRIMARY KEY (id)
        )""")
        conn.commit()


    def bool_to_str(self, a):
        if a == True:
            return 'yes'
        else:
            return 'no'

    def insert_account(self, account: Account) -> None:
        with self.get_connection() as conn:
            conn.cursor().execute("INSERT INTO all_users VALUES "
                           "(:ID, :name, :username, :password, :description, :email, :is_account_premium, :user_photo, :is_publisher)",
                           {'ID': account.id, 'name': account.name, 'username': account.username,
                            'password': account.password,
                            'description': account.description, 'email': account.email, 'is_account_premium':
                                self.bool_to_str(account.account_type == AccountType.PREMIUM),
                            'user_photo': account.photo, 'is_publisher': account.publisher})

    # reqs is a dictionary which maps property to value like
    # {name: 'asghar', is_account_premium: 'yes'}
    # then the select returns all accounts in this format
    def select_accounts(self, q) -> List[Account]:
        query = "SELECT * FROM all_users WHERE "
        for i, key in enumerate(q):
            query += key + "=:" + key
            if i != len(q) - 1:
                query += " AND "
        # print(query)
        cursor = self.get_connection().cursor()
        cursor.execute(query, q)
        return cursor.fetchall()

    def select_all_accounts(self) -> List[Account]:
        return self.get_connection().cursor().execute("SELECT * FROM all_users").fetchall()

    def update_account(self, account: Account, updated_fields):

        query = "UPDATE all_users SET "
        for i, key in enumerate(updated_fields):
            query += key + "=:" + key
            if i != len(updated_fields) - 1:
                query += " AND "
        " WHERE ID=:ID"
        updated_fields['ID'] = account.id
        with self.get_connection() as conn:
            conn.cursor().execute(query, updated_fields)

    #####
    def add_file(self, file: File):
        with self.get_connection() as conn:
            conn.cursor().execute("INSERT INTO files VALUES"
                           "(:id, :mime, :path)",
                           {'id': file.id, 'mime': file.mime, 'path': file.path})

    def select_files(self, q) -> List[File]:
        query = "SELECT * FROM files WHERE "
        for i, key in enumerate(q):
            query += key + "=:" + key
            if i != len(q) - 1:
                query += " AND "
        # print(query)
        c = self.get_connection().cursor()
        c.execute(query, q)
        return c.fetchall()

    ####

    def insert_playlist(self, playlist: PlayList) -> None:
        # affects person_has_playlist
        # music_in_playlist
        # playlist
        for owner in playlist.owners:
            with self.get_connection() as conn:
                conn.cursor().execute("INSERT INTO person_has_playlist VALUES"
                               "(:user_id, :playlist_id)",
                               {'user_id': owner.id, 'playlist_id': playlist.uid})
        for music in playlist.musics:
            with self.get_connection() as conn:
                conn.cursor().execute("INSERT INTO music_in_playlist VALUES"
                               "(:music_id, :playlist_id)",
                               {'music_id': music.uid, 'playlist_id': playlist.uid})
        # print(playlist.uid)
        # print(datetime.now())
        with self.get_connection() as conn:
            conn.cursor().execute("INSERT INTO playlist VALUES"
                           "(:playlist_id, :creator_id, :creation_date)",
                           {'playlist_id': playlist.uid, 'creator_id': playlist.owners[0].id,
                            'creation_date': datetime.now()})
        pass

    def delete_playlist(self, playlist_id: int) -> None:
        with self.get_connection() as conn:
            conn.cursor().execute("DELETE from playlist WHERE playlist_id:=playlist_id", {'playlist_id': playlist_id})
        with self.get_connection() as conn:
            conn.cursor().execute("DELETE from person_has_playlist WHERE playlist_id:=playlist_id",
                           {'playlist_id': playlist_id})
        with self.get_connection() as conn:
            conn.cursor().execute("DELETE from music_in_playlist WHERE playlist_id:=playlist_id", {'playlist_id': playlist_id})

    def insert_new_music_to_playlist(self, playlist_id: int, new_music_id: int):
        with self.get_connection() as conn:
            conn.cursor().execute("INSERT INTO music_in_playlist VALUES"
                           "(:music_id, :playlist_id)",
                           {'music_id': new_music_id, 'playlist_id': playlist_id})

    def delete_music_from_playlist(self, playlist_id: int, music_to_remove_id: int):
        with self.get_connection() as conn:
            conn.cursor().execute("DELETE from music_in_playlist WHERE "
                           "playlist_id:=playlist_id, music_id:=music_id",
                           {'playlist_id': playlist_id, 'music_id': music_to_remove_id})

    def insert_new_owner_to_playlist(self, playlist_id: int, owner_id: int):
        with self.get_connection() as conn:
            conn.cursor().execute("INSERT INTO person_has_playlist VALUES"
                           "(:user_id, :playlist_id)",
                           {'user_id': owner_id, 'playlist_id': playlist_id})

    def select_playlists(self, q) -> List[int]:

        pass

    #####
    def insert_music(self, music: Music) -> None:
        self.add_file(music.file)
        with self.get_connection() as conn:
            conn.cursor().execute("INSERT INTO music VALUES"
                           "(:music_id, :name, :publisher_id, :genre, :date_of_creation)",
                           {'music_id': music.uid, 'name': music.name, 'publisher_id': music.publisher_id,
                            'genre': music.genera, 'date_of_creation': datetime.now()})
        pass

    def select_musics(self, q) -> List[Music]:
        query = "SELECT * FROM music WHERE "
        for i, key in enumerate(q):
            query += key + "=:" + key
            if i != len(q) - 1:
                query += " AND "
        print(query)
        c = self.get_connection().cursor()
        c.execute(query, q)
        return c.fetchall()

    ###
    def add_request(self, request_string: str) -> None:
        with self.get_connection() as conn:
            conn.cursor().execute(request_string)
        pass

    def select_requests(self) -> List[str]:
        pass


if __name__ == '__main__':
    a = DB()

    print(a.select_all_accounts())
    exit(0)

    x1 = Account(100, 'sasa', '1234', 'mohammad', AccountType.PREMIUM, False, 'yo', 'im mohammad', 'sanmoh99@gmail.com')
    x2 = Account(101, 'smss', '1234', 'sadegh', AccountType.FREE, False, 'yo', 'im 22 yo CE student', 'folan@gmail.com')
    x3 = Account(102, 'hamid', '1234', 'hamid', AccountType.FREE, False, 'yo', 'im just me', 'folan2@gmail.com')
    a.insert_account(x1)
    a.insert_account(x2)
    a.insert_account(x3)

    res = a.select_accounts({'name': 'mohammad'})
    print("SELECT account")
    print(res)

    a.update_account(x1, {'description': 'im a good boi'})

    res = a.select_accounts({'name': 'mohammad'})
    print("update account")
    print(res)

    file1 = File(200, 'mime1', 'desktop/my')
    file2 = File(201, 'mime2', 'desktop/my_heart')
    file3 = File(202, 'mime3', 'desktop/my_heart_will_go_on')

    # a.add_file(file1)
    # a.add_file(file2)
    # a.add_file(file3)

    res = a.select_files({'mime': 'mime1'})
    print("SELECT FILE")
    print(res)

    music1 = Music('Bee gees', 500, 600, file1, 128, 'Rock')
    music2 = Music('Chandelier', 501, 601, file2, 320, 'Pop')
    music3 = Music('Shape of my heart', 502, 602, file3, 128, 'Pop')

    a.insert_music(music1)
    a.insert_music(music2)
    a.insert_music(music3)

    p = PlayList(100, [music1, music3], 'one and three', [x1, x2])

    a.insert_playlist(p)

    res = a.select_musics({'genre': 'Pop'})

    print("select musics")
    print(res)
