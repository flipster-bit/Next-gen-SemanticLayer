import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    db = get_db()

    # with current_app.open_resource('C:\\Users\\himanshu.n\\Downloads\\northwindnorthwind') as f:
    #     db.executescript(f.read().decode('utf8'))
    


@click.command('init-db')

def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('view-data')

def view_data_command():
    """View data from a specific table."""
    db = get_db()
    table_name = 'Customers'  # Replace with the table you want to view
    query = f'SELECT * FROM {table_name}'
    
    try:
        cursor = db.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(dict(row))  # Convert row to dictionary for better readability
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")



def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(view_data_command)


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()