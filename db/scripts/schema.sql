CREATE TABLE "User" (
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
                      duration INT NOT NULL
);

CREATE TABLE Playlist (
                          id SERIAL PRIMARY KEY,
                          name VARCHAR(100) NOT NULL,
                          is_user_created BOOLEAN DEFAULT TRUE,
                          user_id INT,
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                          FOREIGN KEY (user_id) REFERENCES "User"(id)
);

CREATE TABLE PlaylistSong (
                              playlist_id INT,
                              song_id INT,
                              added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                              PRIMARY KEY (playlist_id, song_id),
                              FOREIGN KEY (playlist_id) REFERENCES Playlist(id),
                              FOREIGN KEY (song_id) REFERENCES Song(id)
);

CREATE TABLE Playback (
                          id SERIAL PRIMARY KEY,
                          user_id INT,
                          song_id INT,
                          played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                          duration_played INT NOT NULL,
                          FOREIGN KEY (user_id) REFERENCES "User"(id),
                          FOREIGN KEY (song_id) REFERENCES Song(id)
);

CREATE TABLE Follow (
                        user_id INT,
                        playlist_id INT,
                        followed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (user_id, playlist_id),
                        FOREIGN KEY (user_id) REFERENCES "User"(id),
                        FOREIGN KEY (playlist_id) REFERENCES Playlist(id)
);

-- Indexes
CREATE INDEX idx_song_artist ON Song(artist);
CREATE INDEX idx_song_title ON Song(title);
CREATE INDEX idx_playlist_user_id ON Playlist(user_id);
CREATE INDEX idx_playlistsong_song_id ON PlaylistSong(song_id);
CREATE INDEX idx_playback_user_id ON Playback(user_id);
CREATE INDEX idx_playback_song_id ON Playback(song_id);
CREATE INDEX idx_playback_played_at ON Playback(played_at);
CREATE INDEX idx_follow_playlist_id ON Follow(playlist_id);
