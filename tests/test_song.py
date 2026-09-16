import pytest
import datetime
from models.song import Song

def test_song_creation():
    song1 = Song(1, "ABC", "Michael Jackson", 210, False, 1976)

    assert song1.title == "ABC"
    assert song1.artist == "Michael Jackson"
    assert song1.duration_seconds == 210
    assert song1.medley is False
    assert song1.tags == []

def test_song_optional_fields():
    song1 = Song(1, "ABC", "Michael Jackson", 210, False, 1976)

    assert song1.party_score is None
    assert song1.difficulty is None
    assert song1.genre is None
    assert song1.tags == []
    assert song1.lead_vocals == []
    assert song1.created_at is not None
    assert song1.updated_at is None
    assert str(song1) == "id: 1, Title: ABC, Artist: Michael Jackson, Score: None"

def test_song_with_optional_fields():
    song = Song(1, "Beat it", "Michael Jackson", 258, False, 1982, party_score=9, genre="Pop", tags=["Party", "Classic", "Funk"], lead_vocals=["Gilbert"], is_core_repertoire=True, original_key="D", transpose_to="C", notes="Check ending" )

    assert song.party_score ==9
    assert song.genre =="Pop"
    assert song.tags == ["Party", "Classic", "Funk"]
    assert song.lead_vocals ==["Gilbert"]
    assert song.is_core_repertoire == True
    assert song.original_key == "D"
    assert song.transpose_to =="C"
    assert song.notes == "Check ending"

def test_song_invalid_id():
    with pytest.raises(ValueError):
        Song(0, "ABC", "Michael Jackson", 210, False, 1976)

def test_song_id_not_int():
    with pytest.raises(TypeError):
        Song("1", "ABC", "Michael Jackson", 210, False, 1976)

def test_song_id_bool():
    with pytest.raises(TypeError):
        Song(True, "ABC", "Michael Jackson", 210, False, 1976)

def test_song_None_in_Title():
    with pytest.raises(ValueError):
        Song(1, None, "Michael Jackson", 210, False, 1976)

def test_song_Title_301kar():
    with pytest.raises(ValueError):
        Song(1, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0", "Michael Jackson", 210, False, 1976 )
        
def test_song_onlySpaces_in_Title():
    with pytest.raises(ValueError):
        Song(1, "   ", "Michael Jackson", 210, False, 1976)

def test_correct_title_trimmed():
    song = Song(1, "  Beat It   ", "Michael Jackson", 210, False, 1976)
    assert song.title =="Beat It"


def test_song_None_in_Artist():
    with pytest.raises(ValueError):
        Song(1, "Black or White", None, 210, False, 1976)

def test_song_artist_301Char():
    with pytest.raises(ValueError):
        Song(1, "ABC", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0", 210, False, 1976)
        
def test_song_onlySpaces_in_Artist():
    with pytest.raises(ValueError):
        Song(1, "Ghosts", "   ", 210, False, 1976)

def test_correct_Artist_trimmed():
    song = Song(1, "  Beat It", "           Michael Jackson    ", 210, False, 1976)
    assert song.artist =="Michael Jackson"

def test_DurSec_NotIntButBool():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", True, False, 1976)
    
def test_DurSec_String():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", "string_gemaakt", False, 1976)

def test_DurSec_min():
    song = Song(1, "ABC", "Michael Jackson", 10, False, 1976)

    assert song.duration_seconds == 10

def test_DurSec_tooLow():
    with pytest.raises(ValueError):
        song = Song(1, "ABC", "Michael Jackson", 6, False, 1976)

def test_DurSec_max():
    song = Song(1, "ABC", "Michael Jackson", 1000, False, 1976)
    assert song.duration_seconds == 1000

def test_DurSec_tooHigh():
    with pytest.raises(ValueError):
        song = Song(1, "ABC", "Michael Jackson", 1001, False, 1976)    

# medley = "True"     → TypeError
def test_medley_string():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", 210, "True", 1976)

def test_medley_Int():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", 210, 1, 1976)

# medley = None       → TypeError
def test_medley_None():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", 210, None, 1976)

def test_medley_false():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976)
    assert song.medley is False

# medley_titles -> Als meldey ja: dan ook medley titles meegeven
def test_medley_medleyWithTitles():
    song = Song(1, "Early megamix", "Michael Jackson", 810, True, 1980, medley_titles=["ABC", "Don't stop till you get enough", "Off the Wall"])
    assert song.medley == True
    assert song.medley_titles == ["ABC", "Don't stop till you get enough", "Off the Wall"]

# als medley ja, geen none medley titles
def test_medley_medleyYesTitlesNone():
    with pytest.raises(TypeError):
        song = Song(1, "Early megamix", "Michael Jackson", 810, True, 1980, medley_titles=None)

#titles leeg in lijst
def test_medley_medleyYesTitlesEmpty():
    with pytest.raises(ValueError):
        song = Song(1, "Early megamix", "Michael Jackson", 810, True, 1980, medley_titles=[])

#Medley False, maar we medley titels
def test_medley_MedleyFalseWithTitles():
    with pytest.raises(ValueError):
        song = Song(1, "ABC", "Michael Jackson", 810, False, 1980, medley_titles=["ABC", "Don't stop till you get enough", "Off the Wall"])

#nu de list check op strings
def test_medley_titles_only_strings():
    with pytest.raises(TypeError):
        song = Song(1, "Early megamix", "Michael Jackson", 810, True, 1980, medley_titles=["ABC", 123, True])

def test_medley_titles_nolist():
    with pytest.raises(TypeError):
        song = Song(1, "Early megamix", "Michael Jackson", 810, True, 1980, medley_titles="ABC")

#release year, tussen 1900 en 2100
def test_release_year_isString():
    with pytest.raises(TypeError):
        song = Song(1, "Early megamix", "Michael Jackson", 810, True, "1980", medley_titles=["ABC", "Don't stop till you get enough", "Off the Wall"])

def test_release_year_Before1900():
    with pytest.raises(ValueError):
        song = Song(1, "Early megamix", "Michael Jackson", 810, True, 1899, medley_titles=["ABC", "Don't stop till you get enough", "Off the Wall"])

def test_release_year_after2100():
    with pytest.raises(ValueError):
        song = Song(1, "Early megamix", "Michael Jackson", 810, True, 2101, medley_titles=["ABC", "Don't stop till you get enough", "Off the Wall"])

def test_release_year_2100():
    song = Song(1, "Early megamix", "Michael Jackson", 810, True, 2100, medley_titles=["ABC", "Don't stop till you get enough", "Off the Wall"])
    assert song.release_year == 2100

def test_party_score_isString():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score="8")

def test_party_score_isBool():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=True)

def test_party_score_is0():
    with pytest.raises(ValueError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=0)

def test_party_score_is1():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=1)
    assert song.party_score == 1

def test_party_score_is10():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10)
    assert song.party_score ==10

def test_party_score_is11():
    with pytest.raises(ValueError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=11)

def test_difficulty_Medium():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty="Medium")
    assert song.difficulty == "Medium"

def test_difficulty_VeryEasy():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty="Very Easy")
    assert song.difficulty == "Very Easy"

def test_difficulty_VeryHard():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty="Very Hard")
    assert song.difficulty == "Very Hard"

def test_difficulty_Impossible():
    with pytest.raises(ValueError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty="Impossible")

def test_difficulty_123():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty=123)

def test_genre_Pop():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty="Very Hard", genre="Pop")
    assert song.genre == "Pop"

def test_genre_Limburgs():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty="Very Hard", genre="Limburgs")
    assert song.genre == "Limburgs"

def test_genre_HM():
    with pytest.raises(ValueError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty="Very Hard", genre="Heavy Metal")

def test_genre_123():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty="Very Hard", genre=123)

def test_tags_emptyList():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty="Very Hard", genre="Limburgs", tags=[])
    assert song.tags == []

def test_tags_partyListString():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty="Very Hard", genre="Limburgs", tags=["Party"])
    assert song.tags == ["Party"]

def test_tags_partyString():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty="Very Hard", genre="Limburgs", tags="Party")

def test_tags_123list():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty="Very Hard", genre="Limburgs", tags=[123])

def test_tags_multboollist():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty="Very Hard", genre="Limburgs", tags=["Party", True])

def test_tags_multiple():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, difficulty="Very Hard", genre="Limburgs", tags=["Party", "Limburgs", "Gouwe Ouwe"])
    assert song.tags == ["Party", "Limburgs", "Gouwe Ouwe"]

def test_lead_vocals_single():
    song = Song(
        1, "ABC", "Michael Jackson", 210, False, 1976,
        lead_vocals=["Gilbert"]
    )
    assert song.lead_vocals == ["Gilbert"]


def test_lead_vocals_multiple():
    song = Song(
        1, "ABC", "Michael Jackson", 210, False, 1976,
        lead_vocals=["Gilbert", "Ricardo"]
    )
    assert song.lead_vocals == ["Gilbert", "Ricardo"]


def test_lead_vocals_not_list():
    with pytest.raises(TypeError):
        Song(
            1, "ABC", "Michael Jackson", 210, False, 1976,
            lead_vocals="Gilbert"
        )


def test_lead_vocals_contains_non_string():
    with pytest.raises(TypeError):
        Song(
            1, "ABC", "Michael Jackson", 210, False, 1976,
            lead_vocals=["Gilbert", 123]
        )

def test_core_repertoireTrue():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, is_core_repertoire=True)
    assert song.is_core_repertoire == True

def test_core_repertoireFalse():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, is_core_repertoire=False)
    assert song.is_core_repertoire == False

def test_core_repertoireStrFalse():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, is_core_repertoire="False")

def test_core_repertoire0():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, party_score=10, is_core_repertoire=0)

def test_core_repertoireNone():
    song = Song(        1, "ABC", "Michael Jackson", 210, False, 1976, is_core_repertoire=None)
    assert song.is_core_repertoire is None

def test_origKey_Fis():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, original_key="F#")
    assert song.original_key == "F#"

def test_origKey_None():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, original_key=None)
    assert song.original_key is None

def test_origKey_Empty():
    with pytest.raises(ValueError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, original_key="")

def test_origKey_string3():
    with pytest.raises(ValueError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, original_key="B#m")
    
def test_origKey_INT():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, original_key=1)

def test_tranpose_Fis():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, transpose_to="F#")
    assert song.transpose_to == "F#"

def test_transpose_None():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, transpose_to=None)
    assert song.transpose_to is None

def test_transpose_Empty():
    with pytest.raises(ValueError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, transpose_to="")

def test_transpose_string3():
    with pytest.raises(ValueError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, transpose_to="B#m")
    
def test_transpose_INT():
    with pytest.raises(TypeError):
        song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, transpose_to=1)

def test_created_at_isDatetime():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976)
    assert isinstance(song.created_at, datetime.datetime)
    assert song.created_at.year >= 2026

def test_updated_at_isNone():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976)
    assert song.updated_at is None

def test_notes():
    song = Song(1, "ABC", "Michael Jackson", 210, False, 1976, notes="Check ending")
    assert song.notes == "Check ending"