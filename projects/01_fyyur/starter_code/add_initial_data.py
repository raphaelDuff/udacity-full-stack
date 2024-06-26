from app import db, app
from models import Artist, Genre, Show, Venue
from sqlalchemy import select
import dateutil.parser


def add_initial_genres():
    with app.app_context():

        genres = [
            Genre(name="Alternative"),
            Genre(name="Blues"),
            Genre(name="Classical"),
            Genre(name="Country"),
            Genre(name="Electronic"),
            Genre(name="Folk"),
            Genre(name="Funk"),
            Genre(name="Hip-Hop"),
            Genre(name="Heavy Metal"),
            Genre(name="Instrumental"),
            Genre(name="Jazz"),
            Genre(name="Musical Theatre"),
            Genre(name="Pop"),
            Genre(name="Punk"),
            Genre(name="R&B"),
            Genre(name="Reggae"),
            Genre(name="Rock n Roll"),
            Genre(name="Soul"),
            Genre(name="Swing"),
            Genre(name="Other"),
        ]
        db.session.bulk_save_objects(genres)
        db.session.commit()


def add_initial_artists():

    with app.app_context():
        stmt_select_genre_rock = select(Genre).where(Genre.name == "Rock n Roll")
        stmt_select_genre_jazz = select(Genre).where(Genre.name == "Jazz")
        stmt_select_genre_classical = select(Genre).where(Genre.name == "Classical")
        genre_rock = db.session.scalars(stmt_select_genre_rock).one()
        genre_jazz = db.session.scalars(stmt_select_genre_jazz).one()
        genre_classical = db.session.scalars(stmt_select_genre_classical).one()

        artist_guns = Artist(
            id=4,
            name="Guns N Petals",
            genres=[genre_rock],
            city="San Francisco",
            state="CA",
            phone="326-123-5000",
            website="https://www.gunsnpetalsband.com",
            facebook_link="https://www.facebook.com/GunsNPetals",
            seeking_venue=True,
            seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
            image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        )
        artist_quevedo = Artist(
            id=5,
            name="Matt Quevedo",
            genres=[genre_jazz],
            city="New York",
            state="NY",
            phone="300-400-5000",
            website="",
            facebook_link="https://www.facebook.com/mattquevedo923251523",
            seeking_venue=False,
            seeking_description=None,
            image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        )
        artist_sax_band = Artist(
            id=6,
            name="The Wild Sax Band",
            genres=[genre_jazz, genre_classical],
            city="San Francisco",
            state="CA",
            phone="432-325-5432",
            website="",
            facebook_link="",
            seeking_venue=False,
            seeking_description=None,
            image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        )

        db.session.add(artist_guns)
        db.session.add(artist_quevedo)
        db.session.add(artist_sax_band)
        db.session.commit()


def add_initial_venues():

    with app.app_context():
        stmt_select_genre_rock = select(Genre).where(Genre.name == "Rock n Roll")
        stmt_select_genre_jazz = select(Genre).where(Genre.name == "Jazz")
        stmt_select_genre_classical = select(Genre).where(Genre.name == "Classical")
        stmt_select_genre_folk = select(Genre).where(Genre.name == "Folk")
        stmt_select_genre_reggae = select(Genre).where(Genre.name == "Reggae")
        stmt_select_genre_swing = select(Genre).where(Genre.name == "Swing")
        stmt_select_genre_rnb = select(Genre).where(Genre.name == "R&B")
        stmt_select_genre_hiphop = select(Genre).where(Genre.name == "Hip-Hop")

        genre_rock = db.session.scalars(stmt_select_genre_rock).one()
        genre_jazz = db.session.scalars(stmt_select_genre_jazz).one()
        genre_classical = db.session.scalars(stmt_select_genre_classical).one()
        genre_folk = db.session.scalars(stmt_select_genre_folk).one()
        genre_reggae = db.session.scalars(stmt_select_genre_reggae).one()
        genre_swing = db.session.scalars(stmt_select_genre_swing).one()
        genre_rnb = db.session.scalars(stmt_select_genre_rnb).one()
        genre_hiphop = db.session.scalars(stmt_select_genre_hiphop).one()

        venue_musical_hop = Venue(
            id=1,
            name="The Musical Hop",
            genres=[genre_classical, genre_folk, genre_jazz, genre_reggae, genre_swing],
            city="San Francisco",
            state="CA",
            address="1015 Folsom Street",
            phone="123-123-1234",
            website="https://www.themusicalhop.com",
            facebook_link="https://www.facebook.com/TheMusicalHop",
            seeking_talent=True,
            seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
            image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        )
        venue_dueling_pianos = Venue(
            id=2,
            name="The Dueling Pianos Bar",
            genres=[genre_classical, genre_hiphop, genre_rnb],
            city="New York",
            state="NY",
            address="335 Delancey Street",
            phone="914-003-1132",
            website="https://www.theduelingpianos.com",
            facebook_link="https://www.facebook.com/theduelingpianos",
            seeking_talent=False,
            seeking_description=None,
            image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
        )
        venue_park_square = Venue(
            id=3,
            name="Park Square Live Music & Coffee",
            genres=[genre_classical, genre_folk, genre_jazz, genre_rock],
            city="San Francisco",
            state="CA",
            address="34 Whiskey Moore Ave",
            phone="415-000-1234",
            website="https://www.parksquarelivemusicandcoffee.com",
            facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
            seeking_talent=False,
            seeking_description=None,
            image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        )

        db.session.add(venue_musical_hop)
        db.session.add(venue_dueling_pianos)
        db.session.add(venue_park_square)
        db.session.commit()


def add_initial_shows():

    with app.app_context():

        show_one = Show(
            id=1,
            venue_id=1,
            artist_id=4,
            start_time=dateutil.parser.isoparse("2019-05-21T21:30:00.000Z"),
        )
        show_two = Show(
            id=2,
            venue_id=3,
            artist_id=5,
            start_time=dateutil.parser.isoparse("2019-06-15T23:00:00.000Z"),
        )
        show_three = Show(
            id=3,
            venue_id=3,
            artist_id=6,
            start_time=dateutil.parser.isoparse("2035-04-01T20:00:00.000Z"),
        )
        show_four = Show(
            id=4,
            venue_id=3,
            artist_id=6,
            start_time=dateutil.parser.isoparse("2035-04-08T20:00:00.000Z"),
        )
        show_five = Show(
            id=5,
            venue_id=3,
            artist_id=6,
            start_time=dateutil.parser.isoparse("2035-04-15T20:00:00.000Z"),
        )
        db.session.add(show_one)
        db.session.add(show_two)
        db.session.add(show_three)
        db.session.add(show_four)
        db.session.add(show_five)
        db.session.commit()


if __name__ == "__main__":
    add_initial_genres()
    add_initial_artists()
    add_initial_venues()
    add_initial_shows()
