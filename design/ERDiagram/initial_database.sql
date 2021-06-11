SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE registered_users (
	ID INT NOT NULL,
  	username varchar(20) NOT NULL,
  	password varchar(20) NOT NULL,
  	description varchar(300) NOT NULL,
  	email varchar(20) NOT NULL,
  	is_account_premium varchar(20) NOT NULL,
  	user_photo varchar(512) NOT NULL
);

ALTER TABLE registered_users
  ADD PRIMARY KEY (ID);

CREATE TABLE payment (
	date_of_payment date NOT NULL,
	payer_id INT NOT NULL, 
	payment_group varchar(20) NOT NULL,
	description varchar(300) NOT NULL
);

ALTER TABLE payment
  ADD PRIMARY KEY (date_of_payment, payer_id);




CREATE TABLE person_has_playlist (
	user_id INT NOT NULL, 
	playlist_id INT NOT NULL,
	subscription_data date NOT NULL
);

ALTER TABLE person_has_playlist
  ADD PRIMARY KEY (user_id, playlist_id);

CREATE TABLE playlist (
	playlist_id INT NOT NULL,
	creator_id INT NOT NULL,
	creation_date date NOT NULL
);

ALTER TABLE playlist
  ADD PRIMARY KEY (playlist_id);

CREATE TABLE music_in_playlist (
	music_id INT NOT NULL, 
	playlist_id INT NOT NULL,
	date_added date NOT NULL
);

ALTER TABLE music_in_playlist
  ADD PRIMARY KEY (music_id, playlist_id);

CREATE TABLE music (
	music_id INT NOT NULL,
	name varchar(20) NOT NULL,
	publisher_id INT NOT NULL,
	genre varchar(20) NOT NULL,
	description varchar(300) NOT NULL, 
	date_of_creation date NOT NULL
);

ALTER TABLE music
  ADD PRIMARY KEY (music_id);

CREATE TABLE playable_music (
	music_id INT NOT NULL,
	quality varchar(5) NOT NULL,
	file_address varchar(512) NOT NULL
);

ALTER TABLE playable_music
  ADD PRIMARY KEY (music_id);


CREATE TABLE publisher (
	user_id INT NOT NULL, 
	username varchar(20) NOT NULL,
	password varchar(20) NOT NULL
);

ALTER TABLE publisher
  ADD PRIMARY KEY (user_id);

CREATE TABLE user_follow_publisher (
	user_id INT NOT NULL,
	publisher_id INT NOT NULL,
	date_of_following date NOT NULL
);

ALTER TABLE user_follow_publisher
  ADD PRIMARY KEY (user_id, publisher_id);


ALTER TABLE user_follow_publisher
 	ADD FOREIGN KEY (publisher_id) REFERENCES publisher(user_id),
 	ADD FOREIGN KEY (user_id) REFERENCES registered_users(ID);

ALTER TABLE playable_music
 	ADD FOREIGN KEY (music_id) REFERENCES music(music_id);

ALTER TABLE music_in_playlist
	ADD FOREIGN KEY (music_id) REFERENCES music(music_id),
	ADD FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id);

ALTER TABLE playlist 
	ADD FOREIGN KEY (creator_id) REFERENCES registered_users(ID);

ALTER TABLE person_has_playlist
	ADD FOREIGN KEY (user_id) REFERENCES registered_users(ID),
	ADD FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id);

ALTER TABLE payment
	ADD FOREIGN KEY (payer_id) REFERENCES registered_users(ID);