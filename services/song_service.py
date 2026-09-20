from models.song import Song
import datetime

class SongService:

    def __init__(self): 
        #stukje info over oplopende ID, die ergens moet beginnen. Dit is tijdelijk code als we een archief hebben wordt de ID daaruit opgeroepen.
        self._next_id=1
        self._songs=[]
    
    def add_song(self, title, artist, duration_seconds, medley, release_year):
        for s in self._songs:
            if s.title.upper() == title.upper():
                raise ValueError(f"Title already registered in ID {s.id}")
        song = Song(
            self._next_id,
            title, 
            artist, 
            duration_seconds, 
            medley, 
            release_year
        )

        self._next_id +=1
        self._songs.append(song)
        return song

    def get_song(self, id):
        for s in self._songs:
            if id == s.id:
                return s
        raise ValueError(f"Song with ID {id} not found")

    def get_all_songs(self):
        return self._songs
        
    def delete_song(self, id):
        for s in self._songs:
            if id == s.id:
                self._songs.remove(s)
                return
        raise ValueError(f"Song with ID {id} not found")

    def update_song(
        self,
        id,
        title=None,
        artist=None,
        duration_seconds=None,
        medley=None,
        release_year=None,
        party_score=None,
        difficulty=None,
        genre=None,
        tags=None,
        lead_vocals=None,
        is_core_repertoire=None,
        original_key=None,
        transpose_to=None,
        notes=None
    ):
        for s in self._songs:
            if id == s.id:
                if title is not None:
                    s.title = title
                if artist is not None:
                    s.artist = artist
                if duration_seconds is not None:
                    s.duration_seconds = duration_seconds
                if medley is not None:
                    s.medley = medley
                if release_year is not None:
                    s.release_year = release_year
                if party_score is not None:
                    s.party_score = party_score
                if difficulty is not None:
                    s.difficulty = difficulty
                if genre is not None:
                    s.genre = genre
                if tags is not None:
                    s.tags = tags
                if lead_vocals is not None:
                    s.lead_vocals = lead_vocals
                if is_core_repertoire is not None:
                    s.is_core_repertoire= is_core_repertoire
                if original_key is not None:
                    s.original_key = original_key
                if transpose_to is not None:
                    s.transpose_to = transpose_to
                if notes is not None:
                    s.notes = notes
                s.updated_at=datetime.datetime.now()
                return
        raise ValueError(f"Song with ID {id} not found")