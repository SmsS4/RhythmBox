# pylint: skip-file
import uuid

from fastapi import UploadFile

from sharif_music import utils
from sharif_music.db_wrapper import DB
from sharif_music.models import *
from typing import List, Optional, Dict, Tuple


class Server:
    def __init__(self, db: DB):
        """
        Attributes:
            __db: DB Wrapper
            files: dict from File.id to file
            token_to_account: dict from ``login token`` to Account
            accounts: list of account
        """
        self.__db = db
        self.files: Dict[int, File] = {}
        self.token_to_account: Dict[str, Account] = {}
        self.accounts: List[Account] = []
        self.playlist: Dict[int, PlayList] = {}
        self.__fetch_init_data_from_db()

    def get_file_path(self, file_id: int) -> File:
        return self.files[file_id]

    def __fetch_init_data_from_db(self):
        """
        Gets data from db
        """
        # todo
        __file = File(
            0,
            "audio/mp3",
            "/home/smss/Downloads/Telegram Desktop/wires.mp3"
        )
        self.add_file(__file)
        self.musics: Dict[int, Music] = {
            1: Music(
                "wires",
                0,
                1,
                __file,
                128
            ),
            2: Music(
                "wires",
                0,
                2,
                __file,
                320
            )
        }
        #########
        # remove
        # inja mitoni account daem ezafe koni
        self.accounts.append(
            Account(
                id=1,
                username='test',
                password='test',
                name='name',
                account_type=AccountType.PREMIUM,
                publisher=True,
                photo=None,
                description='description',
                email='smss@chmail.ir'
            )
        )
        self.accounts.append(
            Account(
                id=2,
                username='nottest2',
                password='nottest2',
                name='notname',
                account_type=AccountType.FREE,
                publisher=False,
                photo=None,
                description='notdescription2',
                email='smss2@chmail.ir'
            )
        )
        self.playlist[0] = PlayList(
            1,
            [self.musics[1]],
            "Sample",
            [self.accounts[0].username]
        )
        #########

    def get_account_by_username(self, username: str) -> Optional[Account]:
        for account in self.accounts:
            if account.username == username:
                return account
        return None

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        for account in self.accounts:
            if account.id == account_id:
                return account
        return None

    def get_account_by_token(self, token: str) -> Optional[Account]:
        return self.token_to_account.get(token, None)

    def create_account(
            self, username: str, password: str, email: str, name: str
    ) -> Tuple[str, bool]:
        if self.get_account_by_username(username):
            return "Username already taken", False
        account = Account(
            id=utils.gen_id(),
            username=username,
            password=password,
            name=name,
            account_type=AccountType.FREE,
            publisher=False,
            photo=None,
            description='',
            email=email,
        )
        self.accounts.append(account)
        # self.__db.insert_account(account) todo
        return "Register successfully. Welcome to SharifMusic", True

    BASE = "/var/tmp/"

    def get_photo(self, url: str):
        return open(f"{self.BASE}{url}", "r")

    def add_file(self, file: File) -> None:
        self.files[file.id] = file
        # Todo add file to db

    def upload_file(self, uploaded_file: UploadFile) -> File:
        file_id = utils.gen_id()
        path = f"{self.BASE}{file_id}"
        file = File(
            id=utils.gen_id(),
            mime=uploaded_file.content_type,
            path=path,
        )
        with open(path, "wb") as f:
            f.write(uploaded_file.file.read())
        self.add_file(file)
        return file

    def update_account(self, account: Account):
        # todo update db
        pass

    def change_photo(self, token: str, uploaded_file: UploadFile) -> int:
        user = self.get_account_by_token(token)
        user.photo = self.upload_file(uploaded_file)
        self.update_account(user)
        return 1

    def login(self, username: str, password: str) -> Tuple[str, Optional[Account]]:
        token = str(int(uuid.uuid1()))
        account = self.get_account_by_username(username)
        if account is None or account.password != password:
            return "", None
        self.token_to_account[token] = account
        return token, account

    def edit(self, token: str, name: str, description: str):
        account = self.get_account_by_token(token)
        account.name = name
        account.description = description
        self.update_account(account)

    def request_publisher(self, token: str):
        account = self.get_account_by_token(token)
        with open("requests", "a") as f:
            f.write(str(account.id) + "$" + "pub\n")

    def request_premium(self, token: str):
        account = self.get_account_by_token(token)
        with open("requests", "a") as f:
            f.write(str(account.id) + "$" + "pre\n")

    def make_premium(self, token: str) -> bool:
        raise NotImplementedError()

    def add_music(self, token: str, name: str, uploaded_file: UploadFile) -> bool:
        user = self.get_account_by_token(token)
        if not user.publisher:
            return False
        file = self.upload_file(uploaded_file)
        print(name)
        # todo add music to db
        print(file)
        return True

    def search_music(self, music_name: str, music_genera: str) -> List[Music]:
        raise NotImplementedError()

    def get_music(self, uid: int) -> Music:
        return self.musics[uid]

    def follow_artis(self, token: str, artist: str) -> bool:
        raise NotImplementedError()

    def serach(self, token: str, string: str) -> Dict[str, List[WebResult]]:
        user = self.get_account_by_token(token)
        result = {
            'artists': self.search_artists(string),
            'musics': self.search_musics(string, user.account_type == AccountType.PREMIUM),
            'playlists': self.search_playlists(string)
        }
        return result

    def validate_token(self, token: str) -> bool:
        return token in self.token_to_account

    def search_artists(self, string: str) -> List[PublisherWeb]:
        return [PublisherWeb(account.id, account.name) for account in self.accounts if string in account.name]

    def search_musics(self, string: str, high_quality: bool) -> List[MusicWeb]:
        return [MusicWeb(music.uid, music.name, music.quality) for music in self.musics.values() if
                string in music.name and (music.quality == 128 or high_quality)]

    def search_playlists(self, string: str) -> List[PlaylistWeb]:
        return [
            PlaylistWeb(playlist_id, self.playlist[playlist_id].name) for playlist_id in self.playlist if
            string in self.playlist[playlist_id].name
        ]

    def add_playlist_to_db(self, playlist: PlayList):
        # todo
        pass

    def update_playlist_in_db(self, playlist: PlayList):
        # todo
        pass

    def add_playlist(self, token: str, name: str) -> None:
        """
        create empty playlist

        Args:
            token: login token
            name: name of playlist

        Returns:

        """
        uid = utils.gen_id()
        self.playlist[uid] = PlayList(
            uid,
            [],
            name,
            [self.get_account_by_token(token).username]
        )
        self.add_playlist_to_db(self.playlist[uid])

    def get_playlist(self, uid: int) -> PlayList:
        """
        get playlist by ui
        Args:
            uid: uid of playlist

        Returns:

        """
        return self.playlist[uid]

    def add_owner_to_playlist(self, token: str, uid: int, username: str) -> Optional[str]:
        """
        add manager to playlist
        Args:
            uid: id playlist
            username: username of account

        Returns:

        """
        if self.get_account_by_token(token).username != self.playlist[uid].owners[0]:
            return "Only creator of playlist can add new manager"
        if username in self.playlist[uid].owners:
            return "Username is already manager"
        if self.get_account_by_username(username) is None:
            return "Username not found"
        self.playlist[uid].owners.append(self.get_account_by_username(username).username)
        self.update_playlist_in_db(self.playlist[uid])
        return None

    def add_music_to_playlist(
            self, token: str, playlist_uid: int, music_uid: int
    ) -> Optional[str]:
        playlist = self.playlist[playlist_uid]
        if self.get_account_by_token(token).username not in playlist.owners:
            return "User is not manager of playlist"
        if self.musics[music_uid] not in playlist.musics:
            playlist.musics.append(self.musics[music_uid])
            self.update_playlist_in_db(self.playlist[playlist_uid])
            return None
        return "Music is already in playlist"

    def remove_music_from_playlist(
            self, token: str, playlist_uid: int, music_uid: int
    ) -> Optional[str]:
        playlist = self.playlist[playlist_uid]
        if self.get_account_by_token(token).username not in playlist.owners:
            return "User is not manager of playlist"
        if self.musics[music_uid] in playlist.musics:
            playlist.musics.remove(self.musics[music_uid])
            self.update_playlist_in_db(self.playlist[playlist_uid])
            return None
        return "Music is not in playlist"

    def get_my_playlists(self, username: str) -> List[PlaylistWeb]:
        return [
            PlaylistWeb(playlist_id, self.playlist[playlist_id].name) for playlist_id in self.playlist if
            username in self.playlist[playlist_id].owners
        ]
