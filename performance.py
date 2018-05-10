import json

class Performance:
    def __init__(self, cursor):
        self.cursor = cursor

    def getAllPerformances(self, asJSON = False, includePerformer = False):
        if asJSON:
            performances = []
            for performance in self.cursor.execute("SELECT * FROM performances").fetchall():
                performances.append({'performanceId': performance[0], 'performanceStart': performance[1], 'performanceEnd': performance[2], 'podiumId': performance[3], 'bandId': performance[4], 'artistId': performance[5]})
            return json.dumps(performance)
        else:
            if includePerformer:
                performances = []
                for performance in self.cursor.execute("SELECT performanceId, performanceStart, performanceEnd, performances.podiumId, bandId, artistId, podia.podiumDescription FROM performances INNER JOIN podia ON podia.podiumId = performances.podiumId").fetchall():
                    if performance[4]:
                        band = self.cursor.execute("SELECT bandName FROM bands WHERE bandId = ?", (performance[4],)).fetchone()
                        performances.append((performance[0], performance[1], performance[2], performance[6], band[0]))
                    elif performance[5]:
                        artist = self.cursor.execute("SELECT artistName FROM artists WHERE artistId = ?", (performance[5],)).fetchone()
                        performances.append((performance[0], performance[1], performance[2], performance[6], artist[0]))
                return performances
            else:
                return self.cursor.execute("SELECT * FROM performances").fetchall()

    def createPerformance(self, performanceStart, performanceEnd, podiumId, bandId, artistId):
        self.cursor.execute("INSERT INTO performances (performanceStart, performanceEnd, podiumId, bandId, artistId) VALUES (?, ?, ?, ?, ?)", (performanceStart, performanceEnd, podiumId, bandId, artistId))
        return str(self.cursor.lastrowid)

    def getPerformance(self, performanceId, asJSON = False):
        if asJSON:
            performances = []
            for performance in self.cursor.execute("SELECT * FROM performances WHERE performanceId = ?", (performanceId,)).fetchall():
                performances.append({'performanceId': performance[0], 'performanceStart': performance[1], 'performanceEnd': performance[2], 'podiumId': performance[3], 'bandId': performance[4], 'artistId': performance[5]})
            return json.dumps(performances)
        else:
            return self.cursor.execute("SELECT * FROM performances WHERE performanceId = ?", (performanceId,)).fetchall()

    def updatePerformance(self, performanceId, performanceStart, performanceEnd, podiumId, bandId, artistId, asJSON = False):
        self.cursor.execute("UPDATE performances SET performanceStart = ?, performanceEnd = ?, podiumId = ?, bandId = ?, artistId = ? WHERE performanceId = ?", (performanceStart, performanceEnd, podiumId, bandId, artistId, performanceId))
        if asJSON:
            return json.dumps({'performanceId': performanceId, 'performanceStart': performanceStart, 'performanceEnd': performanceEnd, 'podiumId': podiumId, 'bandId': bandId, 'artistId': artistId})
    
    def removePerformance(self, performanceId, asJSON = False):
        if asJSON:
            performance = self.cursor.execute("SELECT * FROM performances WHERE performanceId = ?", (performanceId,)).fetchone()
            self.cursor.execute("DELETE FROM performances WHERE performanceId = ?", (performanceId,))
            return json.dumps({'performanceId': performanceId, 'performanceStart': performance[1], 'performanceEnd': performance[2], 'podiumId': performance[3], 'bandId': performance[4], 'artistId': performance[5]})
        else:
            self.cursor.execute("DELETE FROM performances WHERE performanceId = ?", (performanceId,))