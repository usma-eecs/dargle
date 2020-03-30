from flask import render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from dargle_webapp import app, db
# from dargle_webapp.models import Domain, Timestamp
from dargle_webapp.workflow.dargle_orm import Base, Domain, Timestamp, Source
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3

path = 'dargle_webapp/workflow/dargle.sqlite'
engine = create_engine(f"sqlite:///{path}")
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

def get_rows(table, offset=0, per_page=20):
    return table[offset: offset + per_page]

def query(table):
    # con = sqlite3.connect(path)
    # con.row_factory = sqlite3.Row
    # cur = con.cursor()
    if table == 'domain':
        # cur.execute('SELECT * FROM domains ORDER BY hits DESC')
        return session.query(Domain).all()
    elif table == 'timestamps':
        # cur.execute('SELECT * FROM timestamps')
        return session.query(Timestamp).all()
    elif table == 'sources':
        # cur.execute('SELECT * from sources ORDER BY hits DESC')
        return session.query(Source).all()
    else:
        return
    # return cur.fetchall()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/domains")
def domains():
    page, per_page, offset = get_page_args()
    rows = query("domain")
    total = len(rows)
    pagination_rows = get_rows(rows, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, total=total, per_page=per_page,
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

@app.route("/domain_sources")
def domain_sources():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    per_page = 25
    rows = query("sources")
    total = len(rows)
    pagination_rows = get_rows(rows, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('domain_sources.html', title='Sources', rows=pagination_rows,
                            page=page, per_page=per_page, pagination=pagination)

# https://www.tutorialspoint.com/flask/flask_sqlite.htm
