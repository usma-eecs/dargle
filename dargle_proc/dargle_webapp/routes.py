from flask import render_template, url_for, request, json
from flask_paginate import Pagination, get_page_args
from dargle_webapp import app, db
from dargle_webapp.workflow.dargle_orm import Domain, Timestamp, Source
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, Query

import sqlite3, json
import pandas as pd

path = 'dargle_webapp/workflow/dargle.sqlite'
engine = create_engine(f"sqlite:///{path}")

def get_rows(table, offset, per_page):
    return table[offset: offset + per_page]

def query(table):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if table == 'domain':
        cur.execute('SELECT * FROM domains ORDER BY hits DESC')
    elif table == 'timestamps':
        cur.execute('SELECT * FROM timestamps')
    elif table == 'sources':
        cur.execute('SELECT * from sources ORDER BY hits DESC')
    else:
        return
    return cur.fetchall()

def paginated_query(table, limit, offset):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if table == 'domain':
        cur.execute(f'SELECT DISTINCT * FROM domains ORDER BY hits DESC LIMIT {limit} OFFSET {offset}')
    elif table == 'timestamps':
        cur.execute(f'SELECT * FROM timestamps LIMIT {limit} OFFSET {offset}')
    elif table == 'sources':
        cur.execute(f'SELECT * from sources ORDER BY hits DESC LIMIT {limit} OFFSET {offset}')
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
    page, per_page, offset = get_page_args()
    all_domains = query("domain")
    total = len(all_domains)
    rendered_domains = paginated_query('domain', 25, offset)
    pagination = Pagination(page=page, total=total,
                            offset=offset, css_framework='bootstrap4')
    return render_template('domains.html', title='Domains', rows=rendered_domains,
                             page=page, pagination=pagination, total=total)

@app.route("/timestamps")
def timestamps():
    page, per_page, offset = get_page_args()
    all_timestamps = query("timestamps")
    total = len(all_timestamps)
    rendered_timestamps = paginated_query('timestamps', 25, offset)
    pagination = Pagination(page=page, total=total,
                            offset=offset, css_framework='bootstrap4')
    return render_template('timestamps.html', title='Timestamps', rows=rendered_timestamps,
                            page=page, pagination=pagination, total=total)

@app.route("/domain_sources")
def domain_sources():
    page, per_page, offset = get_page_args()
    all_sources = query("sources")
    total = len(all_sources)
    rendered_sources = paginated_query('sources', 25, offset)
    pagination = Pagination(page=page, total=total,
                            offset=offset, css_framework='bootstrap4')
    return render_template('domain_sources.html', title='Sources', rows=rendered_sources,
                            page=page, pagination=pagination, total=total)

@app.route('/search', methods=['GET','POST'])
def search():
    dbsession = sessionmaker(bind=engine)
    session = dbsession()
    if request.method == "POST":
        item = request.form['domain']
        if not item or item == 'all':
            query = session.query(Domain).filter(
                Domain.title.notlike('N/A')).order_by(
                desc(Domain.hits)).all()
            session.commit()
        else:
            query = session.query(Domain).filter(
                Domain.title.notlike('N/A')).filter(
                Domain.title.like(f'%{item}%')).order_by(
                desc(Domain.hits)).all()
            session.commit()

        return render_template('search.html', data=query)
    return render_template('search.html')

# https://www.tutorialspoint.com/flask/flask_sqlite.htm
