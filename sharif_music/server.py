# pylint: skip-file
import collections
import uuid

from fastapi import UploadFile

from sharif_music import utils
from sharif_music.db_wrapper import DB
from sharif_music.models import *
from typing import List, Optional, Dict, Tuple, Set


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
        self.musics: Dict[int, Music] = {}
        self.followers: Dict[int, List[int]] = collections.defaultdict(list)
        self.__fetch_init_data_from_db()
        self.shared: Dict[int, List[int]] = collections.defaultdict(list)
        self.listened: Dict[str, List[Music]] = collections.defaultdict(list)

    def listen(self, token: str, music_id: int):
        self.listened[token].append(self.get_music(music_id))
        discover_id = self.get_account_by_token(token).id + 1
        self.playlist[discover_id].musics = self.__db.suggest_songs(
            list(self.listened[token]), 10
        )
        self.update_playlist_in_db(self.playlist[discover_id])

    def share(self, playlist_id: int, username: str):
        self.shared[
            self.get_account_by_username(username).id  # pytype:disable=attribute-error
        ].append(playlist_id)

    def shared_with_me(self, token: str) -> List[PlaylistWeb]:
        return [
            PlaylistWeb(id=playlist_id, name=self.playlist[playlist_id].name)
            for playlist_id in self.shared[
                self.get_account_by_token(token).id  # pytype:disable=attribute-error
            ]
            if playlist_id in self.playlist
        ]

    def get_file_path(self, file_id: int) -> File:
        return self.files[file_id]

    def __fetch_init_data_from_db(self):
        """
        Gets data from db
        """
        self.accounts = self.__db.select_accounts()
        self.files = {file.id: file for file in self.__db.select_files()}
        self.musics = {music.uid: music for music in self.__db.select_musics()}
        self.playlist = self.__db.select_playlists()
        # files = [
        #     File(
        #         1,
        #         0,
        #         "audio/mp3",
        #         "/home/smss/Downloads/Telegram Desktop/wires.mp3"
        #     ),
        #     File(
        #         2,
        #         1,
        #         "audio/mp3",
        #         "/home/smss/Downloads/Telegram Desktop/wires.mp3"
        #     ),
        # ]
        # self.files[files[0].id] = files[0]
        # self.files[files[1].id] = files[1]
        # self.musics.update({
        #     1: Music(
        #         "wires",
        #         0,
        #         1,
        #         files[0],
        #         128,
        #         Generes.POP,
        #     ),
        #     2: Music(
        #         "wires",
        #         0,
        #         2,
        #         files[1],
        #         320,
        #         Generes.RAP
        #     )
        # })
        # #########
        # # remove
        # # inja mitoni account daem ezafe koni
        self.accounts.append(
            Account(
                id=1,
                username="test",
                password="test",
                name="name",
                account_type=AccountType.PREMIUM,
                publisher=True,
                photo=None,
                description="description",
                email="smss@chmail.ir",
            )
        )
        # self.accounts.append(
        #     Account(
        #         id=2,
        #         username='nottest2',
        #         password='nottest2',
        #         name='notname',
        #         account_type=AccountType.FREE,
        #         publisher=False,
        #         photo=None,
        #         description='notdescription2',
        #         email='smss2@chmail.ir'
        #     )
        # )
        # self.playlist[0] = PlayList(
        #     1,
        #     [self.musics[1]],
        #     "Sample",
        #     [self.accounts[0].username]
        # )
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
            description="",
            email=email,
        )
        self.accounts.append(account)
        self.__db.insert_account(account)
        publishers_playlist = PlayList(
            uid=account.id, musics=[], name="Followings", owners=[account.username]
        )
        self.add_playlist_to_db(publishers_playlist)
        self.playlist[publishers_playlist.uid] = publishers_playlist

        discover_playlist = PlayList(
            uid=account.id + 1, musics=[], name="Discover", owners=[account.username]
        )
        self.add_playlist_to_db(discover_playlist)
        self.playlist[discover_playlist.uid] = discover_playlist
        return "Register successfully. Welcome to SharifMusic", True

    BASE = "/var/tmp/"

    def get_photo(self, url: str):
        return open(f"{self.BASE}{url}", "r")

    def upload_file(self, uploaded_file: UploadFile, owner_id: int) -> File:
        file_id = utils.gen_id()
        path = f"{self.BASE}{file_id}"
        file = File(
            owner_id=owner_id,
            id=utils.gen_id(),
            mime=uploaded_file.content_type,
            path=path,
        )
        with open(path, "wb") as f:
            f.write(uploaded_file.file.read())
        return file

    def update_account(self, account: Account):
        self.__db.update_account(account)

    def change_photo(self, token: str, uploaded_file: UploadFile) -> int:
        user = self.get_account_by_token(token)
        user.photo = self.upload_file(uploaded_file, user.id)
        self.files[user.photo.id] = user.photo
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
        self.__db.insert_request(f"{account.id}$pub")

    def request_premium(self, token: str):
        account = self.get_account_by_token(token)
        self.__db.insert_request(f"{account.id}$pre")

    def add_music(
        self, token: str, name: str, uploaded_file: UploadFile, genera: str
    ) -> bool:
        user = self.get_account_by_token(token)
        if not user.publisher:  # pytype:disable=attribute-error
            return False
        music = Music(  # pytype:disable=wrong-arg-types
            name=name,
            publisher_id=user.id,  # pytype:disable=attribute-error
            uid=utils.gen_id(),
            file=None,
            quality=128,
            genera=genera,
        )
        file = self.upload_file(uploaded_file, music.uid)
        music.file = file
        self.__db.insert_music(music)
        self.files[file.id] = file
        self.musics[music.uid] = music
        for follower_username in self.followers[
            user.id  # pytype:disable=attribute-error
        ]:
            follower = self.get_account_by_username(
                follower_username
            )  # pytype:disable=attribute-error
            self.playlist[follower.id].musics.append(  # pytype:disable=attribute-error
                music
            )
            self.update_playlist_in_db(
                self.playlist[follower.id]  # pytype:disable=attribute-error
            )
        return True

    def get_music(self, uid: int) -> Music:

        return self.musics[uid]

    def serach(self, token: str, string: str) -> Dict[str, List[WebResult]]:
        if string.startswith("sharedpl$"):
            name = string.split("sharedpl$")[1]
            print(name)
            print(len(name))
            print(self.playlist)
            return {
                "Shared Playlist": [
                    PlaylistWeb(playlist_id, self.playlist[playlist_id].name)
                    for playlist_id in self.playlist
                    if name == self.playlist[playlist_id].name
                ]
            }
        user = self.get_account_by_token(token)
        result = {
            "artists": self.search_artists(string),
            "musics": self.search_musics(
                string, user.account_type == AccountType.PREMIUM
            ),
            "playlists": self.search_playlists(string),
        }
        return result

    def validate_token(self, token: str) -> bool:
        return token in self.token_to_account

    def search_artists(self, string: str) -> List[PublisherWeb]:
        return [
            PublisherWeb(  # pytype:disable=wrong-arg-types
                account.username, account.name
            )
            for account in self.accounts
            if string in account.name and account.publisher
        ]

    def follow(self, token: str, username: str) -> None:
        self.followers[
            self.get_account_by_username(username).id  # pytype:disable=attribute-error
        ].append(
            self.get_account_by_token(token).username  # pytype:disable=attribute-error
        )
        # todo db

    def checkfollow(self, token: str, username: str) -> bool:
        return (
            self.get_account_by_token(token).username  # pytype:disable=attribute-error
            in self.followers[
                self.get_account_by_username(  # pytype:disable=attribute-error
                    username
                ).id
            ]
        )

    def search_musics(self, string: str, high_quality: bool) -> List[MusicWeb]:
        return [
            MusicWeb(music.uid, music.name, music.quality, music.genera)
            for music in self.musics.values()
            if string in music.name and (music.quality == 128 or high_quality)
        ]

    def search_playlists(self, string: str) -> List[PlaylistWeb]:
        return [
            PlaylistWeb(playlist_id, self.playlist[playlist_id].name)
            for playlist_id in self.playlist
            if string in self.playlist[playlist_id].name
            and self.playlist[playlist_id].name not in ("Followings", "Discover")
        ]

    def add_playlist_to_db(self, playlist: PlayList):
        self.__db.insert_playlist(playlist)

    def update_playlist_in_db(self, playlist: PlayList):
        self.__db.delete_playlist(playlist.uid)
        self.__db.insert_playlist(playlist)

    def add_playlist(self, token: str, name: str) -> None:
        """
        create empty playlist

        Args:
            token: login token
            name: name of playlist

        Returns:

        """
        print(name)
        uid = utils.gen_id()
        self.playlist[uid] = PlayList(
            uid,
            [],
            name,
            [
                self.get_account_by_token(  # pytype:disable=attribute-error
                    token
                ).username
            ],
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

    def add_owner_to_playlist(
        self, token: str, uid: int, username: str
    ) -> Optional[str]:
        """
        add manager to playlist
        Args:
            uid: id playlist
            username: username of account

        Returns:

        """
        if (
            not self.get_account_by_token(token)
            or self.get_account_by_token(token).username
            not in self.playlist[uid].owners
        ):
            return "Only managers can add new manager"
        if username in self.playlist[uid].owners:
            return "Username is already manager"
        if self.get_account_by_username(username) is None:
            return "Username not found"
        self.playlist[uid].owners.append(
            self.get_account_by_username(username).username
        )
        self.update_playlist_in_db(self.playlist[uid])
        return None

    def add_music_to_playlist(
        self, token: str, playlist_uid: int, music_uid: int
    ) -> Optional[str]:
        playlist = self.playlist[playlist_uid]
        if (
            not self.get_account_by_token(token)
            or self.get_account_by_token(token).username not in playlist.owners
        ):
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
        if (
            not self.get_account_by_token(token)
            or self.get_account_by_token(token).username not in playlist.owners
        ):
            return "User is not manager of playlist"
        if self.musics[music_uid] in playlist.musics:
            playlist.musics.remove(self.musics[music_uid])
            self.update_playlist_in_db(self.playlist[playlist_uid])
            return None
        return "Music is not in playlist"

    def get_my_playlists(self, username: str) -> List[PlaylistWeb]:
        return [
            PlaylistWeb(playlist_id, self.playlist[playlist_id].name)
            for playlist_id in self.playlist
            if username in self.playlist[playlist_id].owners
        ]

    def remove_playlist(self, token: str, playlist_id: int) -> Optional[str]:
        self.playlist.pop(playlist_id)
        self.__db.delete_playlist(playlist_id)
        return None

    def premium(self, token: str, transaction_id) -> None:
        if self.__db.did_pay(transaction_id):
            print("hey")
            acc = self.get_account_by_token(token)
            acc.account_type = AccountType.PREMIUM
            self.update_account(acc)
            print(acc.account_type)
