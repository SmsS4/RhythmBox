# pylint: skip-file
import uuid

from sharif_music.db_wrapper import DB
from sharif_music.models import *
from typing import List, Optional, Dict, Tuple


class Server:
    def __init__(self, db: DB):
        self.__db = db
        self.token_to_account: Dict[str, Account] = {}
        self.accounts: List[Account] = []
        self.__fetch_init_data_from_db()

    def __fetch_init_data_from_db(self):
        pass

    def get_account_by_username(self, username: str) -> Optional[Account]:
        for account in self.accounts:
            print(username, account.username)
            if account.username == username:
                return account
        return None

    def get_account_by_token(self, token: str) -> Optional[Account]:
        return self.token_to_account.get(token, None)

    def create_account(
        self, username: str, password: str, phone: str, name: str
    ) -> Tuple[str, bool]:
        if self.get_account_by_username(username):
            return "Username already taken", False
        account = Account(
            username=username,
            password=password,
            name=name,
            account_type=AccountType.FREE,
            publisher=False,
        )
        self.accounts.append(account)
        # self.__db.insert_account(account)
        return "Register successfully. Welcome to SharifMusic", True

    def login(self, username: str, password: str) -> str:
        token = str(int(uuid.uuid1()))
        account = self.get_account_by_username(username)
        if account is None or account.password != password:
            return ""
        self.token_to_account[token] = account
        return token

    def __get_user_by_token(self, token: str) -> Account:
        raise NotImplementedError()

    def make_premium(self, token: str) -> bool:
        raise NotImplementedError()

    def add_music(self, token: str, music: Music) -> bool:
        raise NotImplementedError()

    def search_music(self, music_name: str, music_genera: str) -> List[Music]:
        raise NotImplementedError()

    def get_music(self, uid: str, quality: Quality) -> Music:
        raise NotImplementedError()

    def add_playlist(self, token: str, name: str) -> bool:
        raise NotImplementedError()

    def get_playlist(self, uid: str) -> PlayList:
        raise NotImplementedError()

    def add_owner_to_playlist(self, uid: str, username: str) -> bool:
        raise NotImplementedError()

    def add_music_to_playlist(
        self, token: str, playlist_uid: str, music_uid: str
    ) -> bool:
        raise NotImplementedError()

    def remove_music_from_playlist(
        self, token: str, playlist_uid: str, music_uid: str
    ) -> bool:
        raise NotImplementedError()

    def get_default_playlist(self, token: str) -> PlayList:
        raise NotImplementedError()

    def follow_artis(self, token: str, artist: str) -> bool:
        raise NotImplementedError()

    def search_artists(self, string:str) -> List[PublisherWeb]:
        return [
            PublisherWeb(41234, 'AghaSadegh')
        ]
    def search_musics(self, string:str) -> List[MusicWeb]:
        return [
            MusicWeb(5, 'wires'),
            MusicWeb(2, 'not wires'),
        ]

    def search_playlists(self, string: str) -> List[PlaylistWeb]:
        return [
            PlaylistWeb(1, 'musics 2'),
            PlaylistWeb(1, 'musics 5'),
            PlaylistWeb(1, 'musics 1'),
        ]