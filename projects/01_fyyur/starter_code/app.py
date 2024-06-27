# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
from datetime import datetime
import dateutil.parser
import babel
from babel.dates import format_datetime as format_datetime_babel
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    session,
    url_for,
)
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
from models import (
    artist_genre_association,
    venue_genre_association,
    Artist,
    Genre,
    Show,
    Venue,
)
import os
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, select, String, Table
from typing import Optional

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)

# Flask-Moment library is used to facilitate the formatting and display of dates and times
moment = Moment(app)
app.config.from_object("config")

# Adding the Flask_Migrate
migrate = Migrate(app, db)

# Initialize the app with the extension
db.init_app(app)

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale="en")


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = [
        {
            "city": "San Francisco",
            "state": "CA",
            "venues": [
                {
                    "id": 1,
                    "name": "The Musical Hop",
                    "num_upcoming_shows": 0,
                },
                {
                    "id": 3,
                    "name": "Park Square Live Music & Coffee",
                    "num_upcoming_shows": 1,
                },
            ],
        },
        {
            "city": "New York",
            "state": "NY",
            "venues": [
                {
                    "id": 2,
                    "name": "The Dueling Pianos Bar",
                    "num_upcoming_shows": 0,
                }
            ],
        },
    ]
    return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [
            {
                "id": 2,
                "name": "The Dueling Pianos Bar",
                "num_upcoming_shows": 0,
            }
        ],
    }
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: ADD the upcoming and past shows count

    stmt_select_venue_by_id = select(Venue).where(Venue.id == venue_id)
    venue_by_id = db.session.scalars(stmt_select_venue_by_id).one()

    return render_template("pages/show_venue.html", venue=venue_by_id)


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash("Venue " + request.form["name"] + " was successfully listed!")
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template("pages/home.html")


@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():

    stmt_select_all_artists = select(Artist).order_by(Artist.name)
    data_artists = db.session.scalars(stmt_select_all_artists).all()
    return render_template("pages/artists.html", artists=data_artists)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [
            {
                "id": 4,
                "name": "Guns N Petals",
                "num_upcoming_shows": 0,
            }
        ],
    }
    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):

    # TODO - ADD the upcoming and past shows count
    stmt_select_upcoming_shows = select(Show).where(Show.start_time >= datetime.now())
    upcoming_shows = db.session.scalars(stmt_select_upcoming_shows).all()
    upcoming_shows_count = len(upcoming_shows)

    stmt_select_past_shows = select(Show).where(Show.start_time < datetime.now())
    past_shows = db.session.scalars(stmt_select_past_shows).all()
    past_shows_count = len(past_shows)

    stmt_select_artist_by_id = select(Artist).where(Artist.id == artist_id)
    data_by_id = db.session.scalars(stmt_select_artist_by_id).one()

    return render_template("pages/show_artist.html", artist=data_by_id)


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):

    # TODO: populate form with fields from artist with ID <artist_id>

    stmt_select_artist_by_id = select(Artist).where(Artist.id == artist_id)
    data_artist_by_id = db.session.scalars(stmt_select_artist_by_id).one()
    form = ArtistForm()

    return render_template(
        "forms/edit_artist.html", form=form, artist=data_artist_by_id
    )


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    # TODO: try to pre fill the values with the old values

    stmt_select_artist_by_id = select(Artist).where(Artist.id == artist_id)
    artist = db.session.scalars(stmt_select_artist_by_id).one()

    form = ArtistForm()

    if form.validate_on_submit():
        stmt_select_genres = select(Genre).where(Genre.name.in_(form.genres.data))
        genres = db.session.scalars(stmt_select_genres).all()
        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.genres = genres
        artist.facebook_link = form.facebook_link.data
        artist.image_link = form.image_link.data
        artist.website = form.website_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data

        db.session.commit()
        flash("Artist updated successfully!", "success")

    return redirect(url_for("show_artist", artist_id=artist.id))


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for("show_venue", venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash("Artist " + request.form["name"] + " was successfully listed!")
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template("pages/home.html")


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    # displays list of shows at /shows
    shows_list_to_template = []
    stmt_select_shows_join = (
        select(
            Show.start_time.label("start_time"),
            Venue.id.label("venue_id"),
            Venue.name.label("venue_name"),
            Artist.id.label("artist_id"),
            Artist.name.label("artist_name"),
            Artist.image_link.label("artist_image_link"),
        )
        .join(Artist, Show.artist_id == Artist.id)
        .join(Venue, Show.venue_id == Venue.id)
    )

    shows_data_interim = db.session.execute(stmt_select_shows_join)
    shows_list_to_template = []

    for show in shows_data_interim:
        show_dict = {
            "venue_id": show.venue_id,
            "venue_name": show.venue_name,
            "artist_id": show.artist_id,
            "artist_name": show.artist_name,
            "artist_image_link": show.artist_image_link,
            "start_time": str(show.start_time),
        }

        shows_list_to_template.append(show_dict)

    return render_template("pages/shows.html", shows=shows_list_to_template)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash("Show was successfully listed!")
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template("pages/home.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")


# Default port:
if __name__ == "__main__":
    # data = db_add_initial_artists()
    app.run(debug=True)
