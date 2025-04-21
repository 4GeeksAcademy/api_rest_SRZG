from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

db = SQLAlchemy()


class Favorite_Types(enum.Enum):
    planets = 1
    people = 2
    vehicles = 3


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(40), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(40), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)

    favorites = relationship('Favorites', back_populates='user', lazy='joined')


class Planets(db.Model):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    diameter: Mapped[str] = mapped_column(String(100), nullable=False)
    rotation_period: Mapped[str] = mapped_column(String(100), nullable=False)
    orbital_period: Mapped[str] = mapped_column(String(100), nullable=False)
    gravity: Mapped[str] = mapped_column(String(100), nullable=False)
    population: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(100), nullable=False)
    terrain: Mapped[str] = mapped_column(String(100), nullable=False)
    surface_water: Mapped[str] = mapped_column(String(100), nullable=False)

    favorites = relationship(
        'Favorites', back_populates='planet', lazy='joined')

    def serialize(self):
        # favorites = list(map(lambda f: f.serialize(), self.favorites))
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            # "favorites": favorites,
        }


class Vehicles(db.Model):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    vehicle_class: Mapped[str] = mapped_column(String(100), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=False)
    length: Mapped[str] = mapped_column(String(100), nullable=False)
    cost_in_credits: Mapped[str] = mapped_column(String(100), nullable=False)
    crew: Mapped[str] = mapped_column(String(100), nullable=False)
    max_atmosphering_speed: Mapped[str] = mapped_column(
        String(100), nullable=False)
    cargo_capacity: Mapped[str] = mapped_column(String(100), nullable=False)
    consumables: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(200), nullable=False)

    favorites = relationship(
        'Favorites', back_populates='vehicle', lazy='joined')

    def serialize(self):
        # favorites = list(map(lambda f: f.serialize(), self.favorites))
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "length": self.length,
            "cost_in_credits": self.cost_in_credits,
            "crew": self.crew,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "url": self.url,
            # "favorites": favorites,
        }


class People(db.Model):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(100), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(100), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[str] = mapped_column(String(20), nullable=False)
    mass: Mapped[str] = mapped_column(String(40), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(20), nullable=False)
    homeworld: Mapped[str] = mapped_column(String(40), nullable=False)
    url: Mapped[str] = mapped_column(String(100), nullable=False)

    favorites = relationship(
        'Favorites', back_populates='person', lazy='joined')

    def serialize(self):
        # favorites = list(map(lambda f: f.serialize(), self.favorites))
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "homeworld": self.homeworld,
            "url": self.url,
            # "favorites": favorites,
        }


class Favorites(db.Model):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    type: Mapped[Favorite_Types] = mapped_column(Enum(Favorite_Types))
    people_id: Mapped[int] = mapped_column(
        ForeignKey('people.id'), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey('vehicles.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey('planets.id'), nullable=True)

    user: Mapped[User] = relationship(back_populates="favorites")
    person: Mapped[People] = relationship(back_populates="favorites")
    planet: Mapped[Planets] = relationship(back_populates="favorites")
    vehicle: Mapped[Vehicles] = relationship(back_populates="favorites")

    def serialize(self):

        favorite_id = None
        favorite_item = None
        if self.type == Favorite_Types.people:
            favorite_id = self.people_id
            favorite_type = "people"
            favorite_item = self.person.serialize()
        elif self.type == Favorite_Types.planets:
            favorite_id = self.planet_id
            favorite_type = "planets"
            favorite_item = self.planet.serialize()
        elif self.type == Favorite_Types.vehicles:
            favorite_id = self.vehicle_id
            favorite_type = "vehicles"
            favorite_item = self.vehicle.serialize()
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": favorite_type,
            "favoriteId": favorite_id,
            "favoriteItem": favorite_item
        }
