from typing import List, Optional
from dataclasses import dataclass
import enum


class AccountType(enum.IntEnum):
    FREE = 1
    PREMIUM = 2


@dataclass
class File:
    id: int
    mime: str  # image/jpg , application/pdf, ...
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
    uid: int
    file: File
    quality: int
    genera: str

class Generes:
    POP = "Pop"
    RAP = "Rap"
    ROCK = "Rock"
    HEAVY_METAL = "HeavyMetal"
    BLUE = "Blue"

@dataclass
class PlayList:
    uid: int
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
