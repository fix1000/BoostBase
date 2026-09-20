import pytest
from services.song_service import SongService

def test_add_song_assign_id():
    service = SongService()
    song = service.add_song(
        title="Beat it",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

def test_add_song_assigns_unique_ids():
    service = SongService()

    song1 = service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    song2 = service.add_song(
        title="Billie Jean",
        artist="Michael Jackson",
        duration_seconds=294,
        medley=False,
        release_year=1982
    )

    assert song1.id == 1
    assert song2.id == 2

def test_add_song_rejects_duplicate_title():
    service=SongService()
    service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    with pytest.raises(ValueError):
        service.add_song(
            title="Beat It",
            artist="Michael Jackson",
            duration_seconds=258,
            medley=False,
            release_year=1982
        )

def test_get_song_by_id():
    service = SongService()
    service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )
    song = service.get_song(1)
    
    assert song.title=="Beat It"
    assert song.artist=="Michael Jackson"

def test_get_song_not_Found():
    service = SongService()
    with pytest.raises(ValueError):
        service.get_song(999999)

def test_get_all_songs():
    service = SongService()
    song1 = service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    song2 = service.add_song(
        title="Billie Jean",
        artist="Michael Jackson",
        duration_seconds=294,
        medley=False,
        release_year=1982
    )

    songs = service.get_all_songs()
    assert songs == [song1, song2]

def test_delete_song():
    service = SongService()
    song1 = service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    song2 = service.add_song(
        title="Billie Jean",
        artist="Michael Jackson",
        duration_seconds=294,
        medley=False,
        release_year=1982
    )

    service.delete_song(song1.id)

    songs= service.get_all_songs()
    assert songs == [song2]

def test_deleted_id_is_not_reused():
    service = SongService()

    song1 = service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    service.delete_song(song1.id)

    song2 = service.add_song(
        title="Billie Jean",
        artist="Michael Jackson",
        duration_seconds=294,
        medley=False,
        release_year=1982
    )

    assert song2.id == 2

def test_delete_song_not_found():
    service = SongService()

    with pytest.raises(ValueError):
        service.delete_song(99)

def test_update_song():
    service = SongService()
    song = service.add_song(
        title="Beat It",
        artist="ichael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    service.update_song(
        song.id,
        title="Beat It!",
        artist="Michael Jackson",
        duration_seconds = 260,
        medley=False,
        release_year=1982
    )
    updated_song = service.get_song(song.id)
    assert updated_song.title == "Beat It!"
    assert updated_song.artist =="Michael Jackson"
    assert updated_song.duration_seconds == 260

def test_update_song_only_changes_specified_field():
    service = SongService()

    song = service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    service.update_song(song.id, party_score=9)

    updated_song = service.get_song(song.id)

    assert updated_song.party_score == 9
    assert updated_song.title == "Beat It"
    assert updated_song.artist == "Michael Jackson"
    assert updated_song.duration_seconds == 258

def test_update_song_sets_updated_at():
    service = SongService()

    song = service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    assert song.updated_at is None

    service.update_song(song.id, party_score=9)

    assert song.updated_at is not None

def test_update_song_changes_updated_at():
    service = SongService()

    song = service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    service.update_song(song.id, party_score=9)
    first_update = song.updated_at

    service.update_song(song.id, party_score=10)
    second_update = song.updated_at

    assert second_update > first_update