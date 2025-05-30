import os

SONG_DIR = "list_of_songs"   # path to your songs folder
IMAGE_DIR = "images"          # path to your images folder
IMAGE_EXTENSION = ".jpg"      # target image extension (can change to .png)

# Get list of song base names (without .mp3 extension)
song_filenames = [f for f in os.listdir(SONG_DIR) if f.endswith(".mp3")]
song_basenames = [os.path.splitext(f)[0] for f in song_filenames]

# Get list of image files
image_files = [f for f in os.listdir(IMAGE_DIR) if os.path.isfile(os.path.join(IMAGE_DIR, f))]

# Check if counts match
if len(song_basenames) != len(image_files):
    print(f"⚠ WARNING: {len(song_basenames)} songs but {len(image_files)} images!")
    proceed = input("Continue renaming? (y/n): ")
    if proceed.lower() != 'y':
        exit()

# Rename each image file
for old_image, new_basename in zip(image_files, song_basenames):
    old_path = os.path.join(IMAGE_DIR, old_image)
    new_filename = new_basename + IMAGE_EXTENSION
    new_path = os.path.join(IMAGE_DIR, new_filename)
    os.rename(old_path, new_path)
    print(f"Renamed '{old_image}' → '{new_filename}'")

print("\n✅ Done renaming images.")