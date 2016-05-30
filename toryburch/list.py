# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~
    A microblog example application written as Flask tutorial with
    Flask and sqlite3.
    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import copy


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path +'/db/', 'toryburch.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = dict_factory   #sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('./db/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


# @app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# @app.route('/')
# def show_entries():
#     db = get_db()
#     cur = db.execute('SELECT CATEGORY, NAME, STANDARD_PRICE, SALES_PRICE, DESC, URL, IMG_URL, CREATED, LAST_UPD FROM TORYBURCH;')
#     entries = cur.fetchall()
#     return render_template('show_entries.html', entries=entries)

@app.route('/')
def home():
    db = get_db()
    # cur = db.execute('SELECT PROD.CATEGORY, PROD.NAME, PROD.DESC, PROD.URL'
    #                  ', PROD.IMG_URL, PRICE.STANDARD_PRICE, PRICE.SALES_PRICE'
    #                  ', PRICE.CREATED, PRICE.LAST_UPD '
    #                  'FROM TORY_PROD PROD, TORY_PRICE PRICE '
    #                  'WHERE PROD.ROW_ID = PRICE.PAR_ROW_ID AND PROD.ROW_ID = 1;')
    # entries = cur.fetchall()
    # return render_template('home.html', entries=entries)

    sql_prod = 'SELECT ROW_ID, CATEGORY, NAME, DESC, IMG_URL, URL' \
               ', STANDARD_PRICE, SALES_PRICE, LAST_UPD ' \
               'FROM TORY_PROD ' \
               'WHERE SALES_PRICE <> \'$0\';'
    cur_prod = db.execute(sql_prod)
    prods = cur_prod.fetchall()
    for prod in prods:
        prod_id = prod["ROW_ID"]
        sql_price = 'SELECT STANDARD_PRICE, SALES_PRICE, CREATED, LAST_UPD ' \
                    'FROM TORY_PRICE ' \
                    'WHERE PAR_ROW_ID = :PAR_ROW_ID;'
        cur_price = db.execute(sql_price, {"PAR_ROW_ID": prod_id})
        prices = cur_price.fetchall()
        prod['PRICE'] = prices
        # prods.append(prod)
        # prod_list = list(prods[prod_n])
        # prod_list.append(prices)
    #     prods[prod_n] = (100, 200, 300)
    return render_template('home.html', entries=prods)



@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
#    app.run()
	app.run(debug=True)
