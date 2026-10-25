from models.song import Song
import datetime
import inspect

class SongService:

    def __init__(self, repository, setlist_service=None): 
        self.repository=repository
        self.setlist_service = setlist_service
        self._songs = self.repository.load_songs()
        if self._songs:
            self._next_id=max(song.id for song in self._songs) +1
        else:
            self._next_id=1
    
    def add_song(self, title, artist, duration_seconds, medley, release_year, **criteria):
        for s in self._songs:
            if s.title.upper() == title.upper():
                raise ValueError(f"Title already registered in ID {s.id}")

        song = Song(
            self._next_id,
            title, 
            artist, 
            duration_seconds, 
            medley, 
            release_year,
            **criteria
        )

        self._next_id +=1 
        self._songs.append(song) #opslaan in werkgeheugen
        self.repository.save_song(song) #opslaan naar json of... 
        return song

    def get_song(self, id):
        for s in self._songs:
            if id == s.id:
                return s
        raise ValueError(f"Song with ID {id} not found")

    def get_all_songs(self):
        return self._songs

    def delete_song(self, id, confirmed=False):
        song = next((s for s in self._songs if s.id == id), None)

        if song is None:
            raise ValueError(f"Song with ID {id} not found")

        affected_setlists = []
        if self.setlist_service is not None:
            affected_setlists = (
                self.setlist_service.find_setlists_containing_song(id)
            )

        if affected_setlists and not confirmed:
            setlist_names = ", ".join(
                setlist.name for setlist in affected_setlists
            )
            raise ValueError(
                f"Song is still used in these setlists: {setlist_names}. "
                "Confirmation is required."
            )

        original_song_ids = {
            setlist.id: list(setlist.song_ids)
            for setlist in affected_setlists
        }

        try:
            for setlist in affected_setlists:
                setlist.song_ids = [
                    song_id
                    for song_id in setlist.song_ids
                    if song_id != id
                ]
                self.setlist_service.repository.save_setlist(setlist)

            self.repository.delete_song(song)

        except Exception:
            for setlist in affected_setlists:
                setlist.song_ids = original_song_ids[setlist.id]

            for setlist in affected_setlists:
                self.setlist_service.repository.save_setlist(setlist)

            raise

        self._songs.remove(song)


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
                self.repository.update_song(s) #doorvoeren naar de Repo!
                return
        raise ValueError(f"Song with ID {id} not found")

    def search_songs(self, **criteria):
        # Ignore criteria that were explicitly set to None.
        criteria = {
            field: value
            for field, value in criteria.items()
            if value is not None
        }

        # Validate the remaining criteria.
        for field, value in criteria.items():
            if isinstance(value, str) and value.strip() == "":
                raise ValueError("Voer een zoekterm in")

            if isinstance(value, list) and len(value) == 0:
                raise ValueError("Voer een zoekterm in")

        # Extract special search criteria.
        tags_any = criteria.pop("tags_any", None)
        tags_all = criteria.pop("tags_all", None)
        party_score_min = criteria.pop("party_score_min", None)
        playable_key = criteria.pop("playable_key", None)

        # At least one useful search criterion is required.
        if not criteria and all(
            value is None
            for value in [tags_any, tags_all, party_score_min, playable_key]
        ):
            raise ValueError("Voer een zoekterm in")

        # Validate field names against the Song model.
        valid_fields = set(inspect.signature(Song.__init__).parameters)
        valid_fields.discard("self")

        for field in criteria:
            if field not in valid_fields:
                raise ValueError(f"Onbekend zoekcriterium: {field}")

        resultsearch = []

        for song in self._songs:
            matches = True

            # Match songs containing at least one of the requested tags.
            if tags_any is not None:
                any_found = False

                for tag in tags_any:
                    if tag.upper() in [t.upper() for t in song.tags]:
                        any_found = True
                        break

                if not any_found:
                    continue

            # Match songs containing all requested tags.
            if tags_all is not None:
                all_found = True

                for tag in tags_all:
                    if tag.upper() not in [t.upper() for t in song.tags]:
                        all_found = False
                        break

                if not all_found:
                    continue

            # Match songs with at least the requested party score.
            if party_score_min is not None:
                if (
                    song.party_score is None
                    or song.party_score < party_score_min
                ):
                    continue

            # Match the key in which the song can be performed.
            if playable_key is not None:
                effective_key = song.transpose_to

                if effective_key is None:
                    effective_key = song.original_key

                if (
                    effective_key is None
                    or effective_key.upper() != playable_key.upper()
                ):
                    continue

            # Match all remaining criteria.
            for field, value in criteria.items():
                song_value = getattr(song, field)

                if song_value is None:
                    matches = False
                    break

                elif isinstance(song_value, list):
                    found = False

                    for item in song_value:
                        if field == "medley_titles":
                            if value.upper() in item.upper():
                                found = True
                                break
                        else:
                            if value.upper() == item.upper():
                                found = True
                                break

                    if not found:
                        matches = False
                        break

                elif isinstance(value, str):
                    if value.upper() not in song_value.upper():
                        matches = False
                        break

                else:
                    if value != song_value:
                        matches = False
                        break

            if matches:
                resultsearch.append(song)

        return resultsearch
