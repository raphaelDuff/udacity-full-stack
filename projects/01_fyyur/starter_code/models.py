from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


artist_genre_association = Table(
    "artist_genre",
    Base.metadata,
    Column("artist_id", Integer, ForeignKey("artists.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)

venue_genre_association = Table(
    "venue_genre",
    Base.metadata,
    Column("venue_id", Integer, ForeignKey("venues.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)


class Genre(db.Model):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)

    artists = relationship(
        "Artist", secondary=artist_genre_association, back_populates="genres"
    )
    venues = relationship(
        "Venue", secondary=venue_genre_association, back_populates="genres"
    )


class Venue(db.Model):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    genres: Mapped[list[Genre]] = relationship(
        "Genre", secondary=venue_genre_association, back_populates="venues"
    )
    city: Mapped[str] = mapped_column(String(120), nullable=False)
    state: Mapped[str] = mapped_column(String(120), nullable=False)
    address: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(120), nullable=False)
    image_link: Mapped[str] = mapped_column(String(500), nullable=False)
    facebook_link: Mapped[str] = mapped_column(String(120), nullable=False)
    seeking_talent: Mapped[bool] = mapped_column(Boolean, default=True)
    seeking_description: Mapped[Optional[str]]
    website: Mapped[str] = mapped_column(String(120), nullable=False)


class Artist(db.Model):
    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    city: Mapped[str] = mapped_column(String(120), nullable=False)
    state: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(120), nullable=False)
    genres: Mapped[list[Genre]] = relationship(
        "Genre", secondary=artist_genre_association, back_populates="artists"
    )
    image_link: Mapped[str] = mapped_column(String(500), nullable=False)
    facebook_link: Mapped[str] = mapped_column(String(120), nullable=False)
    seeking_venue: Mapped[bool] = mapped_column(Boolean, default=True)
    seeking_description: Mapped[Optional[str]]
    website: Mapped[str] = mapped_column(String(120), nullable=False)


class Show(db.Model):
    __tablename__ = "shows"

    id: Mapped[int] = mapped_column(
        Integer(), primary_key=True, index=True, unique=True
    )
    venue_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("venues.id"), nullable=False
    )
    artist_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("artists.id"), nullable=False
    )
    start_time: Mapped[datetime]
