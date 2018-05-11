import json

class Podium:
    def __init__(self, cursor):
        self.cursor = cursor

    # Gets all podia
    def getAllPodia(self, asJSON = False):
        if asJSON:
            podia = []
            for podium in self.cursor.execute("SELECT * FROM podia").fetchall():
                podia.append({'podiumId': podium[0], 'podiumDescription': podium[1]})
            return json.dumps(podia)
        else:
            return self.cursor.execute("SELECT * FROM podia").fetchall()

    # Creates a podium
    def createPodium(self, podiumDescription):
        self.cursor.execute("INSERT INTO podia (podiumDescription) VALUES (?)", (podiumDescription,))
        return str(self.cursor.lastrowid)

    # Gets a specific podium
    def getPodium(self, podiumId, asJSON = False):
        if asJSON:
            podia = []
            for podium in self.cursor.execute("SELECT * FROM podia WHERE podiumId = ?", (podiumId,)).fetchall():
                podia.append({'podiumId': podium[0], 'podiumDescription': podium[1]})
            return json.dumps(podia)
        else:
            return self.cursor.execute("SELECT * FROM podia WHERE podiumId = ?", (podiumId,)).fetchall()

    # Updates (modifies) a podium
    def updatePodium(self, podiumId, podiumDescription, asJSON = False):
        self.cursor.execute("UPDATE podia SET podiumDescription = ? WHERE podiumId = ?", (podiumDescription, podiumId))
        if asJSON:
            return json.dumps({'podiumId': podiumId, 'podiumDescription': podiumDescription})

    # Deletes a podium
    def removePodium(self, podiumId, asJSON = False):
        if asJSON:
            row = self.cursor.execute("SELECT * FROM podia WHERE podiumId = ?", (podiumId,)).fetchone()
            self.cursor.execute("DELETE FROM podia WHERE podiumId = ?", (podiumId,))
            return json.dumps({'podiumId': podiumId, 'podiumDescription': row[1]})
        else:
            self.cursor.execute("DELETE FROM podia WHERE podiumId = ?", (podiumId,))
        