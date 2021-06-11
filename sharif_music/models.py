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
    phone: str
    account_type: AccountType
    publisher: bool
    photo_url: str

@dataclass
class PlayList:
    uid: str
    musics: List[Music]
    name: str
    owners: List[str]
