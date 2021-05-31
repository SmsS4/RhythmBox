from sharif_music.db_wrapper import DB
from sharif_music.models import *


class Server:
    def __init__(self, db: DB):
        self.__db = db

    def create_account(self, username: str, password: str, phone: str, name: str) -> bool:
        raise NotImplementedError()

    def login(self, username: str, password: str) -> str:
        raise NotImplementedError()

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

    def add_music_to_playlist(self, token: str, playlist_uid: str, music_uid: str) -> bool:
        raise NotImplementedError()

    def remove_music_from_playlist(self, token: str, playlist_uid: str, music_uid:str) -> bool:
        raise NotImplementedError()

    def get_default_playlist(self, token: str) -> PlayList:
        raise NotImplementedError()

    def follow_artis(self, token: str, artist: str) -> bool:
        raise NotImplementedError()
