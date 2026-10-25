from models.setlist import Setlist

class SetlistService:
    def __init__(self, repository,  song_repository):
        self.repository = repository
        self.song_repository = song_repository

    def create_setlist(self, name):
        next_id = self.repository.get_next_setlist_id()

        setlist = Setlist(
            id=next_id,
            name=name
        )
        self.repository.save_setlist(setlist)

        return setlist

    def get_setlists(self):
        return self.repository.load_setlists()

    def add_song_to_setlist(self, setlist_id, song_id):
        setlist =self.get_setlist_by_id(setlist_id)

        songs = self.song_repository.load_songs()
        song_exists = any(song.id == song_id for song in songs)

        if not song_exists:
            raise ValueError(f"Song ID not found: {song_id}")

        setlist.song_ids.append(song_id)
        self.repository.save_setlist(setlist)

    def remove_song_from_setlist(self, setlist_id, song_id, position=None):
        setlists = self.repository.load_setlists()

        for setlist in setlists:
            if setlist.id == setlist_id:
                if position is not None:
                    index= position-1

                    if(
                        index <0
                        or index >= len(setlist.song_ids)
                        or setlist.song_ids[index] != song_id
                    ):
                        raise ValueError("Invalid song occurence position.")

                    setlist.song_ids.pop(index)
                else: 
                    setlist.song_ids.remove(song_id)

                self.repository.save_setlist(setlist)
                return

        raise ValueError("Setlist ID not found.")

    def get_setlist_by_id(self, setlist_id):
        setlists = self.repository.load_setlists()

        for setlist in setlists:
            if setlist.id == setlist_id:
                return setlist
        
        raise ValueError("Setlist ID not found")

    def get_songs_for_setlist(self, setlist_id):
        setlist = self.get_setlist_by_id(setlist_id)
        songs = self.song_repository.load_songs()
        songs_by_id = {song.id: song for song in songs}

        resolved_songs=[]

        for song_id in setlist.song_ids:
            if song_id not in songs_by_id:
                raise ValueError(f"Song ID not found: {song_id}")

            resolved_songs.append(songs_by_id[song_id])

        return resolved_songs

    def reorder_song_in_setlist(self, setlist_id, from_position, to_position):
        setlist = self.get_setlist_by_id(setlist_id)

        if not 1 <= from_position <= len(setlist.song_ids):
            raise ValueError("Invalid source position")
        if not 1 <= to_position <= len(setlist.song_ids):
            raise ValueError("Invalid destination position")

        song_id=setlist.song_ids.pop(from_position - 1)
        setlist.song_ids.insert(to_position -1, song_id)

        self.repository.save_setlist(setlist)

    def delete_setlist(self, setlist_id):
        self.repository.delete_setlist(setlist_id)

    def find_setlists_containing_song(self, song_id):
        setlists = self.repository.load_setlists()

        return [
            setlist
            for setlist in setlists
            if song_id in setlist.song_ids
        ]

