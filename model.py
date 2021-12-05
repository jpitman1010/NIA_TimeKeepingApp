"""Tables for NIA Time Keeping App and connection to database"""
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, String, LargeBinary, Boolean

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri='postgresql:///timeKeeperNIA', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


class User(db.Model):
    """A user. db.Model is PSQL design tool to help manage, design the database."""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True,)
    email = db.Column(db.String, unique=True,)
    fname = db.Column(db.String,)
    lname = db.Column(db.String,)
    password = db.Column(db.String, nullable=False,)
    photo = db.Column(db.String,)
    admin = db.Column(db.Boolean,)

    def __repr__(self):
        """Shows info about the user"""

        return f"<User ID={self.id} Email={self.email}, password={self.password}, author={self.fname}{self.lname}, User Photo={self.photo}>"


class TimeEntry(db.Model):
    """Time Entry Table."""

    __tablename__ = "time_entry"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True,)
    comments = db.Column(db.String,)
    time_entry = db.Column(db.String,)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow,)
    user_name = db.relationship('User', backref='TimeEntry',)

    def __repr__(self):
        """Shows info about the time entryes."""

        return f"<Time Entry ID = {self.id}, User ID={self.user_id}, comments={self.comments}, Time Entry Created Date={self.created_date}, Time Entry={self.time_entry}.>"


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    db.create_all()
