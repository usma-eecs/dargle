from flask import render_template, url_for, request
from dargle_webapp import app, db
from dargle_webapp.models import Domain, Timestamp
import sqlite3

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/tables")
def tables():
    con = sqlite3.connect('dargle.sqlite')
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute('SELECT * FROM domains')

    rows = cur.fetchall();

    cur.execute('SELECT * FROM timestamps')
    rows2 = cur.fetchall();

    return render_template('tables.html',title='Tables',rows=rows,rows2=rows2)

# https://www.tutorialspoint.com/flask/flask_sqlite.htm
