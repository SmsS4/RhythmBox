# pylint: skip-file
from typing import List, Optional, Union

from dataclasses import dataclass
import enum


class AccountType(enum.IntEnum):
    FREE = 1
    PREMIUM = 2


@dataclass
class File:
    id: int
    mime: str
    path: str





@dataclass
class Account:
    id: int
    username: str
    password: str
    name: str
    account_type: AccountType
    publisher: bool
    photo: Optional[File]
    description: str
    email: str


@dataclass
class Music:
    name: str
    publisher_id: int
    uid: str
    file: File
    quality: int
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


@dataclass
class PublisherWeb(WebResult): pass


@dataclass
class MusicWeb(WebResult):
    quality: int


@dataclass
class PlaylistWeb(WebResult): pass
