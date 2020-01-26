from flask import Flask, make_response, request, render_template
from player import Player
from flask_mysqldb import MySQL

# ./bin/run-player bash
#  logout

app = Flask(__name__)
player = Player()

# Database Settings
app.config["MYSQL_USER"] = "sql9320433"
app.config["MYSQL_PASSWORD"] = "uZLKVCVwzC"
app.config["MYSQL_HOST"] = "sql9.freemysqlhosting.net"
app.config["MYSQL_DB"] = "sql9320433"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

@app.route("/", methods=['GET'])
def home():
    db_init()
    return render_template("index.html")

def db_init():
    try:
        cur = mysql.connection.cursor()

        location = '''
                CREATE TABLE IF NOT EXISTS locations (
                    id INT(6) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(20) NOT NULL,
                    latitude FLOAT NOT NULL,
                    longitude FLOAT NOT NULL,
                    radius FLOAT NOT NULL,
                    songName VARCHAR(20) NOT NULL,
                    mainIcon VARCHAR(100) NOT NULL,
                    bgp VARCHAR(100) NOT NULL,
                    bgm VARCHAR(100) NOT NULL
                );
            '''

        song = '''
                CREATE TABLE IF NOT EXISTS songs (
                    id INT(6) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(20) NOT NULL,
                    timeZone ENUM("morning", "night")
                );
            '''


            "INSERT INTO songs (name, timeZone) VALUES ({0}, {1})".format("Homage_To_The_Athletes_Opening_Ceremony_Soundtrack.wav", "morning")
            "INSERT INTO songs (name, timeZONE) VALUES ({0}, {1})".format("Farewell_Song_&_Ballet_of_the_Closing_Ceremony.wav", "evening")
        # geo_locations = '''
        #         INSERT INTO locations (name, latitude, longitude, radius, songName) VALUES
        #         ()
        #     '''

        cur.execute(location)
        cur.execute(song)
        # mysql.connection.commit()
        cur.close()
    except Exception as e:
        app.logger.error(e)

@app.route("/mont-royal", methods=["GET"])
def mont():
    return render_template("mont-royal.html")

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
    data = request.json
    return data
