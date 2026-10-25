import pytest

from services.setlist_service import SetlistService
from services.setlist_repository import SetlistRepository
from models.setlist import Setlist
from unittest.mock import Mock


def test_create_setlist_assigns_id_automatically(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository, Mock())

    setlist = service.create_setlist("Zomerfeest")

    assert setlist.id == 1
    assert setlist.name == "Zomerfeest"
    assert setlist.song_ids == []

def test_create_multiple_setlists_assigns_unique_ids(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository, Mock())

    first = service.create_setlist("Zomerfeest")
    second = service.create_setlist("Bruiloft")

    assert first.id == 1
    assert second.id == 2

def test_create_setlist_does_not_reuse_deleted_id(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository, Mock())

    service.create_setlist("Zomerfeest")
    service.create_setlist("Bruiloft")

    repository.delete_setlist(2)

    new_setlist = service.create_setlist("Bedrijfsfeest")

    assert new_setlist.id == 3

def test_get_setlists_returns_saved_setlists(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository, Mock())

    service.create_setlist("Zomerfeest")
    service.create_setlist("Bruiloft")

    setlists = service.get_setlists()

    assert len(setlists) == 2
    assert setlists[0].name == "Zomerfeest"
    assert setlists[1].name == "Bruiloft"    

def test_add_song_to_setlist(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    song_repository = Mock()
    song = Mock()
    song.id = 42
    song_repository.load_songs.return_value = [song]

    service = SetlistService(repository, song_repository)

    setlist = service.create_setlist("Zomerfeest")

    service.add_song_to_setlist(setlist.id, 42)

    updated_setlist = service.get_setlists()[0]

    assert updated_setlist.song_ids == [42]

def test_add_same_song_twice_to_setlist(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")

    song_repository = Mock()
    song = Mock()
    song.id = 42
    song_repository.load_songs.return_value = [song]

    service = SetlistService(repository, song_repository)

    setlist = service.create_setlist("Zomerfeest")

    service.add_song_to_setlist(setlist.id, 42)
    service.add_song_to_setlist(setlist.id, 42)

    updated_setlist = service.get_setlists()[0]

    assert updated_setlist.song_ids == [42, 42]

def test_remove_song_from_setlist_removes_only_one_occurrence(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    song_repository = Mock()
    song_repository.load_songs.return_value = [
        Mock(id=42),
        Mock(id=17),
    ]

    service = SetlistService(repository, song_repository)

    setlist = service.create_setlist("Zomerfeest")

    service.add_song_to_setlist(setlist.id, 42)
    service.add_song_to_setlist(setlist.id, 17)
    service.add_song_to_setlist(setlist.id, 42)

    service.remove_song_from_setlist(setlist.id, 42)

    updated_setlist = service.get_setlists()[0]

    assert updated_setlist.song_ids == [17, 42]

def test_remove_song_not_in_setlist_raises_error(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    song_repository = Mock()
    song_repository.load_songs.return_value = [
        Mock(id=42),
        Mock(id=99),
    ]

    service = SetlistService(repository, song_repository)

    setlist = service.create_setlist("Zomerfeest")
    service.add_song_to_setlist(setlist.id, 42)

    with pytest.raises(ValueError, match="list.remove"):
        service.remove_song_from_setlist(setlist.id, 99)

def test_remove_song_from_setlist_is_saved_persistently(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    song_repository = Mock()
    song_repository.load_songs.return_value = [
        Mock(id=42),
        Mock(id=17),
    ]

    service = SetlistService(repository, song_repository)

    setlist = service.create_setlist("Zomerfeest")
    service.add_song_to_setlist(setlist.id, 42)
    service.add_song_to_setlist(setlist.id, 17)

    service.remove_song_from_setlist(setlist.id, 42)

    loaded_setlists = repository.load_setlists()

    assert loaded_setlists[0].song_ids == [17]

def test_remove_specific_song_occurrence_from_setlist(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    song_repository = Mock()
    song_repository.load_songs.return_value = [
        Mock(id=42),
        Mock(id=17),
    ]

    service = SetlistService(repository, song_repository)

    setlist = service.create_setlist("Zomerfeest")

    service.add_song_to_setlist(setlist.id, 42)
    service.add_song_to_setlist(setlist.id, 17)
    service.add_song_to_setlist(setlist.id, 42)

    service.remove_song_from_setlist(
        setlist.id,
        song_id=42,
        position=3,
    )

    updated_setlist = service.get_setlists()[0]

    assert updated_setlist.song_ids == [42, 17]

def test_remove_song_from_setlist_rejects_wrong_song_at_position(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    song_repository = Mock()
    song_repository.load_songs.return_value = [
        Mock(id=42),
        Mock(id=17),
    ]

    service = SetlistService(repository, song_repository)

    setlist = service.create_setlist("Zomerfeest")
    service.add_song_to_setlist(setlist.id, 42)
    service.add_song_to_setlist(setlist.id, 17)

    with pytest.raises(ValueError, match="Invalid song"):
        service.remove_song_from_setlist(
            setlist.id,
            song_id=42,
            position=2,
        )

    updated_setlist = service.get_setlists()[0]
    assert updated_setlist.song_ids == [42, 17]

@pytest.mark.parametrize("position", [0, 3])
def test_remove_song_from_setlist_rejects_out_of_range_position(
    tmp_path, position
):
    repository = SetlistRepository(tmp_path / "setlists.json")
    song_repository = Mock()
    song_repository.load_songs.return_value = [
        Mock(id=42),
        Mock(id=17),
    ]

    service = SetlistService(repository, song_repository)

    setlist = service.create_setlist("Zomerfeest")
    service.add_song_to_setlist(setlist.id, 42)
    service.add_song_to_setlist(setlist.id, 17)

    with pytest.raises(ValueError, match="Invalid song"):
        service.remove_song_from_setlist(
            setlist.id,
            song_id=42,
            position=position,
        )

    updated_setlist = service.get_setlists()[0]
    assert updated_setlist.song_ids == [42, 17]

def test_get_setlist_by_id(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository, Mock())

    first_setlist = service.create_setlist("Zomerfeest")
    service.create_setlist("Bruiloft")

    result = service.get_setlist_by_id(first_setlist.id)

    assert result.id == first_setlist.id
    assert result.name == "Zomerfeest"

def test_get_setlist_by_id_raises_error_when_not_found(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository, Mock())

    service.create_setlist("Zomerfeest")

    with pytest.raises(ValueError, match="Setlist ID not found"):
        service.get_setlist_by_id(999)

def test_get_songs_for_setlist_preserves_setlist_order(tmp_path):
    setlist_repository = SetlistRepository(tmp_path / "setlists.json")

    song_42 = Mock()
    song_42.id = 42

    song_17 = Mock()
    song_17.id = 17

    song_repository = Mock()
    song_repository.load_songs.return_value = [song_17, song_42]

    service = SetlistService(setlist_repository, song_repository)
    setlist = service.create_setlist("Zomerfeest")

    setlist.song_ids = [42, 17]
    setlist_repository.save_setlist(setlist)

    songs = service.get_songs_for_setlist(setlist.id)

    assert [song.id for song in songs] == [42, 17]

def test_get_songs_for_setlist_raises_error_for_missing_song(
    tmp_path,
):
    setlist_repository = SetlistRepository(tmp_path / "setlists.json")

    song_repository = Mock()
    song_repository.load_songs.return_value = []

    service = SetlistService(setlist_repository, song_repository)
    setlist = service.create_setlist("Zomerfeest")

    setlist.song_ids = [99]
    setlist_repository.save_setlist(setlist)

    with pytest.raises(ValueError, match="Song ID not found"):
        service.get_songs_for_setlist(setlist.id)

def test_get_songs_for_nonexistent_setlist_raises_error(tmp_path):
    setlist_repository = SetlistRepository(tmp_path / "setlists.json")

    song_repository = Mock()
    song_repository.load_songs.return_value = []

    service = SetlistService(setlist_repository, song_repository)

    with pytest.raises(ValueError, match="Setlist ID not found"):
        service.get_songs_for_setlist(999)

def test_get_songs_for_setlist_preserves_duplicate_occurrences(tmp_path):
    setlist_repository = SetlistRepository(tmp_path / "setlists.json")

    song_42 = Mock()
    song_42.id = 42

    song_repository = Mock()
    song_repository.load_songs.return_value = [song_42]

    service = SetlistService(setlist_repository, song_repository)
    setlist = service.create_setlist("Zomerfeest")

    setlist.song_ids = [42, 42]
    setlist_repository.save_setlist(setlist)

    songs = service.get_songs_for_setlist(setlist.id)

    assert [song.id for song in songs] == [42, 42]
    assert len(songs) == 2

def test_reorder_song_in_setlist(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository, Mock())

    setlist = service.create_setlist("Zomerfeest")
    setlist.song_ids = [42, 17, 99]
    repository.save_setlist(setlist)

    service.reorder_song_in_setlist(
        setlist.id,
        from_position=3,
        to_position=1,
    )

    updated_setlist = service.get_setlist_by_id(setlist.id)

    assert updated_setlist.song_ids == [99, 42, 17]

@pytest.mark.parametrize(
    ("from_position", "to_position"),
    [
        (0, 2),
        (4, 2),
        (1, 0),
        (1, 4),
    ],
)
def test_reorder_song_rejects_invalid_positions(
    tmp_path, from_position, to_position
):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository, Mock())

    setlist = service.create_setlist("Zomerfeest")
    setlist.song_ids = [42, 17, 99]
    repository.save_setlist(setlist)

    with pytest.raises(ValueError):
        service.reorder_song_in_setlist(
            setlist.id,
            from_position=from_position,
            to_position=to_position,
        )

    updated_setlist = service.get_setlist_by_id(setlist.id)
    assert updated_setlist.song_ids == [42, 17, 99]

def test_reorder_specific_duplicate_song_occurrence(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository, Mock())

    setlist = service.create_setlist("Zomerfeest")
    setlist.song_ids = [42, 17, 42]
    repository.save_setlist(setlist)

    service.reorder_song_in_setlist(
        setlist.id,
        from_position=3,
        to_position=1,
    )

    updated_setlist = service.get_setlist_by_id(setlist.id)

    assert updated_setlist.song_ids == [42, 42, 17]

def test_reorder_song_in_setlist_is_saved_persistently(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository, Mock())

    setlist = service.create_setlist("Zomerfeest")
    setlist.song_ids = [42, 17, 99]
    repository.save_setlist(setlist)

    service.reorder_song_in_setlist(
        setlist.id,
        from_position=3,
        to_position=1,
    )

    loaded_setlists = repository.load_setlists()

    assert loaded_setlists[0].song_ids == [99, 42, 17]

def test_delete_setlist_removes_it_from_repository(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository, Mock())

    setlist = service.create_setlist("Zomerfeest")

    service.delete_setlist(setlist.id)

    assert service.get_setlists() == []

def test_delete_setlist_does_not_delete_songs(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository, Mock())

    setlist = service.create_setlist("Zomerfeest")
    setlist.song_ids = [42, 17]
    repository.save_setlist(setlist)

    service.delete_setlist(setlist.id)

    assert service.get_setlists() == []
    assert setlist.song_ids == [42, 17]

def test_delete_nonexistent_setlist_raises_error(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository, Mock())

    with pytest.raises(ValueError, match="Setlist ID not found"):
        service.delete_setlist(999)

def test_find_setlists_containing_song():
    repository = Mock()
    song_repository = Mock()
    service = SetlistService(repository, song_repository)

    setlist_1 = Setlist(id=1, name="Feest", song_ids=[10, 20, 10])
    setlist_2 = Setlist(id=2, name="Rustig", song_ids=[30, 10])
    setlist_3 = Setlist(id=3, name="Rock", song_ids=[20, 30])

    repository.load_setlists.return_value = [
        setlist_1,
        setlist_2,
        setlist_3,
    ]

    result = service.find_setlists_containing_song(10)

    assert result == [setlist_1, setlist_2]

def test_find_setlists_containing_song_returns_empty_list_when_not_found():
    repository = Mock()
    song_repository = Mock()
    service = SetlistService(repository, song_repository)

    repository.load_setlists.return_value = [
        Setlist(id=1, name="Feest", song_ids=[10, 20]),
        Setlist(id=2, name="Rock", song_ids=[30, 40]),
    ]

    result = service.find_setlists_containing_song(99)

    assert result == []

def test_add_nonexistent_song_to_setlist_raises_error(tmp_path):
    setlist_repository = SetlistRepository(tmp_path / "setlists.json")

    song_repository = Mock()
    song_repository.load_songs.return_value = []

    service = SetlistService(setlist_repository, song_repository)
    setlist = service.create_setlist("Zomerfeest")

    with pytest.raises(ValueError, match="Song ID not found"):
        service.add_song_to_setlist(setlist.id, 42)

    saved_setlist = service.get_setlist_by_id(setlist.id)
    assert saved_setlist.song_ids == []
