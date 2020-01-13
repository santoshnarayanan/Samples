from .db import db


class Movie(db.Document):
    name = db.StringField(required=True, unique=True)
    cast = db.ListField(db.StringField(), required=True)
    genres = db.ListField(db.StringField(), required=True)
