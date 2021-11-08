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


class TimePunches(db.Model):
    """Time Punch Table."""

    __tablename__ = "time_punch"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True,)

    comments = db.Column(db.String,)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow,)
    user_name = db.relationship('User', backref='TimePunches',)

    def __repr__(self):
        """Shows info about the time punches."""

        return f"<User ID = {self.user_id}, User Name={self.id}, comments={self.comments}, Time Punch Details={self.created_date}.>"


class Page(db.Model):
    """A Book."""
    __tablename__ = "pages"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True,)
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.id'),)
    text = db.Column(db.String,)
    image = db.Column(db.String,)
    page_number = db.Column(db.Integer,)
    book = db.relationship('Book', backref='pages',)

    def __repr__(self):
        """show info about the pages"""

        return f"< Page ID ={self.id},page text={self.text}, page image = {self.image}, page book_id = {self.book_id}, page_number = {self.page_number}>"


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
