# pylint: skip-file
from typing import List

from dataclasses import dataclass
import enum


class AccountType(enum.IntEnum):
    FREE = 1
    PREMIUM = 2


class Quality(enum.IntEnum):
    Q128 = 128
    Q320 = 320


@dataclass
class Music:
    name: str
    uid: str
    path: str


@dataclass
class Account:
    id: int
    username: str
    password: str
    name: str
    account_type: AccountType
    publisher: bool
    photo_url: str
    description: str
    email: str


@dataclass
class PlayList:
    uid: str
    musics: List[Music]
    name: str
    owners: List[str]


@dataclass
class WebResult:
    id: int
    name: str

class PublisherWeb(WebResult):pass
class MusicWeb(WebResult):pass
class PlaylistWeb(WebResult):pass