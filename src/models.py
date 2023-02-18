from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String

db = SQLAlchemy()

Base = declarative_base()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
        
class Personajes(Base):
    __tablename__ = 'personaje'
    id_personaje = Column(Integer, primary_key=True)
    nombre = Column(String(250))
    titulo = Column(String(250))
    casa= Column(String(250), nullable=False)
    perso_a_casa = Column(Integer, ForeignKey('casa.id_casa'))
    perso_a_conti = Column(Integer, ForeignKey('continente.id_continente'))
    perso_a_fav = Column(Integer, ForeignKey('favorito.id_favoritos'))

class Casas(Base):
    __tablename__ = 'casa'
    id_casa = Column(Integer, primary_key=True)
    nombre = Column(String(250))

class Continentes(Base):
    __tablename__ = 'continente'
    id_continente = Column(Integer, primary_key=True)
    nombre = Column(String(250))
    conti_a_fav = Column(Integer, ForeignKey('favorito.id_favoritos'))

class Favoritos(Base):
    __tablename__ = 'favorito'
    id_favoritos = Column(Integer, primary_key=True)
    user_a_fav = Column(Integer, ForeignKey('usuario.id_usuario'))