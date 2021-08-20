import sqlite3
import threading
from typing import Dict, Any

from sharif_music.models import *


def bool_to_str(condition) -> str:
    if condition:
        return 'yes'
    else:
        return 'no'


import random


class DB:
    PATH = f"/tmp/shm{20+0*random.randint(0, 10000000)}.db"  #

    def get_connection(self) -> sqlite3.Connection:
        thread_id = threading.get_ident()
        if thread_id not in self.connections:
            self.connections[thread_id] = sqlite3.connect(DB.PATH)
        return self.connections[thread_id]

    def __init__(self):
        self.connections: Dict[int, sqlite3.Connection] = {}
        self.create_tables()

    ALL_USERS = 'all_users'
    PAYMENT = 'payment'
    PLAYLIST_ADMINS = 'playlist_admins'
    PLAYLIST = 'playlist'
    MUSIC_IN_PLAYLIST = 'music_in_playlist'
    USER_FOLLOW_PUBLISHER = 'user_follow_publisher'
    FILES = 'files'
    PLAYABLE_MUSIC = 'playable_music'
    MUSIC = 'music'
    REQUESTS = 'requests'

    def create_tables(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS all_users (
                        ID INT PRIMARY KEY,
                        name varchar(20) NOT NULL,
                        username varchar(20) NOT NULL,
                        password varchar(20) NOT NULL,
                        description varchar(300) NOT NULL,
                        email varchar(20) NOT NULL,
                        is_account_premium varchar(20) NOT NULL,
                        is_publisher varchar(3)
                        )""")
        connection.commit()
        # is publisher: yes/no

        cursor.execute("""CREATE TABLE IF NOT EXISTS payment (
                    date_of_payment date,
                    payer_id INT PRIMARY KEY, 
                    payment_group varchar(20) NOT NULL,
                    description varchar(300) NOT NULL,
                    FOREIGN KEY (payer_id) REFERENCES all_users(ID)
                        )""")
        connection.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS playlist_admins (
                    username INT, 
                    playlist_id INT,
                    PRIMARY KEY (username, playlist_id),
                    FOREIGN KEY (username) REFERENCES all_users(ID),
                    FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id)
                )""")
        connection.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS playlist (
                    playlist_id INT,
                    name varchar(300) NOT NULL,
                    PRIMARY KEY(playlist_id)
                )""")
        connection.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS music_in_playlist (
                    music_id INT NOT NULL, 
                    playlist_id INT NOT NULL,
                    PRIMARY KEY (music_id, playlist_id),
                    FOREIGN KEY (music_id) REFERENCES music(music_id),
                    FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id)
                )""")
        connection.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS music (
                    music_id INT PRIMARY KEY,
                    name varchar(20) NOT NULL,
                    publisher_id INT NOT NULL,
                    genre varchar(20) NOT NULL,
                    quality INT NOT NULL,
                    FOREIGN KEY (publisher_id) REFERENCES all_users(ID)
                )""")
        connection.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS user_follow_publisher (
                    username INT NOT NULL,
                    publisher_id INT NOT NULL,
                    date_of_following date NOT NULL,
                    PRIMARY KEY (username, publisher_id),
                    FOREIGN KEY (publisher_id) REFERENCES all_users(ID)
                )""")
        connection.commit()

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS files (
                    id INT NOT NULL,
                    owner_id INT NOT NULL,
                    mime varchar(300) NOT NULL,
                    path varchar(300) NOT NULL,
                    PRIMARY KEY (id)
                )""")
        connection.commit()

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS requests (
                    request varchar(300) NOT NULL
                )""")
        connection.commit()

    def insert_file(self, file: File) -> None:
        connection = self.get_connection()
        connection.cursor().execute(
            f"INSERT INTO {self.FILES} VALUES "
            "(:id, :owner_id, :mime, :path)",
            {
                'id': file.id,
                'owner_id': file.owner_id,
                'mime': file.mime,
                'path': file.path
            }
        )
        connection.commit()

    def insert_account(self, account: Account) -> None:
        connection = self.get_connection()
        connection.commit()
        if account.photo:
            self.insert_file(account.photo)
        connection.cursor().execute(
            f"INSERT INTO {self.ALL_USERS} VALUES "
            "(:ID, :name, :username, :password, :description, :email, :is_account_premium, :is_publisher)",
            {
                'ID': account.id,
                'name': account.name,
                'username': account.username,
                'password': account.password,
                'description': account.description,
                'email': account.email,
                'is_account_premium': bool_to_str(account.account_type == AccountType.PREMIUM),
                'is_publisher': account.publisher
            }
        )
        connection.commit()

    def select_all(self, table_name: str) -> List[Any]:
        return self.get_connection().cursor().execute(f"SELECT * FROM {table_name}").fetchall()

    def select_files(self) -> List[File]:
        return [
            File(
                id=file[0],
                owner_id=file[1],
                mime=file[2],
                path=file[3]
            ) for file in self.select_all(self.FILES)
        ]

    def select_files_dict(self) -> Dict[int, FILES]:
        return {
            file.owner_id: file for file in self.select_files()
        }

    def select_accounts(self) -> List[Account]:
        files = self.select_files_dict()
        return [
            Account(
                id=account[0],
                name=account[1],
                username=account[2],
                password=account[3],
                description=account[4],
                email=account[5],
                account_type=AccountType.PREMIUM if account[6] == 'yes' else AccountType.FREE,
                publisher=account[7],
                photo=files.get(account[0], None),
            ) for account in self.select_all(self.ALL_USERS)
        ]

    def delete_account(self, account: Account):
        connection = self.get_connection()
        connection.cursor().execute(f"DELETE FROM {self.ALL_USERS} WHERE ID={account.id}")
        if account.photo:
            connection.cursor().execute(f"DELETE FROM {self.FILES} WHERE id={account.photo.id}")
        connection.commit()

    def update_account(self, account: Account):
        self.delete_account(account)
        self.insert_account(account)

    def insert_music(self, music: Music) -> None:
        self.insert_file(music.file)
        connection = self.get_connection()
        connection.cursor().execute(
            f"INSERT INTO {self.MUSIC} VALUES(:music_id, :name, :publisher_id, :genre, :quality)",
            {
                'music_id': music.uid,
                'name': music.name,
                'publisher_id': music.publisher_id,
                'genre': music.genera,
                'quality': music.quality
            }
        )
        connection.commit()

    def select_musics(self) -> List[Music]:
        files = self.select_files_dict()
        return [
            Music(
                uid=music[0],
                name=music[1],
                publisher_id=music[2],
                genera=music[3],
                file=files[music[0]],
                quality=music[4],
            )
            for music in self.get_connection().cursor().execute(f"SELECT * FROM {self.MUSIC}").fetchall()
        ]

    ###
    def insert_request(self, string: str) -> None:
        connection = self.get_connection()
        connection.cursor().execute(f'INSERT INTO {self.REQUESTS} VALUES("{string}")')
        connection.commit()

    def select_requests(self) -> List[str]:
        return [req[0] for req in self.get_connection().cursor().execute(f"SELECT * FROM {self.REQUESTS}").fetchall()]

    def insert_playlist(self, playlist: PlayList) -> None:
        # affects person_has_playlist
        # music_in_playlist
        # playlist
        connection = self.get_connection()
        for owner in playlist.owners:
            connection.cursor().execute(
                f"INSERT INTO {self.PLAYLIST_ADMINS} VALUES(:username, :playlist_id)",
                {'username': owner, 'playlist_id': playlist.uid}
            )
        for music in playlist.musics:
            connection.cursor().execute(
                f"INSERT INTO {self.MUSIC_IN_PLAYLIST} VALUES(:music_id, :playlist_id)",
                {'music_id': music.uid, 'playlist_id': playlist.uid}
            )
        connection.cursor().execute(
            f"INSERT INTO {self.PLAYLIST} VALUES(:playlist_id, :creator_id)",
            {
                'playlist_id': playlist.uid,
                'creator_id': playlist.owners[0],
            }
        )
        connection.commit()

    def delete_playlist(self, playlist_id: int) -> None:
        connection = self.get_connection()
        connection.cursor().execute(f"DELETE from playlist WHERE playlist_id={playlist_id}")
        connection.cursor().execute(f"DELETE from {self.PLAYLIST_ADMINS} WHERE playlist_id={playlist_id}")
        connection.cursor().execute(f"DELETE from {self.MUSIC_IN_PLAYLIST} WHERE playlist_id={playlist_id}")
        connection.commit()

    def insert_new_music_to_playlist(self, playlist_id: int, new_music_id: int):
        connection = self.get_connection()
        connection.cursor().execute("INSERT INTO music_in_playlist VALUES"
                                    "(:music_id, :playlist_id)",
                                    {'music_id': new_music_id, 'playlist_id': playlist_id})
        connection.commit()

    def delete_music_from_playlist(self, playlist_id: int, music_to_remove_id: int):
        connection = self.get_connection()
        connection.cursor().execute("DELETE from music_in_playlist WHERE "
                                    f"playlist_id={playlist_id} AND music_id={music_to_remove_id}")
        connection.commit()

    def insert_new_owner_to_playlist(self, playlist_id: int, owner_id: int):
        connection = self.get_connection()
        connection.cursor().execute(f"INSERT INTO {self.PLAYLIST_ADMINS} VALUES"
                                    "(:username, :playlist_id)",
                                    {'username': owner_id, 'playlist_id': playlist_id})

        connection.commit()

    def select_playlists(self) -> Dict[int, PlayList]:
        playlists = self.select_all(self.PLAYLIST)
        musics_in_playlist = self.select_all(self.MUSIC_IN_PLAYLIST)
        musics_dict: Dict[int, Music] = {
            music.uid: music for music in self.select_musics()
        }
        admins = self.select_all(self.PLAYLIST_ADMINS)
        playlists_dict: Dict[int, PlayList] = {
            playlist[0]: PlayList(uid=playlist[0], name=playlist[1], musics=[], owners=[]) for playlist in playlists
        }
        for music in musics_in_playlist:

            playlists_dict[music[1]].musics.append(
                musics_dict[music[0]]
            )
        for admin in admins:
            playlists_dict[admin[1]].owners.append(admin[0])

        return playlists_dict
if __name__ == '__main__':
    a = DB()
    a.insert_request("test fd safsa fdas ")
    a.insert_request("second req")
    print(a.select_requests())

    x1 = Account(100, 'sasa', '1234', 'mohammad', AccountType.PREMIUM, False,
                 File(100, 100, 'image/png', '/home/smss/Pictures/Screenshot from 2021-03-30 11-30-40.png'),
                 'im mohammad', 'sanmoh99@gmail.com')
    x2 = Account(2200, 'notsasa', '1234', 'mohammad', AccountType.PREMIUM, False,
                 File(100, 100, 'image/png', '/home/smss/Pictures/Screenshot from 2021-03-30 11-30-40.png'),
                 'im mohammad', 'sanmoh99@gmail.com')
    a.insert_account(x1)
    print(a.select_accounts())
    x1.name = "new name"
    a.update_account(x1)
    print(a.select_accounts())
    a.delete_account(x1)
    print(a.select_accounts())

    file1 = File(0, 200, 'mime1', 'desktop/my')
    file2 = File(1, 201, 'mime2', 'desktop/my_heart')
    file3 = File(2, 202, 'mime3', 'desktop/my_heart_will_go_on')

    # a.insert_file(file1)
    # a.insert_file(file2)
    # a.insert_file(file3)

    # res = a.select_files()
    # print("SELECT FILE")
    # print(res)

    music1 = Music('Bee gees', 500, 0, file1, 128, 'Rock')
    music2 = Music('Chandelier', 501, 1, file2, 320, 'Pop')
    music3 = Music('Shape of my heart', 2555, 2, file3, 128, 'Pop')

    a.insert_music(music1)
    a.insert_music(music2)
    a.insert_music(music3)
    print(a.select_musics())
    print('----------------------------')
    p = PlayList(100, [music1, music3], 'one and three', [x1.username, x2.username])
    a.insert_playlist(p)
    print(a.select_playlists())
    a.insert_new_owner_to_playlist(p.uid, "test")
    print(a.select_playlists())
    a.insert_new_music_to_playlist(p.uid, music2.uid)
    print(a.select_playlists())
    a.delete_music_from_playlist(p.uid, music3.uid)

    print(a.select_playlists())
    a.delete_playlist(p.uid)
    print(a.select_playlists())

    exit(0)



    a.insert_playlist(p)

    res = a.select_musics({'genre': 'Pop'})

    print("select musics")
    print(res)
