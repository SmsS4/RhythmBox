from sharif_music.logger import get_logger
from sharif_music.models import *
import pyodbc


class DB:
    def __init__(self):
        conn = pyodbc.connect(
            "Driver={SQL Server};"
            "Server=sharif_music;"
            "Database=database_name;"
            "Trusted_Connection=yes;"
        )
        self.logger = get_logger('DB Wrapper')
        self.cursor = conn.cursor()

    def do_query(self, query: str):
        self.logger.info("Do query %s", query)
        self.cursor.execute(query)

    def insert(self, table_name: str, col_names: list, values: list):
        self.logger.debug("Insert into db table: %s, col_names: %s, values: %s", table_name, col_names, values)
        query = "INSERT INTO " + table_name + "( "
        for i, col in enumerate(col_names):
            query += col
            if i != len(col_names) - 1:
                query += ", "
        query += ")\n"
        query += "VALUES ("
        for i, val in enumerate(values):
            if type(val) == str:
                query += f"'{val}'"
            else:
                query += f"{str(val)}"
            if i != len(values) - 1:
                query += ", "
        query += ");"

        self.do_query(query)

    def insert_account(self, account: Account) -> None:
        """
        Notes:
            account.file is always None in ``insert_account`` method
        """
        self.logger.debug("Insert account")
        if (
                account.publisher == False
        ):  # account is a user so we add to registered users table
            tpy = "err"
            if account.account_type == AccountType.PREMIUM:
                tpy = "premium"
            else:
                tpy = "free"
            col_names = [
                "ID",
                "username",
                "password",
                "description",
                "email",
                "is_account_premium",
                "user_photo",
            ]
            values = [
                account.id,
                account.username,
                account.password,
                account.description,
                account.email,
                tpy,
                account.photo_url,
            ]
            self.insert("registered_users", col_names, values)
        else:
            col_names = ["user_id", "username", "password"]
            values = [account.id, account.username, account.password]
            self.insert("publisher", col_names, values)

    def select_accounts(self) -> List[Account]:
        pass

    def update_account(self, account: Account):
        pass

    #####
    def add_file(self, file: File):
        pass

    def select_files(self) -> List[File]:
        pass

    ####
    def insert_playlist(self, playlist: PlayList) -> None:
        pass

    def delete_playlist(self, playlist_id: int) -> None:
        pass

    def insert_new_music_to_playlist(self, playlist_id: int, new_music_id: int):
        pass

    def delete_music_from_playlist(self, playlist_id: int, music_to_remove_id: int):
        pass

    def insert_new_owner_to_playlist(self, playlist_id: int, new_owner: str):
        pass

    def select_playlists(self) -> List[PlayList]:
        pass

    #####
    def insert_music(self, music: Music) -> None:
        self.add_file(music.file)
        pass

    def select_musics(self) -> List[Music]:
        pass

    ###
    def add_request(self, request_string: str) -> None:
        pass

    def select_requests(self) -> List[str]:
        pass