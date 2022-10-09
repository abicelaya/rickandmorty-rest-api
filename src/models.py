from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, orm

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250))
    favorites_characters = db.relationship("Favorites_Characters")
    favorites_planets = db.relationship("Favorites_Planets")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Favorites_Characters(Base):
    __tablename__ = 'favorites_characters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

class Favorites_Planets(Base):
    __tablename__ = 'favorites_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    planets_id = db.Column(db.Integer, ForeignKey('planets.id'))

class Characters(Base):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    height = db.Column(db.Integer)
    eye_color = db.Column(db.String(250))
    favorites_characters = db.relationship("Favorites_Characters")

class Planets(Base):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    population = db.Column(db.Integer)
    gravity = db.Column(db.String(250))
    favorites_planets = db.relationship("Favorites_Planets")