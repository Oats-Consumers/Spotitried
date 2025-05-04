from faker import Faker
import random
from datetime import datetime

fake = Faker()
Faker.seed(42)

NUM_USERS = 50
NUM_SONGS = 100
NUM_PLAYLISTS = 15
NUM_PLAYLIST_SONGS = 70
NUM_PLAYBACKS = 200
NUM_FOLLOWS = 150

# Generate Users (exclude id)
users = [{
    "username": fake.user_name(),
    "email": fake.email(),
    "password": fake.password(length=12),
    "created_at": fake.date_time_this_year()
} for _ in range(NUM_USERS)]

# Generate Songs (exclude id)
songs = [{
    "title": fake.sentence(nb_words=3).replace(".", "").replace("'", "''"),
    "artist": fake.name().replace("'", "''"),
    "album": fake.word().capitalize(),
    "duration": random.randint(120, 400)
} for _ in range(NUM_SONGS)]

# Generate Playlists (exclude id, but keep user_id)
playlists = [{
    "name": fake.catch_phrase().replace("'", "''"),
    "is_user_created": True,
    "user_id": random.randint(1, NUM_USERS),
    "created_at": fake.date_time_this_year()
} for _ in range(NUM_PLAYLISTS)]

# Generate PlaylistSongs
playlist_song_pairs = set()
while len(playlist_song_pairs) < NUM_PLAYLIST_SONGS:
    playlist_id = random.randint(1, NUM_PLAYLISTS)
    song_id = random.randint(1, NUM_SONGS)
    playlist_song_pairs.add((playlist_id, song_id))

playlist_songs = [{
    "playlist_id": pair[0],
    "song_id": pair[1],
    "added_at": fake.date_time_this_year()
} for pair in playlist_song_pairs]

# Generate Playbacks (exclude id, but keep user_id, song_id)
playbacks = [{
    "user_id": random.randint(1, NUM_USERS),
    "song_id": random.randint(1, NUM_SONGS),
    "played_at": fake.date_time_this_year(),
    "duration_played": random.randint(30, 300)
} for _ in range(NUM_PLAYBACKS)]

# Generate Follows
follow_pairs = set()
while len(follow_pairs) < NUM_FOLLOWS:
    user_id = random.randint(1, NUM_USERS)
    playlist_id = random.randint(1, NUM_PLAYLISTS)
    follow_pairs.add((user_id, playlist_id))

follows = [{
    "user_id": pair[0],
    "playlist_id": pair[1],
    "followed_at": fake.date_time_this_year()
} for pair in follow_pairs]

def sql_insert(table, columns, data):
    lines = []
    for row in data:
        values = ", ".join(
            f"'{row[col]}'" if isinstance(row[col], str)
            else f"'{row[col].isoformat(sep=' ')}'" if isinstance(row[col], datetime)
            else str(row[col]) for col in columns)
        lines.append(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({values});")
    return "\n".join(lines)

# Create SQL INSERTs
sql_script = "\n\n".join([
    sql_insert('"User"', ["username", "email", "password", "created_at"], users),
    sql_insert("Song", ["title", "artist", "album", "duration"], songs),
    sql_insert("Playlist", ["name", "is_user_created", "user_id", "created_at"], playlists),
    sql_insert("PlaylistSong", ["playlist_id", "song_id", "added_at"], playlist_songs),
    sql_insert("Playback", ["user_id", "song_id", "played_at", "duration_played"], playbacks),
    sql_insert("Follow", ["user_id", "playlist_id", "followed_at"], follows)
])

# Save SQL file
sql_path = "db/scripts/seed_data.sql"
with open(sql_path, "w") as f:
    f.write(sql_script)
