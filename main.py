import os

## Functions ##
def ensure_song_file(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("[]")

current_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_path, "data")
os.makedirs(data_path, exist_ok=True)
songs_path = os.path.join(data_path, "songs.json")
ensure_song_file(songs_path)

print("BoostBase initialized successfully.")