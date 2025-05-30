CREATE TABLE Listener (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Song (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    artist VARCHAR(100),
    album VARCHAR(100),
    duration INT NOT NULL,
    url VARCHAR UNIQUE NOT NULL,
    image_url VARCHAR
);

CREATE TABLE Playlist (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    is_user_created BOOLEAN DEFAULT TRUE,
    listener_id INT REFERENCES Listener(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE PlaylistSong (
    playlist_id INT REFERENCES Playlist(id) ON DELETE CASCADE,
    song_id INT REFERENCES Song(id) ON DELETE CASCADE,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (playlist_id, song_id)
);

CREATE TABLE Playback (
    id SERIAL PRIMARY KEY,
    listener_id INT REFERENCES Listener(id) ON DELETE CASCADE,
    song_id INT REFERENCES Song(id),
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_played INT NOT NULL
);

CREATE TABLE Follow (
    listener_id INT REFERENCES Listener(id) ON DELETE CASCADE,
    playlist_id INT REFERENCES Playlist(id) ON DELETE CASCADE,
    followed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (listener_id, playlist_id)
);
