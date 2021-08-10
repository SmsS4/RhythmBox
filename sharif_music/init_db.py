import sqlite3

conn = sqlite3.connect(':memory:')

c = conn.cursor()


c.execute("""CREATE TABLE registered_users (
        ID INT PRIMARY KEY,
        username varchar(20) NOT NULL,
        password varchar(20) NOT NULL,
        description varchar(300) NOT NULL,
        email varchar(20) NOT NULL,
        is_account_premium varchar(20) NOT NULL,
        user_photo varchar(512) NOT NULL
        )""")
conn.commit()


c.execute("""CREATE TABLE payment (
	date_of_payment date,
	payer_id INT PRIMARY KEY, 
	payment_group varchar(20) NOT NULL,
	description varchar(300) NOT NULL,
	FOREIGN KEY (payer_id) REFERENCES registered_users(ID)
        )""")
conn.commit()


c.execute("""CREATE TABLE person_has_playlist (
	user_id INT, 
	playlist_id INT,
	subscription_data date NOT NULL,
	PRIMARY KEY (user_id, playlist_id),
	FOREIGN KEY (user_id) REFERENCES registered_users(ID),
	FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id)
	
)""")
conn.commit()

# c.execute("""""")
# conn.commit()


c.execute("""CREATE TABLE playlist (
	playlist_id INT,
	creator_id INT NOT NULL,
	creation_date date NOT NULL,
	PRIMARY KEY(playlist_id),
	FOREIGN KEY (creator_id) REFERENCES registered_users(ID)
	
)""")
conn.commit()


c.execute("""CREATE TABLE music_in_playlist (
	music_id INT NOT NULL, 
	playlist_id INT NOT NULL,
	date_added date NOT NULL,
	PRIMARY KEY (music_id, playlist_id),
	FOREIGN KEY (music_id) REFERENCES music(music_id),
	FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id)
	
)""")
conn.commit()


c.execute("""CREATE TABLE music (
	music_id INT PRIMARY KEY,
	name varchar(20) NOT NULL,
	publisher_id INT NOT NULL,
	genre varchar(20) NOT NULL,
	description varchar(300) NOT NULL, 
	date_of_creation date NOT NULL
)""")
conn.commit()


c.execute("""CREATE TABLE playable_music (
	music_id INT NOT NULL,
	quality varchar(5) NOT NULL,
	file_address varchar(512) NOT NULL,
	FOREIGN KEY (music_id) REFERENCES music(music_id)
)""")
conn.commit()


c.execute("""CREATE TABLE publisher (
	user_id INT PRIMARY KEY, 
	username varchar(20) NOT NULL,
	password varchar(20) NOT NULL
)""")
conn.commit()


c.execute("""CREATE TABLE user_follow_publisher (
	user_id INT NOT NULL,
	publisher_id INT NOT NULL,
	date_of_following date NOT NULL,
	PRIMARY KEY (user_id, publisher_id),
	FOREIGN KEY (publisher_id) REFERENCES publisher(user_id),
	FOREIGN KEY (user_id) REFERENCES registered_users(ID)
)""")
conn.commit()
