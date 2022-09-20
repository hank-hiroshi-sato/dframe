import dataset

import click
from flask import current_app, g
from flask.cli import with_appcontext

# 対象のDBを指定
DBMS = 'mysql'
USER = 'root'
PASS = 'mypass'
HOST = 'localhost'
SYSDB = 'dframe'
CHARSET = 'utf8'

def get_db():
    if 'db' not in g:
        g.db = dataset.connect('{0}://{1}:{2}@{3}/{4}?charset={5}'.format(DBMS, USER, PASS, HOST, SYSDB, CHARSET))
        
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    '''
    with current_app.open_resource('schema.sql') as f:
        db.query(f.read().decode('utf8'))
    '''
    return db


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)