from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import click
from flask.cli import with_appcontext
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    ProgrammingError,
    DataError,
    NoResultFound,
    MultipleResultsFound,
)

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)

def format_database_error(exception):
    if isinstance(exception, IntegrityError):
        return f"Integrity constraint violation: {exception.orig}"
    elif isinstance(exception, OperationalError):
        return f"Database operation error: {exception.orig}"
    elif isinstance(exception, ProgrammingError):
        return f"Database programming error: {exception.orig}"
    elif isinstance(exception, DataError):
        return f"Data error: {exception.orig}"
    elif isinstance(exception, NoResultFound):
        return f"No result found: {exception.orig}"
    elif isinstance(exception, MultipleResultsFound):
        return f"Multiple results found: {exception.orig}"
    else:
        return f"Unknown database error: {exception}"

@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db(current_app)
    with current_app.app_context():
        db.create_all()
    click.echo("Initialized the database.")

@click.command("drop-db")
@with_appcontext
def drop_db_command():
    with current_app.app_context():
        db.drop_all()
    click.echo("Dropped the database.")
