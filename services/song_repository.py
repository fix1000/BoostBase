import json
import os
import datetime
from models.song import Song

class SongRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_song(self, song):
        song_data = {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "duration_seconds": song.duration_seconds,
            "medley": song.medley,
            "medley_titles": song.medley_titles,
            "difficulty": song.difficulty,
            "genre": song.genre,
            "tags": song.tags,
            "release_year": song.release_year,
            "lead_vocals": song.lead_vocals,
            "is_core_repertoire": song.is_core_repertoire,
            "party_score": song.party_score,
            "original_key": song.original_key,
            "transpose_to": song.transpose_to,
            "created_at": song.created_at.isoformat(),
            "updated_at": song.updated_at.isoformat() if song.updated_at else None,
            "notes": song.notes
        }
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                songs = json.load(file)
        else:
            songs = []
        songs.append(song_data)
        with open(self.file_path, "w") as file:
            json.dump(songs, file, indent=4)
    
    def load_songs(self):
        with open(self.file_path, "r") as file:
            songs_data = json.load(file)
            songs=[]
            for data in songs_data:
                created_at = datetime.datetime.fromisoformat(data["created_at"])
                if data["updated_at"] is None:
                    updated_at = None
                else:
                    updated_at = datetime.datetime.fromisoformat(data["updated_at"])

                song = Song(
                    id=data["id"],
                    title=data["title"],
                    artist=data["artist"],
                    duration_seconds=data["duration_seconds"],
                    medley=data["medley"],
                    release_year=data["release_year"],
                    medley_titles=data["medley_titles"],
                    difficulty=data["difficulty"],
                    genre=data["genre"],
                    tags=data["tags"],
                    lead_vocals=data["lead_vocals"],
                    is_core_repertoire=data["is_core_repertoire"],
                    party_score=data["party_score"],
                    original_key=data["original_key"],
                    transpose_to=data["transpose_to"],
                    notes=data["notes"],
                    created_at=created_at,
                    updated_at=updated_at
                )

                songs.append(song)
        return songs
