from faker import Faker
import random
from datetime import datetime

fake = Faker()
Faker.seed(42)

NUM_LISTENERS = 50
NUM_SONGS = 100
NUM_PLAYLISTS = 15
NUM_PLAYLIST_SONGS = 160
NUM_PLAYBACKS = 200
NUM_FOLLOWS = 150

# Generate Listeners
listeners = [{
    "username": fake.user_name(),
    "email": fake.email(),
    "password": fake.password(length=12),
    "created_at": fake.date_time_this_year()
} for _ in range(NUM_LISTENERS)]

# Generate Songs with URL and image URL
songs = [{
    "title": fake.sentence(nb_words=3).replace(".", "").replace("'", "''"),
    "artist": fake.name().replace("'", "''"),
    "album": fake.word().capitalize(),
    "duration": random.randint(120, 400),
    "url": f"https://your-supabase-project.supabase.co/storage/v1/object/public/songs/song{i + 1}.mp3",
    "image_url": f"https://your-supabase-project.supabase.co/storage/v1/object/public/images/song{i + 1}.jpg"
} for i in range(NUM_SONGS)]

# Generate Playlists
playlists = [{
    "name": fake.catch_phrase().replace("'", "''"),
    "is_user_created": True,
    "listener_id": random.randint(1, NUM_LISTENERS),
    "created_at": fake.date_time_this_year()
} for _ in range(NUM_PLAYLISTS)]

# Generate unique PlaylistSongs
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

# Generate Playbacks
playbacks = [{
    "listener_id": random.randint(1, NUM_LISTENERS),
    "song_id": random.randint(1, NUM_SONGS),
    "played_at": fake.date_time_this_year(),
    "duration_played": random.randint(30, 300)
} for _ in range(NUM_PLAYBACKS)]

# Generate unique Follows
follow_pairs = set()
while len(follow_pairs) < NUM_FOLLOWS:
    listener_id = random.randint(1, NUM_LISTENERS)
    playlist_id = random.randint(1, NUM_PLAYLISTS)
    follow_pairs.add((listener_id, playlist_id))

follows = [{
    "listener_id": pair[0],
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
    sql_insert("listener", ["username", "email", "password", "created_at"], listeners),
    # sql_insert("song", ["title", "artist", "album", "duration", "url", "image_url"], songs),
    sql_insert("playlist", ["name", "is_user_created", "listener_id", "created_at"], playlists),
    sql_insert("playlistsong", ["playlist_id", "song_id", "added_at"], playlist_songs),
    sql_insert("playback", ["listener_id", "song_id", "played_at", "duration_played"], playbacks),
    sql_insert("follow", ["listener_id", "playlist_id", "followed_at"], follows)
])

# Save SQL file
sql_path = "db/scripts/seed_data.sql"
with open(sql_path, "w") as f:
    f.write(sql_script)
