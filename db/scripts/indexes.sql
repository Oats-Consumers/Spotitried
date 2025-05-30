-- ================================
-- Listener Table Indexes
-- ================================
CREATE UNIQUE INDEX idx_listener_username ON Listener(username);
CREATE UNIQUE INDEX idx_listener_email ON Listener(email);

-- ================================
-- Song Table Indexes
-- ================================
CREATE INDEX idx_song_title ON Song(title);
CREATE INDEX idx_song_artist ON Song(artist);
CREATE INDEX idx_song_album ON Song(album);

-- ================================
-- Playlist Table Indexes
-- ================================
CREATE INDEX idx_playlist_listener_id ON Playlist(listener_id);
CREATE INDEX idx_playlist_name ON Playlist(name);

-- ================================
-- PlaylistSong Table Indexes
-- ================================
CREATE INDEX idx_playlist_song_song_id ON PlaylistSong(song_id);
CREATE INDEX idx_playlist_song_playlist_id ON PlaylistSong(playlist_id);

-- ================================
-- Playback Table Indexes
-- ================================
CREATE INDEX idx_playback_listener_id ON Playback(listener_id);
CREATE INDEX idx_playback_song_id ON Playback(song_id);
CREATE INDEX idx_playback_played_at ON Playback(played_at);

-- ================================
-- Follow Table Indexes
-- ================================
CREATE INDEX idx_follow_listener_id ON Follow(listener_id);
CREATE INDEX idx_follow_playlist_id ON Follow(playlist_id);
