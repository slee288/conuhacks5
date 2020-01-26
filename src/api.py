from flask import Flask, make_response, request, render_template, redirect
from player import Player
from flask_mysqldb import MySQL
from distance_calculator import get_distance

# ./bin/run-player bash
#  logout

prev_location = ""

app = Flask(__name__)
player = Player()

# Database Settings
app.config["MYSQL_USER"] = "sql9320433"
app.config["MYSQL_PASSWORD"] = "uZLKVCVwzC"
app.config["MYSQL_HOST"] = "sql9.freemysqlhosting.net"
app.config["MYSQL_DB"] = "sql9320433"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)
count = 0

@app.route("/", methods=['GET'])
def home():
    global count
    if count < 1:
        db_init()
        count += 1
    # if player.
    return render_template("index.html")

def db_init():
    try:
        cur = mysql.connection.cursor()

        location = '''
                CREATE TABLE IF NOT EXISTS locations (
                    id INT(6) UNSIGNED PRIMARY KEY,
                    name VARCHAR(20) NOT NULL,
                    latitude FLOAT NOT NULL,
                    longitude FLOAT NOT NULL,
                    radius FLOAT NOT NULL,
                    mainIcon VARCHAR(100),
                    bgp VARCHAR(100),
                    bgm VARCHAR(100) NOT NULL
                );
            '''

        song = '''
                CREATE TABLE IF NOT EXISTS songs (
                    id INT(6) UNSIGNED PRIMARY KEY,
                    bgm VARCHAR(100) NOT NULL,
                    timeZone ENUM("morning", "night")
                );
            '''


        insert_song = '''
                    insert into songs (id, bgm, timeZone) values (0, "Homage_To_The_Athletes_Opening_Ceremony_Soundtrack.wav", "morning"),
                    (1, "Farewell_Song_Olympic.wav", "night")
                    '''

        demo_location = '''
                INSERT INTO locations (id, name, latitude, longitude, radius, bgm) values
                    (1, "Concordia", 45.495, -73.579, 2, "Farewell_Song_Olympic.wav");
            '''

        cur.execute(location)
        cur.execute(song)
        cur.execute(insert_song)
        cur.execute(demo_location)
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        app.logger.error(e)

@app.route("/<id>", methods=["GET"])
def mont(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM locations WHERE id={}".format(id))
    curr_loc = cur.fetchone()

    cur.execute("SELECT * FROM songs INNER JOIN locations ON songs.bgm=locations.bgm")
    songToPlay = cur.fetchone()
    # print(songToPlay)

    player.play(songToPlay['bgm'])
    # return render_template("mont-royal.html")
    return redirect("/")

# @app.route("/<id>", methods=["GET"])
# def play_init():
#     '''
#
#     '''

@app.route('/play', methods=['POST'])
def play():
    if 'name' in request.args:
        if player.play(request.args['name']):
            return make_response('playing', 200)
        else:
            return make_response('failed to play {}'.format(request.args['name']), 400)
    elif 'url' in request.args:
        file_name = player.download(request.args['url'])
        player.play(file_name)

        return make_response('playing', 200)
    else:
        return make_response('you need to pass either name or url', 400)


@app.route('/stop', methods=['POST'])
def stop():
    player.stop()

    return make_response('Stopped playing', 200)


@app.route('/pause', methods=['POST'])
def pause():
    player.pause()
    print("paused")
    return make_response('Paused', 200)


@app.route('/unpause', methods=['POST'])
def unpause():
    player.unpause()
    print("playing")
    return make_response('Unpaused', 200)


@app.route('/status', methods=['GET'])
def status():
    if player.status():
        return make_response('Playing', 200)
    else:
        return make_response('Idle', 200)


@app.route('/download', methods=['POST'])
def download():
    if 'url' not in request.args:
        return make_response('Missing url argument', 400)
    else:
        player.download(request.args['url'])

        return make_response('Downloaded file', request.args['url'])


# Receives Geo_Location
@app.route("/loc", methods=["POST"])
def loca():
    # data = request.json

    # SQL cmd extract all location
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM locations INNER JOIN songs ON locations.bgm=songs.bgm")

    locs = cur.fetchall()

    lat = 45.495
    longi = -73.579
    hour = 23
    global prev_location

    is_daytime = (hour >= 7) and (hour <= 18)
    if is_daytime:
        timeZone = "morning"
    else:
        timeZone = "night"

    for l in locs:
        print("Strings are {0} and {1}".format(prev_location, str(l['id'])))
        result = get_distance(lat, longi, l['latitude'], l['longitude'])
        print(timeZone, l['timeZone'])
        if result < l['radius'] and (timeZone==str(l['timeZone'])):
            print(prev_location != str(l["id"]))
            if str(l["id"]) != prev_location:
                # print("Why")
                prev_location = str(l["id"])
                return redirect("/" + str(l["id"]))

    return redirect("/")
    # result = get_distance(lat, longi, )
    # hehehehehehe
    #
