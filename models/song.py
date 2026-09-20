import datetime

class Song:
    def __init__(self, id, title, artist, duration_seconds, medley, release_year, medley_titles=None, party_score=None, difficulty=None, genre=None, tags=None, lead_vocals=None, is_core_repertoire=None, original_key=None, transpose_to=None, notes=None, created_at=None, updated_at=None):
        if type(id) is not int:
            raise TypeError("Id wordt niet opgehoogd met een nummer")
        elif id >0:
            self.id = id
        else:
            raise ValueError("Song ID must be greater than 0")
        
        if title is not None and title.strip() != "":
            if len(title)>300:
                raise ValueError("Beperk tot 300 karakters")
            self.title = title.strip()
        else:
            raise ValueError("Title song cannot be empty")

        if artist is not None and artist.strip() != "":
            if len(artist)>300:
                raise ValueError("Beperk tot 300 karakters")
            self.artist = artist.strip()
        else:
            raise ValueError("Title song cannot be empty")

        if type(duration_seconds) is not int:
            raise TypeError("Duration must be an Integer")
        elif not 10 <= duration_seconds <= 1000:
            raise ValueError("Duration song in seconds! Please stay between 10 and 1000 value.")
        else:
            self.duration_seconds = duration_seconds
    
        if type(medley) is bool:
            self.medley =medley
        else:
            raise TypeError("True or False is the only option for this field.")

        if type(release_year) is not int:
            raise TypeError("Geef een waarde in van tussen 1900 en 2100")
        elif not 1900<= release_year <= 2100:
            raise ValueError("Release year is foutief ingevoerd. Kies een waarde tussen 1900 en 2100.")
        else: 
            self.release_year = release_year

        if party_score is None:
            self.party_score = None
        elif type(party_score) is not int:
            raise TypeError("Geef een waarde in van 1 tot 10")
        elif not 1<= party_score <=10:
            raise ValueError("Geen een waarde in tussen 1 en 10")
        else: 
            self.party_score = party_score

        if self.medley == True:
            if medley_titles is None:
                raise TypeError("Medley lijst mag niet leeg zijn als Medley = Ja")
            elif medley_titles == []:
                raise ValueError("Als meldey is Ja, dan moeten de titels van de nummers worden opgevoerd.")
            elif type(medley_titles) is not list:
                raise TypeError("Medley titles moet een lijst zijn van titels")
            else:
                for title in medley_titles:
                    if type(title) is not str:
                        raise TypeError(f"Titel '{title}' in medley list is geen tekst")
                self.medley_titles = medley_titles
        else:
            if medley_titles is not None and medley_titles != []:
                raise ValueError("Als het geen medley betreft, dan ook geen medley titels toevoegen.")
            else:    
                self.medley_titles = []

        difficulty_levels = ["Very Easy", "Easy", "Medium", "Hard", "Very Hard"]
        if difficulty is None: 
            self.difficulty = None
        elif type(difficulty) is not str:
            raise TypeError("Vul in: Very easy - Easy - Medium - Hard - Very Hard")
        elif difficulty not in difficulty_levels:
            raise ValueError("Vul in: Very easy - Easy - Medium - Hard - Very Hard")
        else:
            self.difficulty = difficulty

        GENRES = [
            "Pop",
            "Rock",
            "Dance",
            "Disco",
            "Funk",
            "Soul",
            "Reggae",
            "Nederlandstalig",
            "Schlager",
            "Country",
            "Blues",
            "Jazz",
            "R&B",
            "Limburgs",
            "Duitse Stimmung",
            "Nieuwe hits (Top 40)", 
            "Hard-Rock"
        ]
        if genre is None:
            self.genre = None
        elif type(genre) is not str:
            raise TypeError("Gebruik een toegestaan genre die het meest past")
        elif genre not in GENRES:
            raise ValueError("Gebruik een genre uit de lijst met genres, die het meest past")
        else: 
            self.genre = genre

        self.tags = []
        if tags is not None: 
            if type(tags) is not list:
                raise TypeError("Gebruik een lijst met tags")
            for t in tags:
                if type(t) is not str:
                    raise TypeError("Elke tag moet tekst zijn")
                self.tags.append(t)

        self.lead_vocals = []
        if lead_vocals is not None:
            if type(lead_vocals) is not list:
                raise TypeError("Gebruik een lijst om lead vocals te registreren")
            for l in lead_vocals:
                if type(l) is not str:
                    raise TypeError("vul een tekst in een lijst in")
                self.lead_vocals.append(l)
        
        if is_core_repertoire is None:
            self.is_core_repertoire = None
        elif type(is_core_repertoire) is not bool:
            raise TypeError("Alleen True of False toegestaan")
        else:
            self.is_core_repertoire = is_core_repertoire

        if original_key is None:
            self.original_key = None
        elif type(original_key) is not str:
            raise TypeError("Vul een geldige muzieknoot in van 1 of 2 karakters, zoals G#")
        elif not 1<= len(original_key) <=2:
            raise ValueError("Vul een geldige muzieknoot in van 1 of 2 karakters")
        else:
            self.original_key = original_key

        if transpose_to is None:
            self.transpose_to = None
        elif type(transpose_to) is not str:
            raise TypeError("Vul een geldige muzieknoot in van 1 of 2 karakters, zoals G#")
        elif not 1<= len(transpose_to) <=2:
            raise ValueError("Vul een geldige muzieknoot in van 1 of 2 karakters")
        else:
            self.transpose_to = transpose_to

        if created_at is None:
            self.created_at = datetime.datetime.now()
        else:
            self.created_at = created_at
        

        self.updated_at = updated_at
        self.notes = notes




    def __str__(self):
        return f"id: {self.id}, Title: {self.title}, Artist: {self.artist}, Score: {self.party_score}"