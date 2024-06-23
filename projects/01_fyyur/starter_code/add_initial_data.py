from app import db, app
from models import Artist, Genre, Venue
from sqlalchemy import select


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


if __name__ == "__main__":
    add_initial_genres()
    add_initial_artists()
