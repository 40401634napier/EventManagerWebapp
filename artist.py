import json

class Artist:
    def __init__(self, cursor):
        self.cursor = cursor

    def getAllArtists(self, asJSON = False, includeBand = False):
        if asJSON:
            artists = []
            if includeBand:
                for artist in self.cursor.execute("SELECT artistId, artistName, artistDescription, artists.bandId, bands.bandName FROM artists LEFT JOIN bands ON bands.bandId = artists.bandId").fetchall():
                    artists.append({'artistId': artist[0], 'artistName': artist[1], 'artistDescription': artist[2], 'bandId': artist[3], 'bandName':artist[4]})
            else:
                for artist in self.cursor.execute("SELECT * FROM artists").fetchall():
                    artists.append({'artistId': artist[0], 'artistName': artist[1], 'artistDescription': artist[2], 'bandId': artist[3]})
            return json.dumps(artists)
        else:
            if includeBand:
                return self.cursor.execute("SELECT artistId, artistName, artistDescription, artists.bandId, bands.bandName FROM artists LEFT JOIN bands ON bands.bandId = artists.bandId").fetchall()
            else:
                return self.cursor.execute("SELECT * FROM artists").fetchall()

    def createArtist(self, artistName, artistDescription, bandId):
        print(bandId)
        self.cursor.execute("INSERT INTO artists (artistName, artistDescription, bandId) VALUES (?, ?, ?)", (artistName, artistDescription, bandId))
        return str(self.cursor.lastrowid)

    def getArtist(self, artistName, asJSON = False):
        if asJSON:
            artists = []
            for artist in self.cursor.execute("SELECT * FROM artists WHERE artistName = ?", (artistName,)).fetchall():
                artists.append({'artistId': artist[0], 'artistName': artist[1], 'artistDescription': artist[2], 'bandId': artist[3]})
            return json.dumps(artists)
        else:
            return self.cursor.execute("SELECT * FROM artists WHERE artistName = ?", (artistName,)).fetchall()

    def updateArtist(self, artistId, artistName, artistDescription, bandId, asJSON = False):
        self.cursor.execute("UPDATE artists SET artistName = ?, artistDescription = ?, bandId = ? WHERE artistId = ?", (artistName, artistDescription, bandId, artistId))
        if asJSON:
            return json.dumps({'artistId': artistId, 'artistName': artistName, 'artistDescription': artistDescription, 'bandId': bandId})

    def removeArtist(self, artistId, asJSON = False):
        if asJSON:
            row = self.cursor.execute("SELECT * FROM artists WHERE artistId = ?", (artistId,)).fetchone()
            self.cursor.execute("DELETE FROM artists WHERE artistId = ?", (artistId,))
            return json.dumps({'artistId': artistId, 'artistName': row[1], 'artistDescription': row[2], 'bandId': row[3]})
        else:
            self.cursor.execute("DELETE FROM artists WHERE artistId = ?", (artistId,))