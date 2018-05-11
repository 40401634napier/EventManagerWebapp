# Created by Bart Simons, 2018

# Import deps
import sqlite3, signal
from flask import Flask, Response, request, render_template

# Import data model classes
from .artist import Artist
from .band import Band
from .podium import Podium
from .performance import Performance

# Create a sqlite3 file-based database connection, create the file if it does not exist yet. And create a cursor after that.
conn = sqlite3.connect('data.db', check_same_thread=False)
cur = conn.cursor()

# Define the SIGINT handler (so we can close the DB safely on interruption)
def handler_sigint(sig, frame):
    print('Exiting..')
    conn.close()
    exit()

signal.signal(signal.SIGINT, handler_sigint)

# Create tables in the database if they do not yet exist.
conn.execute("CREATE TABLE IF NOT EXISTS bands (bandId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, bandName TEXT NOT NULL, bandDescription TEXT NOT NULL);")
conn.execute("CREATE TABLE IF NOT EXISTS artists (artistId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, artistName TEXT NOT NULL, artistDescription TEXT NOT NULL, bandId INTEGER, FOREIGN KEY(bandId) REFERENCES bands(bandId));")
conn.execute("CREATE TABLE IF NOT EXISTS podia (podiumId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, podiumDescription TEXT NOT NULL);")
conn.execute("CREATE TABLE IF NOT EXISTS performances (performanceId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, performanceStart TEXT NOT NULL, performanceEnd TEXT NOT NULL, podiumId INTEGER NOT NULL, bandId INTEGER, artistId INTEGER, FOREIGN KEY(podiumId) REFERENCES podia(podiumId), FOREIGN KEY(bandId) REFERENCES bands(bandId), FOREIGN KEY(artistId) REFERENCES artists(artistId));")

conn.commit()

# Instantiate our app
app = Flask(__name__)

# @app.route('/api')
# def api_home():
#     return render_template('main.html', title="It works!")

@app.route('/')
def home():
    return render_template('index.html', isHome=True)

@app.route('/artists')
def artists():
    if (request.args.get('success')):
        return render_template('artists.html', isArtist=True, isSuccess=True, artists=Artist(cur).getAllArtists(False, True))
    else:
        return render_template('artists.html', isArtist=True, artists=Artist(cur).getAllArtists(False, True))

@app.route('/artists/<int:artistId>')
def artist_modify(artistId):
    return render_template('modifyartist.html', isArtist=True, artistId=artistId, bands=Band(cur).getAllBands())

@app.route('/artists/add')
def artists_add():
    return render_template('addartist.html', isArtist=True, bands=Band(cur).getAllBands())

@app.route('/artists/delete')
def artists_delete():
    return render_template('deleteartist.html', isArtist=True, artists=Artist(cur).getAllArtists())

@app.route("/bands")
def bands():
    if (request.args.get('success')):
        return render_template('bands.html', isBand=True, isSuccess=True, bands=Band(cur).getAllBands(False, True))
    else:
        return render_template('bands.html', isBand=True, bands=Band(cur).getAllBands(False, True))

@app.route('/bands/<int:bandId>')
def bands_modify(bandId):
    return render_template('modifyband.html', isBand=True, bandId=bandId)

@app.route("/bands/add")
def bands_add():
    return render_template('addband.html', isBand=True)

@app.route("/bands/delete")
def bands_delete():
    return render_template('deleteband.html', isBand=True, bands=Band(cur).getAllBands())

@app.route("/podia")
def podia():
    if (request.args.get('success')):
        return render_template('podia.html', isPodium=True, isSuccess=True, podia=Podium(cur).getAllPodia())
    else:
        return render_template('podia.html', isPodium=True, podia=Podium(cur).getAllPodia())

@app.route('/podia/<int:podiumId>')
def podia_modify(podiumId):
    return render_template('modifypodium.html', isPodium=True, podiumId=podiumId)

@app.route("/podia/add")
def podia_add():
    return render_template('addpodium.html', isPodium=True)

@app.route("/podia/delete")
def podia_delete():
    return render_template('deletepodium.html', isPodium=True, podia=Podium(cur).getAllPodia())

@app.route('/performances')
def performances():
    if (request.args.get('success')):
        return render_template('performances.html', isPerformance=True, isSuccess=True, performances=Performance(cur).getAllPerformances(False, True))
    else:
        return render_template('performances.html', isPerformance=True, performances=Performance(cur).getAllPerformances(False, True))

@app.route('/performances/<int:performanceId>')
def performances_modify(performanceId):
    return render_template('modifyperformance.html', isPerformance=True, podia=Podium(cur).getAllPodia(), artists=Artist(cur).getAllArtists(), bands=Band(cur).getAllBands(), performanceId=performanceId)

@app.route('/performances/add')
def performances_add():
    return render_template('addperformance.html', isPerformance=True, podia=Podium(cur).getAllPodia(), artists=Artist(cur).getAllArtists(), bands=Band(cur).getAllBands())

@app.route('/performances/delete')
def performances_delete():
    return render_template('deleteperformance.html', isPerformance=True, performances=Performance(cur).getAllPerformances(False, True))

@app.route('/api/band', methods=['GET','POST','PATCH','DELETE'])
def api_band():
    if request.method == 'GET':
        bandId = request.args.get('bandId')
        if (bandId):
            return Response(Band(cur).getBand(bandId, True), mimetype='application/json')
        else:
            return Response(Band(cur).getAllBands(True), mimetype='application/json')
    elif request.method == 'POST':
        if 'bandName' in request.form and 'bandDescription' in request.form:
            rowId = Band(cur).createBand(request.form['bandName'], request.form['bandDescription'])
            conn.commit()
            return rowId
        else:
            return 'Please make sure to provide both bandName and bandDescription!'
    elif request.method == 'PATCH':
        if 'bandId' in request.form and 'bandName' in request.form and 'bandDescription' in request.form:
            row = Band(cur).updateBand(request.form['bandId'], request.form['bandName'], request.form['bandDescription'], True)
            conn.commit()
            return row
        else:
            return 'Please make sure to provide bandId, bandName and bandDescription!'
    elif request.method == 'DELETE':
        if 'bandId' in request.form:
            row = Band(cur).removeBand(request.form['bandId'], True)
            conn.commit()
            return row
        else:
            return 'Please make sure to provide bandId!'

@app.route('/api/artist', methods=['GET','POST','PATCH','DELETE'])
def api_artist():
    if request.method == 'GET':
        artistId = request.args.get('artistId')
        if (artistId):
            return Response(Artist(cur).getArtist(artistId, True), mimetype='application/json')
        else:
            return Response(Artist(cur).getAllArtists(True), mimetype='application/json')
    elif request.method == 'POST':
        if 'artistName' in request.form and 'artistDescription' in request.form:
            if 'bandId' in request.form:
                rowId = Artist(cur).createArtist(request.form['artistName'], request.form['artistDescription'], request.form['bandId'])
            else:
                rowId = Artist(cur).createArtist(request.form['artistName'], request.form['artistDescription'], None)
            conn.commit()
            return rowId
        else:
            return 'Please make sure to provide both artistName and artistDescription!'
    elif request.method == 'PATCH':
        if 'artistId' in request.form and 'artistName' in request.form and 'artistDescription' in request.form:
            if 'bandId' in request.form:
                row = Artist(cur).updateArtist(request.form['artistId'], request.form['artistName'], request.form['artistDescription'], request.form['bandId'], True)
            else:
                row = Artist(cur).updateArtist(request.form['artistId'], request.form['artistName'], request.form['artistDescription'], None, True)
            conn.commit()
            return Response(row, mimetype='application/json')
        else:
            return 'Please make sure to provide artistId, artistName and artistDescription'
    elif request.method == 'DELETE':
        if 'artistId' in request.form:
            row = Artist(cur).removeArtist(request.form['artistId'], True)
            conn.commit()
            return Response(row, mimetype='application/json')
        else:
            return 'Please make sure to provide artistId!'

@app.route('/api/performance', methods=['GET','POST','PATCH','DELETE'])
def api_performance():
    if request.method == 'GET':
        performanceId = request.args.get('performanceId')
        if (performanceId):
            return Response(Performance(cur).getPerformance(performanceId, True), mimetype='application/json')
        else:
            return Response(Performance(cur).getAllPerformances(True), mimetype='application/json')
    elif request.method == 'POST':
        if 'performanceStart' in request.form and 'performanceEnd' in request.form and 'podiumId' in request.form and ('bandId' in request.form or 'artistId' in request.form):
            if ('bandId' in request.form):
                rowId = Performance(cur).createPerformance(request.form['performanceStart'], request.form['performanceEnd'], request.form['podiumId'], request.form['bandId'], None)
            elif ('artistId' in request.form):
                rowId = Performance(cur).createPerformance(request.form['performanceStart'], request.form['performanceEnd'], request.form['podiumId'], None, request.form['artistId'])
            conn.commit()
            return rowId
        else:
            return 'Please make sure to provide performanceStart, performanceEnd, podiumId and bandId/artistId.'
    elif request.method == 'PATCH':
        if 'performanceId' in request.form and 'performanceStart' in request.form and 'performanceEnd' in request.form and 'podiumId' in request.form and ('bandId' in request.form or 'artistId' in request.form):
            if ('bandId' in request.form):
                row = Performance(cur).updatePerformance(request.form['performanceId'], request.form['performanceStart'], request.form['performanceEnd'], request.form['podiumId'], request.form['bandId'], None, True)
            elif ('artistId' in request.form):
                row = Performance(cur).updatePerformance(request.form['performanceId'], request.form['performanceStart'], request.form['performanceEnd'], request.form['podiumId'], None, request.form['artistId'], True)
            conn.commit()
            return Response(row, mimetype='application/json')
        else:
            return 'Please make sure to provide performanceId, performanceStart, performanceEnd, podiumId and bandId/artistId.'
    elif request.method == 'DELETE':
        if 'performanceId' in request.form:
            row = Performance(cur).removePerformance(request.form['performanceId'], True)
            conn.commit()
            return Response(row, mimetype='application/json')
        else:
            return 'Please make sure to provide performanceId!'

@app.route('/api/podium', methods=['GET','POST','PATCH','DELETE'])
def api_podium():
    if request.method == 'GET':
        podiumId = request.args.get('podiumId')
        if (podiumId):
            return Response(Podium(cur).getPodium(podiumId, True), mimetype='application/json')
        else:
            return Response(Podium(cur).getAllPodia(True), mimetype='application/json')
    elif request.method == 'POST':
        if 'podiumDescription' in request.form:
            cur.execute("INSERT INTO podia (podiumDescription) VALUES (?)", (request.form['podiumDescription'],))
            conn.commit()
            return str(cur.lastrowid)
        else:
            return 'Please make sure to provide podiumDescription!'
    elif request.method == 'PATCH':
        if 'podiumId' in request.form and 'podiumDescription' in request.form:
            row = Podium(cur).updatePodium(request.form['podiumId'], request.form['podiumDescription'], True)
            conn.commit()
            return Response(row, mimetype='application/json')
        else:
            return 'Please make sure to provide podiumId and podiumDescription!'
    elif request.method == 'DELETE':
        if 'podiumId' in request.form:
            row = Podium(cur).removePodium(request.form['podiumId'], True)
            conn.commit()
            return Response(row, mimetype='application/json')
        else:
            return 'Please make sure to provide podiumId'