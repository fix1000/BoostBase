import pytest

from services.setlist_service import SetlistService
from services.setlist_repository import SetlistRepository
from models.setlist import Setlist


def test_create_setlist_assigns_id_automatically(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository)

    setlist = service.create_setlist("Zomerfeest")

    assert setlist.id == 1
    assert setlist.name == "Zomerfeest"
    assert setlist.song_ids == []

def test_create_multiple_setlists_assigns_unique_ids(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository)

    first = service.create_setlist("Zomerfeest")
    second = service.create_setlist("Bruiloft")

    assert first.id == 1
    assert second.id == 2

def test_create_setlist_does_not_reuse_deleted_id(tmp_path):
    repository = SetlistRepository(tmp_path / "setlists.json")
    service = SetlistService(repository)

    service.create_setlist("Zomerfeest")
    service.create_setlist("Bruiloft")

    repository.delete_setlist(2)

    new_setlist = service.create_setlist("Bedrijfsfeest")

    assert new_setlist.id == 3