import pytest
from services.song_service import SongService
from services.song_repository import SongRepository
from models.song import Song

@pytest.fixture
def song_service(tmp_path):
    repository=SongRepository(tmp_path /"songs.json")
    return SongService(repository)

def test_add_song_assign_id(song_service): #song_service is een fixture voor de pytest
    song = song_service.add_song(  #song_service is een fixture voor de pytest
        title="Beat it",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

def test_add_song_assigns_unique_ids(song_service):
    song1 = song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    song2 = song_service.add_song(
        title="Billie Jean",
        artist="Michael Jackson",
        duration_seconds=294,
        medley=False,
        release_year=1982
    )

    assert song1.id == 1
    assert song2.id == 2

def test_add_song_rejects_duplicate_title(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    with pytest.raises(ValueError):
        song_service.add_song(
            title="Beat It",
            artist="Michael Jackson",
            duration_seconds=258,
            medley=False,
            release_year=1982
        )

def test_get_song_by_id(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )
    song = song_service.get_song(1)
    
    assert song.title=="Beat It"
    assert song.artist=="Michael Jackson"

def test_get_song_not_Found(song_service):
    with pytest.raises(ValueError):
        song_service.get_song(999999)

def test_get_all_songs(song_service):
    song1 = song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    song2 = song_service.add_song(
        title="Billie Jean",
        artist="Michael Jackson",
        duration_seconds=294,
        medley=False,
        release_year=1982
    )

    songs = song_service.get_all_songs()
    assert songs == [song1, song2]

def test_delete_song(song_service):
    song1 = song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    song2 = song_service.add_song(
        title="Billie Jean",
        artist="Michael Jackson",
        duration_seconds=294,
        medley=False,
        release_year=1982
    )

    song_service.delete_song(song1.id)

    songs= song_service.get_all_songs()
    assert songs == [song2]

def test_deleted_id_is_not_reused(song_service):
    song1 = song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    song_service.delete_song(song1.id)

    song2 = song_service.add_song(
        title="Billie Jean",
        artist="Michael Jackson",
        duration_seconds=294,
        medley=False,
        release_year=1982
    )

    assert song2.id == 2

def test_delete_song_not_found(song_service):
    with pytest.raises(ValueError):
        song_service.delete_song(99)

def test_update_song(song_service):
    song = song_service.add_song(
        title="Beat It",
        artist="ichael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    song_service.update_song(
        song.id,
        title="Beat It!",
        artist="Michael Jackson",
        duration_seconds = 260,
        medley=False,
        release_year=1982
    )
    updated_song = song_service.get_song(song.id)
    assert updated_song.title == "Beat It!"
    assert updated_song.artist =="Michael Jackson"
    assert updated_song.duration_seconds == 260

def test_update_song_only_changes_specified_field(song_service):
    song = song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    song_service.update_song(song.id, party_score=9)

    updated_song = song_service.get_song(song.id)

    assert updated_song.party_score == 9
    assert updated_song.title == "Beat It"
    assert updated_song.artist == "Michael Jackson"
    assert updated_song.duration_seconds == 258

def test_update_song_sets_updated_at(song_service):
    song = song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    assert song.updated_at is None

    song_service.update_song(song.id, party_score=9)

    assert song.updated_at is not None

def test_update_song_changes_updated_at(song_service):
    song = song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    song_service.update_song(song.id, party_score=9)
    first_update = song.updated_at

    song_service.update_song(song.id, party_score=10)
    second_update = song.updated_at

    assert second_update > first_update

def test_add_song_saves_song_to_repository(tmp_path):
    repository = SongRepository(tmp_path / "songs.json")
    service= SongService(repository)

    song=service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )
    
    songs=repository.load_songs()
    assert len(songs) == 1
    assert songs[0].title == "Beat It"

def test_service_loads_existing_songs(tmp_path):
    repository = SongRepository(tmp_path / "songs.json")
    song= Song(
        id=1,
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )
    repository.save_song(song)
    
    newservice = SongService(repository)
    songs=newservice.get_all_songs()
    assert len(songs) ==1
    assert songs[0].title=="Beat It"

def test_service_assigns_higher_id_after_loading_existing_songs(tmp_path):
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
        title="Fate of Ophelia",
        artist="Taylor Swift",
        duration_seconds=201,
        medley=False,
        release_year=2026
    )
    repository.save_song(song2)

    newservice = SongService(repository)

    song3 = newservice.add_song(
        title="Next Generation",
        artist="Alphaville",
        duration_seconds=350,
        medley=False,
        release_year=1995
    )

    assert song3.id == 3

def test_update_song_saves_changes_to_repository(tmp_path):
        repository = SongRepository(tmp_path / "songs.json")
        service = SongService(repository)
        song=service.add_song(
            title="Beat It",
            artist="Michael Jackson",
            duration_seconds=258,
            medley=False,
            release_year=1982
        )
        service.update_song(song.id, party_score=9)

        songs=repository.load_songs()

        assert len(songs) ==1
        assert songs[0].party_score ==9

def test_delete_song_saves_changes_to_repository(tmp_path):
        repository = SongRepository(tmp_path / "songs.json")
        service = SongService(repository)
        song=service.add_song(
            title="Beat It",
            artist="Michael Jackson",
            duration_seconds=258,
            medley=False,
            release_year=1982
        )
        service.delete_song(song.id)
        songs = repository.load_songs()
        assert len(songs) == 0


