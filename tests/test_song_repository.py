import json
import datetime
from models.song import Song
from services.song_repository import SongRepository

def test_save_song(tmp_path):
    repository = SongRepository(tmp_path / "songs.json")

    song = Song(
        id=1,
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    repository.save_song(song)

    with open(tmp_path / "songs.json", "r") as file:
        data = json.load(file)

    assert len(data) ==1
    assert data[0]["id"]==1
    assert data[0]["title"] =="Beat It"

def test_save_2songs(tmp_path):
    repository = SongRepository(tmp_path / "songs.json")

    song1 = Song(
        id=1,
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    repository.save_song(song1)

    song2 = Song(
        id=2,
        title="Billy Jean",
        artist="Michael Jackson",
        duration_seconds=240,
        medley=False,
        release_year=1983
    )

    repository.save_song(song2)

    with open(tmp_path / "songs.json", "r") as file:
        data = json.load(file)

    assert len(data) ==2
    assert data[0]["id"]==1
    assert data[0]["title"] =="Beat It"
    assert data[1]["id"] ==2
    assert data[1]["title"] =="Billy Jean"
    assert data[1]["artist"] =="Michael Jackson"

def test_load_songs(tmp_path):
    repository = SongRepository(tmp_path / "songs.json")

    song = Song(
        id=1,
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    repository.save_song(song)

    # Simuleer een nieuwe programma-start
    repository = SongRepository(tmp_path / "songs.json")

    songs = repository.load_songs()

    assert len(songs) == 1
    assert songs[0].id == 1
    assert songs[0].title == "Beat It"
    assert songs[0].artist == "Michael Jackson"

def test_load_multiple_songs(tmp_path):
    repository = SongRepository(tmp_path / "songs.json")

    song1 = Song(
        id=1,
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    song2 = Song(
        id=2,
        title="Billy Jean",
        artist="Michael Jackson",
        duration_seconds=240,
        medley=False,
        release_year=1983
    )

    repository.save_song(song1)
    repository.save_song(song2)

    # Simuleer een nieuwe programma-start
    repository = SongRepository(tmp_path / "songs.json")

    songs = repository.load_songs()

    assert len(songs) == 2
    assert songs[0].id == 1
    assert songs[0].title == "Beat It"
    assert songs[1].id == 2
    assert songs[1].title == "Billy Jean" 

def test_save_and_load_multiple_songs(tmp_path):
    repository = SongRepository(tmp_path / "songs.json")

    song1 = Song(
        id=1,
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        difficulty="Medium",
        genre="Pop",
        tags=["80s", "Party"],
        lead_vocals=["Marvin"],
        is_core_repertoire=True,
        party_score=9,
        original_key="E",
        transpose_to="F",
        notes="Strak einde"
    )

    song2 = Song(
        id=2,
        title="Billy Jean",
        artist="Michael Jackson",
        duration_seconds=240,
        medley=False,
        release_year=1983
    )

    repository.save_song(song1)
    repository.save_song(song2)

    # Simuleer een nieuwe programma-start
    repository = SongRepository(tmp_path / "songs.json")

    songs = repository.load_songs()

    assert len(songs) == 2

    assert songs[0].id == 1
    assert songs[0].title == "Beat It"
    assert songs[0].artist == "Michael Jackson"
    assert songs[0].duration_seconds == 258
    assert songs[0].difficulty == "Medium"
    assert songs[0].genre == "Pop"
    assert songs[0].tags == ["80s", "Party"]
    assert songs[0].lead_vocals == ["Marvin"]
    assert songs[0].is_core_repertoire is True
    assert songs[0].party_score == 9
    assert songs[0].original_key == "E"
    assert songs[0].transpose_to == "F"
    assert songs[0].notes == "Strak einde"

    assert songs[1].id == 2
    assert songs[1].title == "Billy Jean"
    assert songs[1].artist == "Michael Jackson"

def test_save_and_load_timestamps(tmp_path):
    repository = SongRepository(tmp_path / "songs.json")

    created_at = datetime.datetime(2026, 9, 20, 12, 30, 0)
    updated_at = datetime.datetime(2026, 9, 20, 13, 45, 0)

    song = Song(
        id=1,
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        created_at=created_at,
        updated_at=updated_at
    )

    repository.save_song(song)

    repository = SongRepository(tmp_path / "songs.json")
    songs = repository.load_songs()

    assert songs[0].created_at == created_at
    assert songs[0].updated_at == updated_at

def test_save_and_load_updated_at_none(tmp_path):
    repository = SongRepository(tmp_path / "songs.json")

    song = Song(
        id=1,
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        updated_at=None
    )

    repository.save_song(song)

    repository = SongRepository(tmp_path / "songs.json")
    songs = repository.load_songs()

    assert songs[0].updated_at is None