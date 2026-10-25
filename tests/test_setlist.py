import pytest

from models.setlist import Setlist


def test_setlist_stores_id_name_and_song_ids():
    setlist = Setlist(
        id=1,
        name="Zomerfeest",
        song_ids=[12, 7, 12, 4]
    )

    assert setlist.id == 1
    assert setlist.name == "Zomerfeest"
    assert setlist.song_ids == [12, 7, 12, 4]


def test_setlist_can_start_without_songs():
    setlist = Setlist(
        id=1,
        name="Nieuw optreden"
    )

    assert setlist.song_ids == []


def test_setlist_rejects_empty_name():
    with pytest.raises(ValueError):
        Setlist(id=1, name="   ")


def test_setlist_rejects_invalid_id():
    with pytest.raises((TypeError, ValueError)):
        Setlist(id=0, name="Zomerfeest")

def test_setlist_rejects_non_string_name():
    with pytest.raises(ValueError):
        Setlist(id=1, name=None)


def test_setlist_strips_whitespace_from_name():
    setlist = Setlist(id=1, name="  Zomerfeest  ")

    assert setlist.name == "Zomerfeest"