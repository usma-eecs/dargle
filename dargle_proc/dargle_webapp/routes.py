from flask import render_template, url_for, request
from dargle_webapp import app, db
from dargle_webapp.models import Domain, Timestamp
import sqlite3

path = 'dargle_webapp/workflow/dargle.sqlite'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/tables")
def tables():
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute('SELECT * FROM domains')

    rows = cur.fetchall();

    return render_template('tables.html',title='Tables',rows=rows)

@app.route("/tables2")
def tables2():
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute('SELECT * FROM timestamps')
    
    rows2 = cur.fetchall();

    return render_template('tables2.html',title='Tables2',rows2=rows2)

# https://www.tutorialspoint.com/flask/flask_sqlite.htm
