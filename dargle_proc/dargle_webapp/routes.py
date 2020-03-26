from flask import render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from dargle_webapp import app, db
from dargle_webapp.models import Domain, Timestamp
import sqlite3

path = 'dargle_webapp/workflow/dargle.sqlite'

def get_rows(table, offset=0, per_page=20):
    return table[offset: offset + per_page]

def query(table):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if table == 'domain':
        cur.execute('SELECT * FROM domains')
    elif table == 'timestamps':
        cur.execute('SELECT * FROM timestamps')
    else:
        return
    return cur.fetchall()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/domains")
def domains():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    rows = query("domain")
    total = len(rows)
    pagination_rows = get_rows(rows, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('domains.html', title='Domains', rows=pagination_rows,
                            page=page, per_page=per_page, pagination=pagination)

@app.route("/timestamps")
def timestamps():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    rows = query("timestamps")
    total = len(rows)
    pagination_rows = get_rows(rows, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('timestamps.html', title='Timestamps', rows=pagination_rows,
                            page=page, per_page=per_page, pagination=pagination)

# https://www.tutorialspoint.com/flask/flask_sqlite.htm
