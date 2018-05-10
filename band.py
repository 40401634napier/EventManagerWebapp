import json

class Band:
    def __init__(self, cursor):
        self.cursor = cursor

    def getAllBands(self, asJSON = False, includeMembers = False):
        if asJSON:
            bands = []
            for band in self.cursor.execute("SELECT * FROM bands").fetchall():
                bands.append({'bandId': band[0], 'bandName': band[1], 'bandDescription': band[2]})
            return json.dumps(bands)
        else:
            if includeMembers:
                resultList = []
                for band in self.cursor.execute("SELECT * FROM bands").fetchall():
                    memberArtists = self.cursor.execute("SELECT artistName FROM artists WHERE bandId = ?", (str(band[0]))).fetchall()
                    resultList.append(band + (', '.join(i[0] for i in memberArtists),))
                return resultList
            else:
                return self.cursor.execute("SELECT * FROM bands").fetchall()

    def createBand(self, bandName, bandDescription):
        self.cursor.execute("INSERT INTO bands (bandName, bandDescription) VALUES (?, ?)", (bandName, bandDescription))
        return str(self.cursor.lastrowid)

    def getBand(self, bandName, asJSON = False):
        if asJSON:
            bands = []
            for band in self.cursor.execute("SELECT * FROM bands WHERE bandName = ?", (bandName,)).fetchall():
                bands.append({'bandId': band[0], 'bandName': band[1], 'bandDescription': band[2]})
            return json.dumps(bands)
        else:
            return self.cursor.execute("SELECT * FROM bands WHERE bandName = ?", (bandName,)).fetchall()
    
    def updateBand(self, bandId, bandName, bandDescription, asJSON = False):
        self.cursor.execute("UPDATE bands SET bandName = ?, bandDescription = ? WHERE bandId = ?", (bandName,bandDescription,bandId))
        if asJSON:
            return json.dumps({'bandId': bandId, 'bandName': bandName, 'bandDescription': bandDescription})

    def removeBand(self, bandId, asJSON = False):
        if asJSON:
            row = self.cursor.execute("SELECT * FROM bands WHERE bandId = ?", (bandId,)).fetchone()
            self.cursor.execute("DELETE FROM bands WHERE bandId = ?", (bandId,))
            return json.dumps({'bandId': bandId, 'bandName': row[1], 'bandDescription': row[2]})
        else:
            self.cursor.execute("DELETE FROM bands WHERE bandId = ?", (bandId,))