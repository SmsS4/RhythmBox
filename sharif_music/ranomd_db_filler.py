import os
import random
from typing import List

from sharif_music import utils
from sharif_music.db_wrapper import DB
from sharif_music.models import Music, File, Account, AccountType

with open("words", "r") as words_file:
    words = words_file.readlines()
current = 0


def get_random_word():
    global current
    current += 1
    return words[current]


def create_random_publishers():
    for i in range(10):
        account = Account(
            id=i,
            username=get_random_word(),
            password=get_random_word(),
            name=get_random_word(),
            account_type=AccountType.PREMIUM,
            publisher=True,
            photo=None,
            description=get_random_word() + get_random_word() + get_random_word(),
            email=f"{get_random_word()}@{get_random_word()}.com",
        )
        db.insert_account(account)


def get_publishers() -> List[Account]:
    return [account for account in db.select_accounts() if account.publisher]


def get_random_publisher() -> Account:
    return get_publishers()[random.randint(0, len(get_publishers()) - 1)]


genres = ["Pop", "Rap", "Rock", "Blue", "Danbooli", "Indie", "Classic", "Pulp", "Jazz"]


def get_random_genre() -> str:
    return genres[random.randint(0, len(genres) - 1)]


def add_musics():
    path_to_musics_folder = "/home/smss/Downloads/all_mus/"
    for root, dirs, files in os.walk(path_to_musics_folder):
        for filename in files:
            if filename.endswith(".mp3"):
                full_path = os.path.join(root, filename)
                print(filename, full_path)
                music_name = filename.split(".mp3")[0]
                pub = get_random_publisher()
                music_id = utils.gen_id()
                file = File(
                    owner_id=music_id,
                    id=utils.gen_id(),
                    mime="audio/mp3",
                    path=full_path,
                )
                music = Music(
                    name=music_name,
                    publisher_id=pub.id,
                    uid=music_id,
                    file=file,
                    quality=128 if random.random() >= 0.5 else 320,
                    genera=get_random_genre(),
                )
                db.insert_music(music)
            else:
                continue


db = DB()
print("init db")
create_random_publishers()
print("publisheds added")
add_musics()
print("done")
