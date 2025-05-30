from supabase import create_client, Client
import os
from mutagen.mp3 import MP3  # for getting mp3 duration
import re

from secrets import SUPABASE_KEY, SUPABASE_URL

# CONFIGURE HERE
SONG_BUCKET = "songs"
IMAGE_BUCKET = "images"
SONGS_DIR = "list_of_songs"
IMAGE_DIR = "images"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def clean_title_and_artist(filename):
    base = os.path.splitext(filename)[0]
    match = re.match(r"(.+)-\((.+)\)", base)
    if match:
        title = match.group(1).replace("-", " ").strip()
        artist = match.group(2).strip()
    else:
        title = base.replace("-", " ").strip()
        artist = "Unknown"
    return title, artist

def upload_and_insert():
    for filename in os.listdir(SONGS_DIR):
        if filename.endswith(".mp3"):
            file_path = os.path.join(SONGS_DIR, filename)
            title, artist = clean_title_and_artist(filename)

            # Get duration in seconds
            audio = MP3(file_path)
            duration = int(audio.info.length)

            # Upload song file
            song_storage_path = filename  # keep original name

            with open(file_path, "rb") as f:
                supabase.storage.from_(SONG_BUCKET).upload(song_storage_path, f, {"content-type": "audio/mpeg"})

            song_url = supabase.storage.from_(SONG_BUCKET).get_public_url(song_storage_path)

            # Upload corresponding image (same base filename + .jpg)
            image_filename = os.path.splitext(filename)[0] + ".jpg"
            image_file_path = os.path.join(IMAGE_DIR, image_filename)
            if os.path.exists(image_file_path):
                with open(image_file_path, "rb") as img_f:
                    supabase.storage.from_(IMAGE_BUCKET).upload(image_filename, img_f, {"content-type": "image/jpeg"})
                image_url = supabase.storage.from_(IMAGE_BUCKET).get_public_url(image_filename)
            else:
                image_url = None  # fallback if image missing

            # Pretty print
            print(f"\n🎵 Uploaded Song:")
            print(f"  Title     : {title}")
            print(f"  Artist    : {artist}")
            print(f"  Duration  : {duration} sec")
            print(f"  Song URL  : {song_url}")
            print(f"  Image URL : {image_url}")

            # Insert into DB
            supabase.table("song").insert({
                "title": title,
                "artist": artist,
                "album": None,
                "duration": duration,
                "url": song_url,
                "image_url": image_url
            }).execute()

if __name__ == "__main__":
    upload_and_insert()
