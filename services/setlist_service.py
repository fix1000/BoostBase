from models.setlist import Setlist

class SetlistService:
    def __init__(self, repository):
        self.repository = repository

    def create_setlist(self, name):
        next_id = self.repository.get_next_setlist_id()

        setlist = Setlist(
            id=next_id,
            name=name
        )
        self.repository.save_setlist(setlist)

        return setlist