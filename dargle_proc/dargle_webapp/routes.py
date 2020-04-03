from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as fg

from flask import render_template, url_for, request, json, send_file
from flask_paginate import Pagination, get_page_args
from dargle_webapp import app, db
# from dargle_webapp.models import Domain, Timestamp
from dargle_webapp.workflow.dargle_orm import Base, Domain, Timestamp, Source
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, Query

import sqlite3, json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')

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

@app.route('/analysis')
def analysis():
    fig, ax = plt.subplots()

    dframeD = pd.read_sql_query("select * from domains order by hits desc limit 10",
                engine)
    titleD = dframeD['title']
    domainD = dframeD['domain']
    hitsD = dframeD['hits']

    plt.barh(domainD,hitsD,align='center',color='orange')
    plt.xlabel('Hits')
    plt.ylabel('Domain')
    plt.title('Number of Hits / Top 10 .onion Domains')
    plt.tight_layout(w_pad=1)

    canvasD = fg(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)

    return send_file(img, mimetype='image/png')
