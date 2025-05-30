from supabase import create_client, Client
from faker import Faker

from secrets import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
fake = Faker()


def update_null_albums():
    try:
        # Step 1: fetch all songs where album is NULL
        response = supabase.table("song").select("id").is_("album", None).execute()
        songs = response.data

        if not songs:
            print("No songs with NULL album found.")
            return

        print(f"Found {len(songs)} songs with NULL album.")

        # Step 2: update each song with a fake album title
        for song in songs:
            random_album = fake.catch_phrase()
            try:
                update_response = supabase.table("song").update({"album": random_album}).eq("id", song["id"]).execute()
                print(f"Updated song id {song['id']} with album: {random_album}")
            except Exception as update_error:
                print(f"Error updating song id {song['id']}: {update_error}")

    except Exception as fetch_error:
        print("Error fetching songs:", fetch_error)


if __name__ == "__main__":
    update_null_albums()
