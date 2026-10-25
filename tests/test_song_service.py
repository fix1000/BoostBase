import pytest
from services.song_service import SongService
from services.song_repository import SongRepository
from services.setlist_repository import SetlistRepository
from services.setlist_service import SetlistService
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


def test_search_songs_by_title(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    song_service.add_song(
        title="Billie Jean",
        artist="Michael Jackson",
        duration_seconds=294,
        medley=False,
        release_year=1982
    )

    results = song_service.search_songs(title="Beat")

    assert len(results) == 1
    assert results[0].title == "Beat It"

def test_search_songs_by_title_is_case_insensitive(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    results = song_service.search_songs(title="beat")

    assert len(results) == 1
    assert results[0].title == "Beat It"

def test_search_songs_returns_empty_list_when_no_match(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    results = song_service.search_songs(title="Purple Rain")

    assert results == []

def test_search_songs_rejects_empty_title(song_service):
    with pytest.raises(ValueError, match="Voer een zoekterm in"):
        song_service.search_songs(title="")

def test_search_songs_rejects_whitespace_title(song_service):
    with pytest.raises(ValueError, match="Voer een zoekterm in"):
        song_service.search_songs(title="   ")

def test_search_songs_by_artist(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )
    results = song_service.search_songs(artist="Michael Jackson")
    assert len(results) == 1
    assert results[0].artist == "Michael Jackson"

def test_search_songs_diffcat(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        genre="Pop"
    )
    song_service.add_song(
        title="Billy Jean",
        artist="Michael Jackson",
        duration_seconds=248,
        medley=False,
        release_year=1983,
        genre="Rock"
    )
    song_service.add_song(
        title="Purple Rain",
        artist="Prince",
        duration_seconds=458,
        medley=False,
        release_year=1985,
        genre="Pop"
    )
    results = song_service.search_songs(artist="Michael Jackson", genre = "Pop")
    assert len(results) == 1
    assert results[0].title == "Beat It"

def test_add_songs_with_genre(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        genre="Pop"
    )
    songs = song_service.get_all_songs()
    assert len(songs) ==1
    assert songs[0].genre == "Pop"

def test_search_songs_by_release_year(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        genre="Pop"
    )
    song_service.add_song(
        title="Purple Rain",
        artist="Prince",
        duration_seconds=458,
        medley=False,
        release_year=1985,
        genre="Pop"
    )
    results = song_service.search_songs(release_year=1982)
    assert len(results) ==1
    assert results[0].title == "Beat It"

def test_search_songs_by_medley(song_service):

    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        genre="Pop"
    )

    song_service.add_song(
        title="Grease Megamix",
        artist="Various",
        duration_seconds=300,
        medley=True,
        medley_titles=["Grease; Greased Lightnin'"],
        release_year=1978,
        genre="Pop"
    )

    results = song_service.search_songs(medley=True)

    assert len(results) == 1
    assert results[0].title == "Grease Megamix"

def test_search_songs_by_partial_genre(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        genre="Pop"
    )
    results = song_service.search_songs(genre = "Po")
    assert len(results) ==1
    assert results[0].genre == "Pop"

def test_search_songs_by_genre_returns_empty_when_no_match(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        genre="Pop"
    )

    results = song_service.search_songs(genre="Jazz")

    assert results == []

def test_search_songs_by_genre_when_song_has_no_genre(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    results = song_service.search_songs(genre="Pop")

    assert results == []

def test_search_songs_skips_missing_genre(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982
    )

    song_service.add_song(
        title="Billie Jean",
        artist="Michael Jackson",
        duration_seconds=294,
        medley=False,
        release_year=1982,
        genre="Pop"
    )

    results = song_service.search_songs(genre="Pop")

    assert len(results) == 1
    assert results[0].title == "Billie Jean"

def test_search_song_with_one_tag(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        tags=["Dutch", "Party", "Tent"]
    )

    song_service.add_song(
        title="Billie Jean",
        artist="Michael Jackson",
        duration_seconds=294,
        medley=False,
        release_year=1982,
        genre="Pop"
    )

    results = song_service.search_songs(tags="Party")
    assert len(results) ==1
    assert results[0].tags == ["Dutch", "Party", "Tent"]

def test_search_songs_by_tag_returns_empty_when_no_match(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        tags=["Dutch", "Party", "Tent"]
    )

    results = song_service.search_songs(tags="Partie")

    assert results == []

def test_search_songs_by_tag_returns_empty_when_partial_match(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        tags=["Dutch", "Party", "Tent"]
    )

    results = song_service.search_songs(tags="Part")

    assert results == []

def test_search_song_with_one_tag_in_lower(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        tags=["Dutch", "Party", "Tent"]
    )

    results = song_service.search_songs(tags="party")
    assert len(results) ==1
    assert results[0].tags == ["Dutch", "Party", "Tent"]


def test_search_songs_by_any_tag(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        tags=["Dutch", "Party"]
    )

    song_service.add_song(
        title="Billie Jean",
        artist="Michael Jackson",
        duration_seconds=294,
        medley=False,
        release_year=1982,
        tags=["Dutch"]
    )

    song_service.add_song(
        title="Purple Rain",
        artist="Prince",
        duration_seconds=458,
        medley=False,
        release_year=1985,
        tags=["Party"]
    )

    song_service.add_song(
        title="Smells Like Teen Spirit",
        artist="Nirvana",
        duration_seconds=301,
        medley=False,
        release_year=1991,
        tags=["Rock"]
    )

    results = song_service.search_songs(tags_any=["Dutch", "Party"])

    assert len(results) == 3
    assert {song.title for song in results} == {
        "Beat It",
        "Billie Jean",
        "Purple Rain"
    }

def test_search_songs_by_all_tags(song_service):
    song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
        tags=["Dutch", "Party"]
    )

    song_service.add_song(
        title="Billie Jean",
        artist="Michael Jackson",
        duration_seconds=294,
        medley=False,
        release_year=1982,
        tags=["Dutch"]
    )

    song_service.add_song(
        title="Purple Rain",
        artist="Prince",
        duration_seconds=458,
        medley=False,
        release_year=1985,
        tags=["Party"]
    )

    song_service.add_song(
        title="Smells Like Teen Spirit",
        artist="Nirvana",
        duration_seconds=301,
        medley=False,
        release_year=1991,
        tags=["Rock"]
    )

    results = song_service.search_songs(tags_all=["Dutch", "Party"])

    assert len(results) == 1
    assert results[0].title == "Beat It"


def test_search_songs_by_lead_vocals(song_service):
    song_service.add_song(
        title="Example Song",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        lead_vocals=["Bianca", "Peter"]
    )

    results = song_service.search_songs(lead_vocals="bianca")

    assert len(results) == 1
    assert results[0].title == "Example Song"


def test_search_songs_by_partial_difficulty(song_service):
    song_service.add_song(
        title="Example Song",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        difficulty="Medium"
    )

    results = song_service.search_songs(difficulty="med")

    assert len(results) == 1
    assert results[0].title == "Example Song"


def test_search_songs_by_core_repertoire_false(song_service):
    song_service.add_song(
        title="Core Song",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        is_core_repertoire=True
    )

    song_service.add_song(
        title="Occasional Song",
        artist="Example Artist",
        duration_seconds=200,
        medley=False,
        release_year=2021,
        is_core_repertoire=False
    )

    results = song_service.search_songs(is_core_repertoire=False)

    assert len(results) == 1
    assert results[0].title == "Occasional Song"

def test_search_songs_by_party_score(song_service):
    song_service.add_song(
        title="High Energy",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        party_score=9
    )

    song_service.add_song(
        title="Good Song",
        artist="Another Artist",
        duration_seconds=200,
        medley=False,
        release_year=2021,
        party_score=8
    )

    results = song_service.search_songs(party_score=9)

    assert len(results) == 1
    assert results[0].title == "High Energy"


def test_search_songs_by_minimum_party_score(song_service):
    song_service.add_song(
        title="Score Seven",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        party_score=7
    )

    song_service.add_song(
        title="Score Eight",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        party_score=8
    )

    song_service.add_song(
        title="Score Nine",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        party_score=9
    )

    results = song_service.search_songs(party_score_min=8)

    assert len(results) == 2
    assert [song.title for song in results] == ["Score Eight", "Score Nine"]


def test_search_songs_by_partial_medley_title(song_service):
    song_service.add_song(
        title="Michael Jackson Medley",
        artist="Michael Jackson",
        duration_seconds=600,
        medley=True,
        release_year=1980,
        medley_titles=[
            "Don't Stop Till You Get Enough",
            "Billie Jean",
            "Beat It"
        ]
    )

    results = song_service.search_songs(medley_titles="don't stop")

    assert len(results) == 1
    assert results[0].title == "Michael Jackson Medley"

def test_search_songs_by_original_key(song_service):
    song_service.add_song(
        title="Example Song",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        original_key="F#"
    )

    results = song_service.search_songs(original_key="f#")

    assert len(results) == 1
    assert results[0].title == "Example Song"

def test_search_songs_by_transpose_to(song_service):
    song_service.add_song(
        title="Example Song",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        original_key="E",
        transpose_to="F#"
    )

    results = song_service.search_songs(transpose_to="f#")

    assert len(results) == 1
    assert results[0].title == "Example Song"


def test_search_songs_by_playable_key(song_service):
    song_service.add_song(
        title="Transposed Song",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        original_key="E",
        transpose_to="F#"
    )

    song_service.add_song(
        title="Original Key Song",
        artist="Another Artist",
        duration_seconds=200,
        medley=False,
        release_year=2021,
        original_key="C"
    )

    results_f_sharp = song_service.search_songs(playable_key="F#")
    results_c = song_service.search_songs(playable_key="C")

    assert len(results_f_sharp) == 1
    assert results_f_sharp[0].title == "Transposed Song"

    assert len(results_c) == 1
    assert results_c[0].title == "Original Key Song"

def test_search_songs_without_criteria_raises_error(song_service):
    with pytest.raises(ValueError, match="Voer een zoekterm in"):
        song_service.search_songs()

def test_search_songs_with_none_criterion_raises_error(song_service):
    with pytest.raises(ValueError, match="Voer een zoekterm in"):
        song_service.search_songs(playable_key=None)

def test_search_songs_with_empty_playable_key_raises_error(song_service):
    with pytest.raises(ValueError, match="Voer een zoekterm in"):
        song_service.search_songs(playable_key="")

def test_search_songs_with_empty_tags_any_raises_error(song_service):
    with pytest.raises(ValueError, match="Voer een zoekterm in"):
        song_service.search_songs(tags_any=[])


def test_search_songs_with_empty_tags_all_raises_error(song_service):
    with pytest.raises(ValueError, match="Voer een zoekterm in"):
        song_service.search_songs(tags_all=[])

def test_search_songs_with_playable_key_none_and_artist(song_service):
    song_service.add_song(
        title="Example Song",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        original_key="E"
    )

    results = song_service.search_songs(
        artist="Example Artist",
        playable_key=None
    )

    assert len(results) == 1
    assert results[0].title == "Example Song"


def test_search_songs_by_playable_key_and_artist(song_service):
    song_service.add_song(
        title="Matching Song",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        original_key="E",
        transpose_to="F#"
    )

    song_service.add_song(
        title="Different Artist",
        artist="Other Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        original_key="E",
        transpose_to="F#"
    )

    results = song_service.search_songs(
        playable_key="F#",
        artist="Example Artist"
    )

    assert len(results) == 1
    assert results[0].title == "Matching Song"

def test_search_songs_by_tags_any_and_minimum_party_score(song_service):
    song_service.add_song(
        title="High Score Party Song",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        tags=["Dutch", "Party"],
        party_score=9
    )

    song_service.add_song(
        title="Low Score Party Song",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        tags=["Party"],
        party_score=6
    )

    song_service.add_song(
        title="High Score Rock Song",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        tags=["Rock"],
        party_score=9
    )

    results = song_service.search_songs(
        tags_any=["Party", "Dutch"],
        party_score_min=8
    )

    assert len(results) == 1
    assert results[0].title == "High Score Party Song"

def test_search_songs_with_unknown_criterion_raises_error(song_service):
    with pytest.raises(ValueError, match="Onbekend zoekcriterium"):
        song_service.search_songs(banana="test")

def test_search_songs_by_tags_all_and_minimum_party_score(song_service):
    song_service.add_song(
        title="Matching Song",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        tags=["Dutch", "Party", "Tent"],
        party_score=9
    )

    song_service.add_song(
        title="Missing Tag Song",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        tags=["Dutch", "Party"],
        party_score=9
    )

    song_service.add_song(
        title="Low Score Song",
        artist="Example Artist",
        duration_seconds=180,
        medley=False,
        release_year=2020,
        tags=["Dutch", "Party", "Tent"],
        party_score=6
    )

    results = song_service.search_songs(
        tags_all=["Dutch", "Tent"],
        party_score_min=8
    )

    assert len(results) == 1
    assert results[0].title == "Matching Song"

def test_search_songs_with_valid_and_unknown_criteria_raises_error(song_service):
    with pytest.raises(ValueError, match="Onbekend zoekcriterium"):
        song_service.search_songs(
            artist="Queen",
            banana="test"
        )



def test_cancel_deleting_song_keeps_song_and_setlist_unchanged(
    tmp_path,
):
    song_repository = SongRepository(tmp_path / "songs.json")
    song_service = SongService(song_repository)

    song = song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
    )

    setlist_repository = SetlistRepository(tmp_path / "setlists.json")
    setlist_service = SetlistService(setlist_repository, song_repository)

    setlist = setlist_service.create_setlist("Feest")
    setlist_service.add_song_to_setlist(setlist.id, song.id)

    # The user cancels the deletion.
    # The song and its setlist reference must remain unchanged.
    assert song_service.get_all_songs() == [song]
    assert setlist_service.get_setlist_by_id(setlist.id).song_ids == [song.id]



def test_delete_song_in_setlist_requires_confirmation(
    tmp_path,
):
    song_repository = SongRepository(tmp_path / "songs.json")
    setlist_repository = SetlistRepository(tmp_path / "setlists.json")
    setlist_service = SetlistService(setlist_repository, song_repository)
    song_service = SongService(song_repository, setlist_service)

    song = song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
    )

    setlist = setlist_service.create_setlist("Feest")
    setlist_service.add_song_to_setlist(setlist.id, song.id)

    with pytest.raises(ValueError, match="setlist"):
        song_service.delete_song(song.id)

    assert song_service.get_all_songs() == [song]
    assert setlist_service.get_setlist_by_id(setlist.id).song_ids == [song.id]


def test_confirmed_song_deletion_removes_all_setlist_references(tmp_path):
    song_repository = SongRepository(tmp_path / "songs.json")
    setlist_repository = SetlistRepository(tmp_path / "setlists.json")

    setlist_service = SetlistService(setlist_repository, song_repository)
    song_service = SongService(song_repository, setlist_service)

    song = song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
    )

    other_song = song_service.add_song(
        title="Billie Jean",
        artist="Michael Jackson",
        duration_seconds=294,
        medley=False,
        release_year=1982,
    )

    feest = setlist_service.create_setlist("Feest")
    rock = setlist_service.create_setlist("Rock")

    setlist_service.add_song_to_setlist(feest.id, song.id)
    setlist_service.add_song_to_setlist(feest.id, other_song.id)
    setlist_service.add_song_to_setlist(feest.id, song.id)
    setlist_service.add_song_to_setlist(rock.id, song.id)

    song_service.delete_song(song.id, confirmed=True)

    assert [s.id for s in song_repository.load_songs()] == [other_song.id]
    assert setlist_service.get_setlist_by_id(feest.id).song_ids == [
        other_song.id
    ]
    assert setlist_service.get_setlist_by_id(rock.id).song_ids == []



def test_failed_setlist_save_keeps_song_in_repository(tmp_path, monkeypatch):
    song_repository = SongRepository(tmp_path / "songs.json")
    setlist_repository = SetlistRepository(tmp_path / "setlists.json")

    setlist_service = SetlistService(setlist_repository, song_repository)
    song_service = SongService(song_repository, setlist_service)

    song = song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
    )

    setlist = setlist_service.create_setlist("Feest")
    setlist_service.add_song_to_setlist(setlist.id, song.id)

    def fail_save_setlist(setlist):
        raise OSError("Simulated setlist save failure")

    monkeypatch.setattr(
        setlist_repository,
        "save_setlist",
        fail_save_setlist,
    )

    with pytest.raises(OSError, match="Simulated setlist save failure"):
        song_service.delete_song(song.id, confirmed=True)

    saved_songs = song_repository.load_songs()
    assert [saved_song.id for saved_song in saved_songs] == [song.id]


def test_failed_second_setlist_save_keeps_song_in_repository(
    tmp_path,
    monkeypatch,
):
    song_repository = SongRepository(tmp_path / "songs.json")
    setlist_repository = SetlistRepository(tmp_path / "setlists.json")

    setlist_service = SetlistService(setlist_repository, song_repository)
    song_service = SongService(song_repository, setlist_service)

    song = song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
    )

    first_setlist = setlist_service.create_setlist("Feest")
    second_setlist = setlist_service.create_setlist("Rock")

    setlist_service.add_song_to_setlist(first_setlist.id, song.id)
    setlist_service.add_song_to_setlist(second_setlist.id, song.id)

    original_save = setlist_repository.save_setlist
    save_count = 0

    def fail_on_second_save(setlist):
        nonlocal save_count
        save_count += 1

        if save_count == 2:
            raise OSError("Simulated second save failure")

        original_save(setlist)

    monkeypatch.setattr(
        setlist_repository,
        "save_setlist",
        fail_on_second_save,
    )

    with pytest.raises(OSError, match="Simulated second save failure"):
        song_service.delete_song(song.id, confirmed=True)

    saved_songs = song_repository.load_songs()
    assert [saved_song.id for saved_song in saved_songs] == [song.id]
    saved_setlists = setlist_repository.load_setlists()
    assert saved_setlists[0].song_ids == [song.id]
    assert saved_setlists[1].song_ids == [song.id]


def test_failed_song_deletion_restores_setlist_references(
    tmp_path,
    monkeypatch,
):
    song_repository = SongRepository(tmp_path / "songs.json")
    setlist_repository = SetlistRepository(tmp_path / "setlists.json")

    setlist_service = SetlistService(setlist_repository, song_repository)
    song_service = SongService(song_repository, setlist_service)

    song = song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
    )

    setlist = setlist_service.create_setlist("Feest")
    setlist_service.add_song_to_setlist(setlist.id, song.id)

    def fail_delete_song(song):
        raise OSError("Simulated song deletion failure")

    monkeypatch.setattr(
        song_repository,
        "delete_song",
        fail_delete_song,
    )

    with pytest.raises(OSError, match="Simulated song deletion failure"):
        song_service.delete_song(song.id, confirmed=True)

    saved_songs = song_repository.load_songs()
    saved_setlist = setlist_repository.load_setlists()[0]

    assert [saved_song.id for saved_song in saved_songs] == [song.id]
    assert saved_setlist.song_ids == [song.id]

def test_delete_song_warning_identifies_affected_setlist(tmp_path):
    song_repository = SongRepository(tmp_path / "songs.json")
    setlist_repository = SetlistRepository(tmp_path / "setlists.json")
    setlist_service = SetlistService(setlist_repository, song_repository)
    song_service = SongService(song_repository, setlist_service)

    song = song_service.add_song(
        title="Beat It",
        artist="Michael Jackson",
        duration_seconds=258,
        medley=False,
        release_year=1982,
    )

    setlist = setlist_service.create_setlist("Zomerfeest")
    setlist_service.add_song_to_setlist(setlist.id, song.id)

    with pytest.raises(ValueError, match="Zomerfeest"):
        song_service.delete_song(song.id)
