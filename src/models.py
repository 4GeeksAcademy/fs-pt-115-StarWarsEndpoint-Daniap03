from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column , ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_characters_table = Table(
    "favorite_characters",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True),
)

favorite_vehicles_table = Table(
    "favorite_vehicles",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("vehicle_id", ForeignKey("vehicles.id"), primary_key=True),
)

favorite_planets_table = Table(
    "favorite_planets",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("planet_id", ForeignKey("planets.id"), primary_key=True),
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120),unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(20), nullable=False)
    lastname: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    favorite_characters: Mapped[List["Character"]] = relationship(
        "Character",
        secondary=favorite_characters_table,
        back_populates="favorites_by"
    )

    favorite_vehicles: Mapped[List["Vehicles"]] = relationship(
        "Vehicles",
        secondary=favorite_vehicles_table,
        back_populates="favorites_by"
    )

    favorite_planets: Mapped[List["Planets"]] = relationship(
        "Planets",
        secondary=favorite_planets_table,
        back_populates="favorites_by"
    )


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname" : self.lastname,
            "favorite_characters": [character.serialize() for character in self.favorite_characters],
            "favorite_vehicles": [vehicle.serialize() for vehicle in self.favorite_vehicles],
            "favorite_planets": [planet.serialize() for planet in self.favorite_planets]
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]= mapped_column(String(30), nullable=False)

    favorites_by: Mapped[List["User"]] = relationship(
        "User",
        secondary=favorite_characters_table,
        back_populates="favorite_characters"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Vehicles(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]= mapped_column(String(50), nullable=False)

    favorites_by: Mapped[List["User"]] = relationship(
        "User",
        secondary=favorite_vehicles_table,
        back_populates="favorite_vehicles"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]= mapped_column(String(50), nullable=False)

    favorites_by: Mapped[List["User"]] = relationship(
        "User",
        secondary=favorite_planets_table,
        back_populates="favorite_planets"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
    