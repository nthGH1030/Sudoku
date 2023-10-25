import sqlite3
from . import solver
import click
from flask import current_app, g

#Get database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Run sql command in schema.sql
def init_db():
    db = get_db()
    # run the following if the database is not established
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if tables:
        click.echo('Database is already initialized.')
    else:
        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
        click.echo('Initialized the database.')

        #insert 20 set of question and answers into the database
        rowInitial = "ABCDEFGHI"
        colInitial = "123456789"

        for i in range(20):
            index = 0
            question, answer = solver.solve()
            for char in rowInitial:
                for digit in colInitial:
                    #squares.append(char + digit)
                    #questionGrid[char + digit] = question[index]
                    #answerGrid[char + digit] = answer[index]
                    #append the questionGrid into database
                    db.execute(
                        'INSERT INTO question (question_id, question_key, question_value)'
                        'VALUES (?,?,?)',
                        (i, char + digit, question[index])
                    )
                    db.execute(
                        'INSERT INTO answer (question_id, ans_key, ans_value)'
                        'VALUES (?,?,?)',
                        (i, char + digit, answer[index])
                    )
                    
                    index += 1

        db.commit()


        
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)