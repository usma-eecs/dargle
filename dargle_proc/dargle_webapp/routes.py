from flask import render_template, url_for, request, json
from flask_paginate import Pagination, get_page_args
from dargle_webapp import app, db
# from dargle_webapp.models import Domain, Timestamp
from dargle_webapp.workflow.dargle_orm import Base, Domain, Timestamp, Source
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

import sqlite3, json
import pandas as pd

path = 'dargle_webapp/workflow/dargle.sqlite'
engine = create_engine(f"sqlite:///{path}")

def get_rows(table, offset=0, per_page=20):
    return table[offset: offset + per_page]

def query(table):
    # con = sqlite3.connect(path)
    # con.row_factory = sqlite3.Row
    # cur = con.cursor()
    engine.connect()
    if table == 'domain':
        # cur.execute('SELECT * FROM domains ORDER BY hits DESC')
        return engine.execute('SELECT * FROM domains ORDER BY hits DESC')
    elif table == 'timestamps':
        # cur.execute('SELECT * FROM timestamps')
        return engine.execute('SELECT * FROM timestamps')
    elif table == 'sources':
        # cur.execute('SELECT * from sources ORDER BY hits DESC')
        return engine.execute('SELECT * from sources ORDER BY hits DESC')
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
    # page, per_page, offset = get_page_args()
    rows = query("domain")
    # total = len(rows)
    # pagination_rows = get_rows(rows, offset=offset, per_page=per_page)
    # pagination = Pagination(page=page, total=total, per_page=per_page,
    #                         css_framework='bootstrap4')
    return render_template('domains.html', title='Domains', rows=rows)#,
                            #page=page, per_page=per_page, pagination=pagination)

@app.route("/timestamps")
def timestamps():
    # page, per_page, offset = get_page_args(page_parameter='page',
                                        #    per_page_parameter='per_page')
    rows = query("timestamps")
    # total = len(rows)
    # pagination_rows = get_rows(rows, offset=offset, per_page=per_page)
    # pagination = Pagination(page=page, per_page=per_page, total=total,
    #                         css_framework='bootstrap4')
    return render_template('timestamps.html', title='Timestamps', rows=rows)#,
                            # page=page, per_page=per_page, pagination=pagination)

@app.route("/domain_sources")
def domain_sources():
    # page, per_page, offset = get_page_args(page_parameter='page',
    #                                        per_page_parameter='per_page')
    # per_page = 25
    rows = query("sources")
    # total = len(rows)
    # pagination_rows = get_rows(rows, offset=offset, per_page=per_page)
    # pagination = Pagination(page=page, per_page=per_page, total=total,
    #                         css_framework='bootstrap4')
    return render_template('domain_sources.html', title='Sources', rows=rows)#,
                            # page=page, per_page=per_page, pagination=pagination)

@app.route('/search', methods=['GET','POST'])
def search():
    dbsession = sessionmaker(bind=engine)
    session = dbsession()
    if request.method == "POST":
        item = request.form['domain']

        query = session.query(Domain).filter(Domain.domain.like(f'%{item}%'),
            Domain.title.like(item)).all()
        session.commit()

        if len(query)==0 and item=='all':
            query = session.query(Domain).filter(Domain.domain.like(f'%{item}%'),
                Domain.title.like(item)).all()
            session.commit()

        return render_template('search.html', data=query)
    return render_template('search.html')

# https://www.tutorialspoint.com/flask/flask_sqlite.htm
