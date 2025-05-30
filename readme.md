# 🎵 Spotitried: A Simple Music Streaming Platform

Welcome to **Spotitried**, a web-based music streaming application created for the Spring 2025 Databases Project. It simulates a copyright-free Spotify-style platform, where users can register, listen to music, create playlists, and follow each other’s content.

## 📚 Project Description

Spotitried is a lightweight music streaming system focused on:
- Managing **users**, **songs**, and **playlists**
- Tracking **song playbacks**
- Supporting **social features** like following playlists
- Providing **analytics** on listening behavior and popularity

---

## 🧩 Domain Overview

This project implements a **Spotify-like schema**, designed with the following goals:
- Create and follow playlists
- Add and organize songs within them
- Track listening habits and play counts
- Support both system-generated and user-generated content

---

## 🗂️ Entities & Attributes

### 👤 Listener
Represents the app's end users.

| Attribute     | Type             | Description                        |
|---------------|------------------|------------------------------------|
| `id`          | SERIAL PRIMARY KEY | Unique listener ID                |
| `username`    | VARCHAR(50) UNIQUE NOT NULL | Chosen display name           |
| `email`       | VARCHAR(100) UNIQUE NOT NULL | Email for login              |
| `password`    | VARCHAR(255) NOT NULL | Securely hashed password       |
| `created_at`  | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Signup timestamp         |

**Indexes:**
- `idx_listener_username` (unique)
- `idx_listener_email` (unique)

---

### 🎵 Song
Metadata for each music track.

| Attribute     | Type             | Description                        |
|---------------|------------------|------------------------------------|
| `id`          | SERIAL PRIMARY KEY | Unique song ID                    |
| `title`       | VARCHAR(100) NOT NULL | Song title                     |
| `artist`      | VARCHAR(100) | Artist name                         |
| `album`       | VARCHAR(100) | Album name                          |
| `duration`    | INT NOT NULL    | Duration in seconds                |
| `url`         | VARCHAR UNIQUE NOT NULL | Link to the audio file        |
| `image_url`   | VARCHAR         | Album or song cover image URL      |

**Indexes:**
- `idx_song_title`
- `idx_song_artist`
- `idx_song_album`

---

### 📃 Playlist
Playlists can be user- or system-generated.

| Attribute         | Type             | Description                        |
|-------------------|------------------|------------------------------------|
| `id`              | SERIAL PRIMARY KEY | Unique playlist ID              |
| `name`            | VARCHAR(100) NOT NULL | Playlist title                 |
| `is_user_created` | BOOLEAN DEFAULT TRUE | Flag for user-generated        |
| `listener_id`     | INT REFERENCES Listener(id) ON DELETE CASCADE | Creator |
| `created_at`      | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Creation date             |

**Indexes:**
- `idx_playlist_listener_id`
- `idx_playlist_name`

---

### 🔁 PlaylistSong (Join Table)
Links songs to playlists.

| Attribute     | Type             | Description                        |
|---------------|------------------|------------------------------------|
| `playlist_id` | INT REFERENCES Playlist(id) ON DELETE CASCADE | Playlist ID |
| `song_id`     | INT REFERENCES Song(id) ON DELETE CASCADE | Song ID |
| `added_at`    | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Timestamp of addition |

**Primary Key:** `(playlist_id, song_id)`

**Indexes:**
- `idx_playlist_song_song_id`
- `idx_playlist_song_playlist_id`

---

### ▶️ Playback
Tracks listening activity.

| Attribute        | Type             | Description                        |
|------------------|------------------|------------------------------------|
| `id`             | SERIAL PRIMARY KEY | Playback event ID                |
| `listener_id`    | INT REFERENCES Listener(id) ON DELETE CASCADE | Who played |
| `song_id`        | INT REFERENCES Song(id) | What was played             |
| `played_at`      | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | When                   |
| `duration_played`| INT NOT NULL    | Time in seconds played             |

**Indexes:**
- `idx_playback_listener_id`
- `idx_playback_song_id`
- `idx_playback_played_at`

---

### 📌 Follow
Tracks which playlists users follow.

| Attribute     | Type             | Description                        |
|---------------|------------------|------------------------------------|
| `listener_id` | INT REFERENCES Listener(id) ON DELETE CASCADE | Follower      |
| `playlist_id` | INT REFERENCES Playlist(id) ON DELETE CASCADE | Followed list |
| `followed_at` | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | When followed  |

**Primary Key:** `(listener_id, playlist_id)`

**Indexes:**
- `idx_follow_listener_id`
- `idx_follow_playlist_id`

---

## 🧪 Example Queries Implemented

1. **Top 5 Most Played Songs in the Last Month**
   ```sql
   SELECT s.title, COUNT(*) AS play_count
   FROM Playback p
   JOIN Song s ON p.song_id = s.id
   WHERE p.played_at >= CURRENT_DATE - INTERVAL '30 days'
   GROUP BY s.title
   ORDER BY play_count DESC
   LIMIT 5;
   ```

2. **Total Listening Time Per Listener**
   ```sql
   SELECT l.username, SUM(p.duration_played) AS total_time
   FROM Listener l
   JOIN Playback p ON l.id = p.listener_id
   GROUP BY l.username;
   ```

3. **Most Followed User-Generated Playlist**
   ```sql
   SELECT p.name, COUNT(*) AS follower_count
   FROM Follow f
   JOIN Playlist p ON f.playlist_id = p.id
   WHERE p.is_user_created = TRUE
   GROUP BY p.name
   ORDER BY follower_count DESC
   LIMIT 1;
   ```

---

## 🔍 Schema Diagram

You can view the full DBML or visual schema using [dbdiagram.io](https://dbdiagram.io/d/Databases-Project-6817e6531ca52373f5699fc0).

---

## 💡 Contributors

- Turganov Imran  
- Alain David Escarra Garcia  
- Jose Carlos Serize Portela

---

## 🚀 Link to Project

🌐 [Live Demo of Spotitried](https://oats-consumers.github.io/Spotitried/)

---

## 📄 License

This project is for educational purposes. All music used is copyright-free.
