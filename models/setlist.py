class Setlist: #bestaat uit ID, Naam, de songs id's.
    def __init__(self, id, name, song_ids=None):
        if type(id) is not int:
            raise TypeError("Setlist ID must be an integer.")

        if id <= 0:
            raise ValueError("Setlist ID must be greater than zero.")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Setlist name cannot be empty.")

        if song_ids is None:
            song_ids = []

        self.id = id
        self.name = name.strip()
        self.song_ids = list(song_ids)