from flask import Flask,g
import sqlite3
import os

app = Flask(__name__)


DATABASE = 'C:\\Users\\reshef\\Desktop\\database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def query_voter(voter):
    voter = query_db('select * from voters where voter_identification = ?',
                [voter], one=True)
    return str(voter is not None)

@app.route("/voters/<voter>")
def check_voter(voter):
    try:
        return query_voter(voter)
    except e:
        return e

@app.route("/")
def hello():
    return "The Voter Identification Service is up!"
