from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)

NUM_USERS = 10
NUM_SONGS = 30
NUM_PLAYLISTS = 8
NUM_PLAYLIST_SONGS = 40
NUM_PLAYBACKS = 50
NUM_FOLLOWS = 20

# Generate Users
users = [{
    "id": i,
    "username": fake.user_name(),
    "email": fake.email(),
    "password": fake.password(length=12),
    "created_at": fake.date_time_this_year()
} for i in range(1, NUM_USERS + 1)]

# Generate Songs
songs = [{
    "id": i,
    "title": fake.sentence(nb_words=3).replace(".", "").replace("'", "''"),
    "artist": fake.name().replace("'", "''"),
    "album": fake.word().capitalize(),
    "duration": random.randint(120, 400)
} for i in range(1, NUM_SONGS + 1)]

# Generate Playlists
playlists = [{
    "id": i,
    "name": fake.catch_phrase().replace("'", "''"),
    "is_user_created": True,
    "user_id": random.randint(1, NUM_USERS),
    "created_at": fake.date_time_this_year()
} for i in range(1, NUM_PLAYLISTS + 1)]

# Generate PlaylistSongs
playlist_songs = [{
    "playlist_id": random.randint(1, NUM_PLAYLISTS),
    "song_id": random.randint(1, NUM_SONGS),
    "added_at": fake.date_time_this_year()
} for _ in range(NUM_PLAYLIST_SONGS)]

# Generate Playbacks
playbacks = [{
    "id": i,
    "user_id": random.randint(1, NUM_USERS),
    "song_id": random.randint(1, NUM_SONGS),
    "played_at": fake.date_time_this_year(),
    "duration_played": random.randint(30, 300)
} for i in range(1, NUM_PLAYBACKS + 1)]

# Generate Follows
follows = [{
    "user_id": random.randint(1, NUM_USERS),
    "playlist_id": random.randint(1, NUM_PLAYLISTS),
    "followed_at": fake.date_time_this_year()
} for _ in range(NUM_FOLLOWS)]

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
    sql_insert('"User"', ["id", "username", "email", "password", "created_at"], users),
    sql_insert("Song", ["id", "title", "artist", "album", "duration"], songs),
    sql_insert("Playlist", ["id", "name", "is_user_created", "user_id", "created_at"], playlists),
    sql_insert("PlaylistSong", ["playlist_id", "song_id", "added_at"], playlist_songs),
    sql_insert("Playback", ["id", "user_id", "song_id", "played_at", "duration_played"], playbacks),
    sql_insert("Follow", ["user_id", "playlist_id", "followed_at"], follows)
])

# Save SQL file
sql_path = "data/music_service_custom_fake_data.sql"
with open(sql_path, "w") as f:
    f.write(sql_script)