from flask import current_app
from flask_sqlalchemy import SQLAlchemy
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


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


def drop_db(app):
    with app.app_context():
        db.reflect()
        db.drop_all()


def populate_db(app):
    with app.app_context():
        from database.model.pond import (
            Pond,
            WaterQuality,
            FishData,
            FishPondMetrics,
        )

        from database.model.user import User
        from datetime import datetime
        # Fetch or create a user for pond ownership
        user = User.query.first()
        if not user:
            user = User(username="default_user", password="password", email="user1@example.com")
            db.session.add(user)
            db.session.commit()

        # Example data for Pond
        ponds = [
            {"pond_name": "Pond A", "location": "Location A", "owner_id": user.user_id},
            {"pond_name": "Pond B", "location": "Location B", "owner_id": user.user_id},
        ]

        for pond in ponds:
            p = Pond(**pond)
            db.session.add(p)
        db.session.commit()

        # Example data for WaterQuality
        water_qualities = [
            {
                "pond_id": 1,
                "pH": 7.0,
                "turbidity": 5.0,
                "temperature": 25.0,
                "nitrate": 10.0,
                "date": datetime(2024, 7, 31, 8, 0, 0)
            },
            {
                "pond_id": 1,
                "pH": 7.1,
                "turbidity": 4.5,
                "temperature": 26.0,
                "nitrate": 9.5,
                "date": datetime(2024, 7, 31, 12, 0, 0)
            },
            {
                "pond_id": 1,
                "pH": 6.9,
                "turbidity": 6.0,
                "temperature": 24.5,
                "nitrate": 10.5,
                "date": datetime(2024, 8, 1, 8, 0, 0)
            },
            {
                "pond_id": 1,
                "pH": 7.2,
                "turbidity": 5.5,
                "temperature": 25.5,
                "nitrate": 11.0,
                "date": datetime(2024, 8, 1, 12, 0, 0)
            },
            {
                "pond_id": 2,
                "pH": 6.5,
                "turbidity": 10.0,
                "temperature": 22.0,
                "nitrate": 5.0,
                "date": datetime(2024, 7, 31, 8, 0, 0)
            },
            {
                "pond_id": 2,
                "pH": 6.6,
                "turbidity": 9.5,
                "temperature": 22.5,
                "nitrate": 5.2,
                "date": datetime(2024, 7, 31, 12, 0, 0)
            },
            {
                "pond_id": 2,
                "pH": 6.4,
                "turbidity": 10.5,
                "temperature": 21.5,
                "nitrate": 4.8,
                "date": datetime(2024, 8, 1, 8, 0, 0)
            },
            {
                "pond_id": 2,
                "pH": 6.7,
                "turbidity": 10.2,
                "temperature": 22.2,
                "nitrate": 5.1,
                "date": datetime(2024, 8, 1, 12, 0, 0)
            },
        ]

        for water_quality in water_qualities:
            wq = WaterQuality(**water_quality)
            db.session.add(wq)
        db.session.commit()

        # Example data for FishData
        fish_data = [
            {
                "pond_id": 1,
                "fish_weight": 1.5,
                "fish_height": 10.0,
                "fish_population": 100,
                "date": datetime(2024, 7, 31, 8, 0, 0)
            },
            {
                "pond_id": 1,
                "fish_weight": 1.6,
                "fish_height": 10.5,
                "fish_population": 105,
                "date": datetime(2024, 7, 31, 12, 0, 0)
            },
            {
                "pond_id": 1,
                "fish_weight": 1.4,
                "fish_height": 9.8,
                "fish_population": 95,
                "date": datetime(2024, 8, 1, 8, 0, 0)
            },
            {
                "pond_id": 1,
                "fish_weight": 1.7,
                "fish_height": 10.2,
                "fish_population": 110,
                "date": datetime(2024, 8, 1, 12, 0, 0)
            },
            {
                "pond_id": 2,
                "fish_weight": 2.0,
                "fish_height": 12.0,
                "fish_population": 150,
                "date": datetime(2024, 7, 31, 8, 0, 0)
            },
            {
                "pond_id": 2,
                "fish_weight": 2.1,
                "fish_height": 12.5,
                "fish_population": 155,
                "date": datetime(2024, 7, 31, 12, 0, 0)
            },
            {
                "pond_id": 2,
                "fish_weight": 1.9,
                "fish_height": 11.8,
                "fish_population": 145,
                "date": datetime(2024, 8, 1, 8, 0, 0)
            },
            {
                "pond_id": 2,
                "fish_weight": 2.2,
                "fish_height": 12.3,
                "fish_population": 160,
                "date": datetime(2024, 8, 1, 12, 0, 0)
            },
        ]

        for fish in fish_data:
            f = FishData(**fish)
            db.session.add(f)
        db.session.commit()

        # Example data for FishPondMetrics
        metrics = [
            {
                "pond_id": 1,
                "total_fish_weight": 1.5 * 100 + 1.6 * 105 + 1.4 * 95 + 1.7 * 110,
                "average_fish_weight": (1.5 + 1.6 + 1.4 + 1.7) / 4,
                "average_fish_height": (10.0 + 10.5 + 9.8 + 10.2) / 4,
                "total_population": 100 + 105 + 95 + 110,
            },
            {
                "pond_id": 2,
                "total_fish_weight": 2.0 * 150 + 2.1 * 155 + 1.9 * 145 + 2.2 * 160,
                "average_fish_weight": (2.0 + 2.1 + 1.9 + 2.2) / 4,
                "average_fish_height": (12.0 + 12.5 + 11.8 + 12.3) / 4,
                "total_population": 150 + 155 + 145 + 160,
            },
        ]

        for metric in metrics:
            m = FishPondMetrics(**metric)
            db.session.add(m)
        db.session.commit()

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
    click.echo("Initialized the database.")


@click.command("drop-db")
@with_appcontext
def drop_db_command():
    drop_db(current_app)
    click.echo("Dropped the database.")


@click.command("populate-db")
@with_appcontext
def populate_db_command():
    populate_db(current_app)
    click.echo("Database populated with dummy data.")


# Ensure the command is added to the Flask CLI
def add_commands(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(drop_db_command)
    app.cli.add_command(populate_db_command)
