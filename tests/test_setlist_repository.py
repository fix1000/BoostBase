import json
import pytest

from models.setlist import Setlist
from services.setlist_repository import SetlistRepository


def test_save_and_load_setlist(tmp_path):
    file_path = tmp_path / "setlists.json"
    repository = SetlistRepository(file_path)

    setlist = Setlist(
        id=1,
        name="Zomerfeest",
        song_ids=[12, 7, 4]
    )

    repository.save_setlist(setlist)
    loaded_setlists = repository.load_setlists()

    assert len(loaded_setlists) == 1
    assert loaded_setlists[0].id == 1
    assert loaded_setlists[0].name == "Zomerfeest"
    assert loaded_setlists[0].song_ids == [12, 7, 4]


def test_load_setlists_returns_empty_list_when_file_does_not_exist(tmp_path):
    file_path = tmp_path / "setlists.json"
    repository = SetlistRepository(file_path)

    assert repository.load_setlists() == []


def test_save_and_load_preserves_song_order_and_duplicates(tmp_path):
    file_path = tmp_path / "setlists.json"
    repository = SetlistRepository(file_path)

    setlist = Setlist(
        id=1,
        name="Zomerfeest",
        song_ids=[12, 7, 12, 4]
    )

    repository.save_setlist(setlist)
    loaded_setlists = repository.load_setlists()

    assert loaded_setlists[0].song_ids == [12, 7, 12, 4]

def test_save_multiple_setlists(tmp_path):
    file_path = tmp_path / "setlists.json"
    repository = SetlistRepository(file_path)

    summer_party = Setlist(id=1, name="Zomerfeest")
    wedding = Setlist(id=2, name="Bruiloft")

    repository.save_setlist(summer_party)
    repository.save_setlist(wedding)

    loaded_setlists = repository.load_setlists()

    assert len(loaded_setlists) == 2
    assert loaded_setlists[0].name == "Zomerfeest"
    assert loaded_setlists[1].name == "Bruiloft"

def test_saving_existing_setlist_updates_it(tmp_path):
    file_path = tmp_path / "setlists.json"
    repository = SetlistRepository(file_path)

    original = Setlist(id=1, name="Zomerfeest")
    updated = Setlist(
        id=1,
        name="Zomerfeest 2027",
        song_ids=[12, 7, 4]
    )

    repository.save_setlist(original)
    repository.save_setlist(updated)

    loaded_setlists = repository.load_setlists()

    assert len(loaded_setlists) == 1
    assert loaded_setlists[0].name == "Zomerfeest 2027"
    assert loaded_setlists[0].song_ids == [12, 7, 4]

def test_delete_setlist_removes_only_selected_setlist(tmp_path):
    file_path = tmp_path / "setlists.json"
    repository = SetlistRepository(file_path)

    repository.save_setlist(Setlist(id=1, name="Zomerfeest"))
    repository.save_setlist(Setlist(id=2, name="Bruiloft"))

    repository.delete_setlist(1)

    remaining_setlists = repository.load_setlists()

    assert len(remaining_setlists) == 1
    assert remaining_setlists[0].id == 2
    assert remaining_setlists[0].name == "Bruiloft"


def test_delete_nonexistent_setlist_raises_value_error(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")

    with pytest.raises(ValueError):
        repository.delete_setlist(999)

def test_next_setlist_id_is_persisted(tmp_path):
    file_path = tmp_path / "setlists.json"

    repository = SetlistRepository(file_path)

    assert repository.get_next_setlist_id() == 1
    assert repository.get_next_setlist_id() == 2

    # Create a new repository to simulate restarting the application.
    new_repository = SetlistRepository(file_path)

    assert new_repository.get_next_setlist_id() == 3

def test_new_storage_file_contains_next_id_and_setlists(tmp_path):
    file_path = tmp_path / "setlists.json"
    repository = SetlistRepository(file_path)

    repository.get_next_setlist_id()

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["next_setlist_id"] == 2
    assert data["setlists"] == []

def test_saving_setlist_preserves_next_id(tmp_path):
    file_path = tmp_path / "setlists.json"
    repository = SetlistRepository(file_path)

    repository.get_next_setlist_id()
    repository.save_setlist(Setlist(id=1, name="Zomerfeest"))

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["next_setlist_id"] == 2
    assert len(data["setlists"]) == 1