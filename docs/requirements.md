####### BoostBase Requirements ###################################

## Goal

BoostBase helps bands managing their repertoire (songs)

---

## Version 0.1

- Saving songs persistently
    As a band member, I want to be able to save songs, so eventually we can make setlists of it. 
    Data Specs: in song_model.md
- Displaying songs
    As a band member, I want to see the metadata behind the song, so I can review it, if it does makes sence to put them in a certain setlist.
- Adding songs
    As a band member, I want to add numbers to my saved songs, so we can add more succesfull numbers into the setlist.
- Updating songs
    As a band member, I want to adjust data in case we want to change the data, so the etadata is allways up to date.
- Deleting songs
    As a band member, I want to erase the song and all the (meta)data around that song, so in case of a mistake I can remove false data.
- Archiving songs
    As a band member, I want to archive a song, if it is retired / not played anymore, so when we make a setlist, you also can include older / forgotten songs. 

---

## Version 0.2

- Search artist
    As a band member, I want to search for artists in the data, so I can manually look for numbers to be played or adjusted.
- Search titel
    As a band member, I want to search for titels in the data, so I can manually look for numbers to be played or adjusted.
- Search for tags
    As a band member, I want to search for tags in the data, so I can manually look for numbers to be played or adjusted.
- **Search for tags (ANY)**
    As a band member, I want to search for songs matching any of the specified tags, so I can find songs that match at least one of my selected criteria.
- **Search for tags (ALL)**
    As a band member, I want to search for songs matching all of the specified tags, so I can find songs that meet every selected criterion.
- Search for partyscore:
    As a band member, I want to search for party score in the data, including the minimal party score of a song.
- Search by playable key
    As a band member, I want to search for songs by the key in which we perform them, so I can find songs that fit the key required for a performance.
---

## Version 0.3 — Setlist Management

### 1. Create a setlist
As a band member, I want to create a named setlist, so I can prepare a repertoire for a specific event.

**Acceptance criteria**
- A setlist has a unique ID and a name.
- A setlist can initially contain no songs.
- A setlist is saved persistently.
- Setlist names cannot be empty or consist only of whitespace.
- Setlist IDs are assigned automatically by the application; users do not provide them.
- Every newly created setlist receives a unique ID.
- Setlist IDs are not reused after a setlist is deleted.
- The next available ID is stored persistently and remains correct after restarting the application.

### 2. View a setlist
As a band member, I want to view a setlist and its songs, so I can review the repertoire planned for an event.

**Acceptance criteria**
- A setlist can be retrieved by its ID.
- Songs are resolved using their existing song IDs.
- Songs are displayed in the order stored in the setlist.
- The same song may appear multiple times in one setlist.
- Each occurrence of a song is treated as a separate entry with its own position.
- A missing setlist ID produces a clear error.

### 3. Add songs to a setlist
As a band member, I want to add existing songs to a setlist, so I can prepare the repertoire for an event.

**Acceptance criteria**
- Only songs that exist in the repertoire can be added.
- The setlist stores song IDs rather than duplicate song objects.
- A song can be added multiple times to the same setlist.
- Each addition creates a separate occurrence at the end of the setlist.
- Adding a song preserves the existing order.
- The change is saved persistently.

### 4. Reorder songs in a setlist
As a band member, I want to change the order of songs in a setlist, so I can optimise the flow of a performance.

**Acceptance criteria**
- A specific occurrence of a song can be moved to a different position.
- When the same song appears more than once, the occurrence being moved can be identified unambiguously.
- The requested position must be valid.
- The new order is saved persistently.

### 5. Remove a song from a setlist
As a band member, I want to remove a song from a setlist without deleting it from the repertoire, so I can adapt a setlist without losing the song.

**Acceptance criteria**
- A specific occurrence can be removed from the selected setlist.
- Removing one occurrence does not automatically remove other occurrences of the same song.
- The song remains in the repertoire.
- The updated setlist is saved persistently.

### 6. Delete a setlist
As a band member, I want to delete a complete setlist, so I can remove a setlist that is no longer needed.

**Acceptance criteria**
- The selected setlist is deleted persistently.
- Its deletion does not delete any songs from the repertoire.
- Attempting to delete a non-existent setlist produces a clear error.

### 7. Warn before deleting a song used in setlists
As a band member, I want to receive a warning before permanently deleting a song that is used in one or more setlists, so I can review the consequences before proceeding.

**Acceptance criteria**
- Before permanently deleting a song, the application checks whether the song occurs in any setlists.
- If the song occurs in one or more setlists, the application displays a warning before deletion.
- The warning identifies the song and lists the affected setlists.
- The warning explains that continuing will remove all occurrences of the song from the affected setlists.
- The user can cancel the deletion.
- If the user cancels, the song and all setlists remain unchanged.
- If the user confirms, the song is permanently deleted and all its occurrences are removed from the affected setlists.
- If the song is not used in any setlist, the setlist-specific warning is not required.
- If deletion or cleanup fails, the application must not leave the song repository and setlist repositories in an inconsistent state.
- Archiving a song does not remove it from existing setlists.

---

## Future versions

- AI setlist generator
    As a band member, I want to generate a smart setlist, by prompting a question, so we get machine learned (more effective) stelists for different occasions 
- Spotify Integrations
    As a band member, I want the songs to be linked to a Spotify song, so I can immediately identofy the song and hear how it's played, so in reheasrsels when we are in doubt, we can lookup very quickly.
- Statistics
    As an app developer, I want to see the statistics behind the app, so I can see which parts are most famous, and which are not, and focus on extending and promoting. 
- Mobile app
    As a band member, I want to use my phone during the application, so I do not need to bring my Computer or laptop with me.
- Cloud Synchronisation
    As an app developer, I want top make use of cloud synchronisation (Azure), so there is no need for storage on my own PC.
- Saving songs persistently
    As a band member, I want to be able to save songs in a database, so eventually we can make setlists of it. 

---


