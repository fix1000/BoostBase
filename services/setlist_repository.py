import json
import os
from models.setlist import Setlist

class SetlistRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def _load_data(self):
        if not os.path.exists(self.file_path):
            return {
                "next_setlist_id": 1,
                "setlists": []
            }

        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    def _save_data(self, data):
        with open(self.file_path, "w", encoding="UTF-8") as file:
            json.dump(data, file, indent=4)

    def save_setlist(self, setlist):
        data=self._load_data()
        setlists = data["setlists"]
        
        setlist_data = {
            "id": setlist.id,
            "name":setlist.name,
            "song_ids": setlist.song_ids
        }

        for index, existing_setlist in enumerate(setlists): #code zodat we niet een zelfde lijst 2 keer gaan opslaan
            if existing_setlist["id"] == setlist.id:
                setlists[index] = setlist_data
                break
        else:
            setlists.append(setlist_data)

        self._save_data(data)
        

    def load_setlists(self):
        data = self._load_data()
        setlists = []

        for item in data["setlists"]:
            setlist = Setlist(
                id=item["id"],
                name=item["name"],
                song_ids=item["song_ids"]
            )
            setlists.append(setlist)

        return setlists

    def delete_setlist(self, setlist_id):
        data = self._load_data()
        setlists = data["setlists"]
        for index, item in enumerate(setlists):
            if item["id"] == setlist_id:
                setlists.pop(index)
                self._save_data(data)
                return
        raise ValueError("Setlist ID not found")

    def get_next_setlist_id(self):
        data= self._load_data()

        next_id = data["next_setlist_id"]
        data["next_setlist_id"] = next_id + 1

        self._save_data(data)

        return next_id

    def delete_setlist(self, setlist_id):
        data = self._load_data()
        for index, item in enumerate(data["setlists"]):
            if item["id"] ==setlist_id:
                data["setlists"].pop(index)
                self._save_data(data)
                return
        raise ValueError("Setlist ID not found.")