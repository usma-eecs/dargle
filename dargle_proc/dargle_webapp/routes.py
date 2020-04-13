from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as fg

from flask import render_template, url_for, request, json, send_file
from flask_paginate import Pagination, get_page_args
from dargle_webapp import app, db
from dargle_webapp.workflow.dargle_orm import Domain, Timestamp, Source
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, Query

import sqlite3, json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')

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

def paginated_query(table, limit, offset, item=None):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if table == 'domain':
        cur.execute(f'SELECT DISTINCT * FROM domains ORDER BY hits DESC LIMIT {limit} OFFSET {offset}')
    elif table == 'timestamps':
        cur.execute(f'SELECT * FROM timestamps LIMIT {limit} OFFSET {offset}')
    elif table == 'sources':
        cur.execute(f'SELECT * from sources ORDER BY hits DESC LIMIT {limit} OFFSET {offset}')
    elif table == 'search':
        cur.execute(f"""SELECT DISTINCT * FROM domains NOT LIKE 'N/A'
                    AND LIKE '%{item}%' ORDER BY hits DESC LIMIT {limit} OFFSET {offset}""")
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
    offset = (page - 1) * 25
    total = len(all_domains)
    rendered_domains = paginated_query('domain', 25, offset)
    pagination = Pagination(page=page, total=total, per_page=25,
                            offset=offset, css_framework='bootstrap4')
    return render_template('domains.html', title='Domains', rows=rendered_domains,
                             page=page, pagination=pagination, total=total)

@app.route("/timestamps")
def timestamps():
    page, per_page, offset = get_page_args()
    all_timestamps = query("timestamps")
    offset = (page - 1) * 25
    total = len(all_timestamps)
    rendered_timestamps = paginated_query('timestamps', 25, offset)
    pagination = Pagination(page=page, total=total, per_page=25,
                            offset=offset, css_framework='bootstrap4')
    return render_template('timestamps.html', title='Timestamps', rows=rendered_timestamps,
                            page=page, pagination=pagination, total=total)

@app.route("/domain_sources")
def domain_sources():
    page, per_page, offset = get_page_args()
    all_sources = query("sources")
    offset = (page - 1) * 25
    total = len(all_sources)
    rendered_sources = paginated_query('sources', 25, offset)
    pagination = Pagination(page=page, total=total, per_page=25,
                            offset=offset, css_framework='bootstrap4')
    return render_template('domain_sources.html', title='Sources', rows=rendered_sources,
                            page=page, pagination=pagination, total=total)

@app.route('/search', methods=['GET','POST'])
def search():
    page, per_page, offset = get_page_args()
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
        total = len(query)
        pagination = Pagination(page=page, total=total, per_page=25,
                            offset=offset, css_framework='bootstrap4')
        return render_template('paginated_search.html', data=query,
                                page=page, pagination=pagination)
    return render_template('search.html')

@app.route('/figure_1')
def figure1():
    fig, ax = plt.subplots(figsize=(10.24,7.68))

    dframeD = pd.read_sql_query("select * from domains order by hits desc limit 10",
                engine)
    titleD = dframeD['title']
    domainD = dframeD['domain']
    hitsD = dframeD['hits']

    plt.barh(domainD,hitsD,align='center',color='orange')
    plt.xlabel('Hits')
    plt.ylabel('Domain')
    ax.invert_yaxis()
    plt.title('Hits / Top 10 .onion Domains')
    plt.tight_layout(w_pad=1)

    canvasD = fg(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)

    return send_file(img, mimetype='image/png')

@app.route('/figure_2')
def figure2():
    fig2, ax2 = plt.subplots(figsize=(10.24,7.68))

    dframeS = pd.read_sql_query("select * from sources order by hits desc limit 12",
                engine).drop([2,8])
    domainS = dframeS['domain']
    hitsS = dframeS['hits']

    plt.barh(domainS,hitsS,align='center',color='orange')
    plt.xlabel('Hits')
    plt.ylabel('Domain')
    ax2.invert_yaxis()
    plt.title('Hits / Top 10 .onion Sources')
    plt.tight_layout(w_pad=1)

    canvasS = fg(fig2)
    img2 = BytesIO()
    fig2.savefig(img2)
    img2.seek(0)

    return send_file(img2, mimetype='image/png')

@app.route('/rankings')
def rankings():
    rankfig, (ra1,ra2) = plt.subplots(2,figsize=(10.24,7.68))

    dframe1 = pd.read_sql_query("select * from domains order by hits desc",
                    engine)
    title1 = dframe1['title']
    hitRank1 = []
    for i in range(0,len(title1)):
        hitRank1.append(i)
    hits1 = dframe1['hits']

    dframe2 = pd.read_sql_query("select * from sources order by hits desc",
                    engine)
    hits2 = dframe2['hits']
    hitRank2 = []
    for i in range(0,len(hits2)):
        hitRank2.append(i)

    ra1.plot(hitRank1,hits1,color='orange')
    ra1.set_title('Hits by Rank, .onions')

    ra2.plot(hitRank2,hits2,color='orange')
    ra2.set_title('Hits by Rank, Sources')

    for ax in (ra1,ra2):
        ax.set(xlabel='Rank',ylabel='Hits')

    plt.tight_layout(w_pad=1)

    canvasD = fg(rankfig)
    img3 = BytesIO()
    rankfig.savefig(img3)
    img3.seek(0)

    return send_file(img3, mimetype='image/png')

@app.route('/statuses')
def statuses():
    sfig, (ax1, ax2) = plt.subplots(2,figsize=(11.36,13.37))

    status = pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status='200'",
                    engine)
    status = status.rename(index={0: 1})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status like '%30%'",
                    engine))
    status = status.rename(index={0: 2})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status like '%40%'",
                    engine))
    status = status.rename(index={0: 3})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status like '%50%'",
                    engine))
    status = status.rename(index={0: 4})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status='ConnectTimeout'",
                    engine))
    status = status.rename(index={0: 5})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status='SSLError'",
                    engine))
    status = status.rename(index={0: 6})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status like '%Attribute%'",
                    engine))
    status = status.rename(index={0: 7})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status like '%Read%'",
                    engine))
    status = status.rename(index={0: 8})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status like '%Connection%'",
                    engine))
    status = status.rename(columns={'count(*)': 'Hits'}, index={0: 9})
    status = status.rename(index={1:0,2:1,3:2,4:3,5:4,6:5,7:6,8:7,9:8})

    newCol = pd.DataFrame(['200 Status',
                           '300 Series Status',
                           '400 Series Status',
                           '500 Series Status',
                           'Connect Timeout',
                           'SSLError',
                           'Attribute Error',
                           'Read Timeout',
                           'Connection Error'],columns=['Status'])

    dframe = pd.DataFrame({'Status': newCol['Status'],
                           'Hits': status['Hits']}).sort_values('Hits',ascending=False)

    ax1.set_title('Hits by Status')
    ax2.set_title('Hits by Status')

    bar1 = ax1.barh(dframe['Status'],dframe['Hits'],align='center',color='orange')
    ax1.invert_yaxis()

    bar2 = ax2.barh(dframe['Status'].drop([4]),dframe['Hits'].drop([4]),align='center',color='orange')
    ax2.invert_yaxis()

    for index, value in enumerate(dframe['Hits']):
        ax1.text(value, index, value)
    for index, value in enumerate(dframe['Hits'].drop([4])):
        ax2.text(value, index, value)

    for ax in (ax1, ax2):
        ax.set(xlabel='Hits',ylabel='Status')

    plt.tight_layout(w_pad=1)

    canvasD = fg(sfig)
    img4 = BytesIO()
    sfig.savefig(img4)
    img4.seek(0)

    return send_file(img4, mimetype='image/png')

@app.route('/status_pie')
def status_pie():
    fig, ax = plt.subplots(figsize=(10.24,7.68))

    status = pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status='200'",
                    engine)
    status = status.rename(index={0: 1})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status like '%30%'",
                    engine))
    status = status.rename(index={0: 2})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status like '%40%'",
                    engine))
    status = status.rename(index={0: 3})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status like '%50%'",
                    engine))
    status = status.rename(index={0: 4})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status='ConnectTimeout'",
                    engine))
    status = status.rename(index={0: 5})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status='SSLError'",
                    engine))
    status = status.rename(index={0: 6})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status like '%Attribute%'",
                    engine))
    status = status.rename(index={0: 7})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status like '%Read%'",
                    engine))
    status = status.rename(index={0: 8})
    status = status.append(pd.read_sql_query("select count(*) from timestamps where timestamp like '%04/%' and status like '%Connection%'",
                    engine))
    status = status.rename(columns={'count(*)': 'Hits'}, index={0: 9})
    status = status.rename(index={1:0,2:1,3:2,4:3,5:4,6:5,7:6,8:7,9:8})

    newCol = pd.DataFrame(['200 Status',
                           '300 Series Status',
                           '400 Series Status',
                           '500 Series Status',
                           'Connect Timeout',
                           'SSLError',
                           'Attribute Error',
                           'Read Timeout',
                           'Connection Error'],columns=['Status'])

    dframe = pd.DataFrame({'Status': newCol['Status'],
                           'Hits': status['Hits']}).sort_values('Hits',ascending=False)

    labels = dframe['Status'].drop([0,4,1])
    sizes = dframe['Hits'].drop([0,4,1])

    ax.pie(sizes,labels=labels,autopct='%1.1f%%',startangle=45)
    ax.axis('equal')

    canvasD = fg(fig)
    img5 = BytesIO()
    fig.savefig(img5)
    img5.seek(0)

    return send_file(img5, mimetype='image/png')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')
