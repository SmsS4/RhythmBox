from typing import List

from sharif_music.models import Music, Quality, PlayList
from sharif_music.server import Server


class Api:
    def __init__(self, server: Server):
        self.__server = server

    def login(self, username: str, password: str) -> str:
        return self.__server.login(username, password)

    def register(self, username: str, password: str, phone: str, name: str) -> bool:
        return self.__server.create_account(username, password, phone, name)

    def make_premium(self, token: str) -> bool:
        return self.__server.make_premium(token)

    def add_music(self, token: str) -> bool:
        raise NotImplementedError()
        return self.__server.add_music(token, None)

    def search_music(self, music_name: str, music_genera: str) -> List[Music]:
        return self.__server.search_music(music_name, music_genera)

    def get_music(self, uid: str, quality: Quality):
        music_info = self.__server.get_music(uid, quality)
        raise NotImplementedError()

    def add_playlist(self, token: str, name: str) -> bool:
        return self.__server.add_playlist(token, name)

    def get_playlist(self, uid: str) -> PlayList:
        return self.__server.get_playlist(uid)

    def add_owner_to_playlist(self, uid: str, username: str) -> bool:
        return self.__server.add_owner_to_playlist(uid, username)

    def add_music_to_playlist(
        self, token: str, playlist_uid: str, music_uid: str
    ) ->\
            bool:
        return self.__server\
            .add_music_to_playlist(token, playlist_uid, music_uid)

    def remove_music_from_playlist(
        self, token: str, playlist_uid: str, music_uid
    ) -> bool:
        return self.__server.remove_music_from_playlist(token, playlist_uid, music_uid)

    def get_default_playlist(self, token: str) -> PlayList:
        return self.__server.get_default_playlist(token)

    def follow_artis(self, token: str, artist: str) -> bool:
        return self.__server.follow_artis(token, artist)
