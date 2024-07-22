from enum import Enum
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
    SubmitField,
)
from wtforms.validators import DataRequired, URL, ValidationError
import re


class StateEnum(Enum):
    AL = "AL"
    AK = "AK"
    AZ = "AZ"
    AR = "AR"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DE = "DE"
    DC = "DC"
    FL = "FL"
    GA = "GA"
    HI = "HI"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    IA = "IA"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    ME = "ME"
    MT = "MT"
    NE = "NE"
    NV = "NV"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NY = "NY"
    NC = "NC"
    ND = "ND"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    MD = "MD"
    MA = "MA"
    MI = "MI"
    MN = "MN"
    MS = "MS"
    MO = "MO"
    PA = "PA"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    UT = "UT"
    VT = "VT"
    VA = "VA"
    WA = "WA"
    WV = "WV"
    WI = "WI"
    WY = "WY"

    @classmethod
    def choices(cls):
        """Return a list of tuples for form choices."""
        return [(member.name, member.value) for member in cls]


class GenreEnum(Enum):
    ALTERNATIVE = "Alternative"
    BLUES = "Blues"
    CLASSICAL = "Classical"
    COUNTRY = "Country"
    ELECTRONIC = "Electronic"
    FOLK = "Folk"
    FUNK = "Funk"
    HIPHOP = "Hip-Hop"
    HEAVYMETAL = "Heavy Metal"
    INSTRUMENTAL = "Instrumental"
    JAZZ = "Jazz"
    MUSICAL = "Musical Theatre"
    POP = "Pop"
    PUNK = "Punk"
    RNB = "R&B"
    REGGAE = "Reggae"
    ROCK = "Rock n Roll"
    SOUL = "Soul"
    OTHER = "Other"

    @classmethod
    def values_from_names(cls, names):
        """Convert a list of enum names to a list of enum values."""
        return [cls[name].value for name in names]


def phone_number_validator(form, field):
    phone_number = field.data
    if not re.match(r"^\d{3}-\d{3}-\d{4}$", phone_number):
        raise ValidationError("Phone number must be in the format xxx-xxx-xxxx.")


def validate_facebook_url(form, field):
    if not field.data.startswith("https://www.facebook.com/"):
        raise ValidationError("The URL must start with 'https://www.facebook.com/'.")


class ShowForm(FlaskForm):
    artist_id = StringField("artist_id")
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )
    submit = SubmitField("Create Venue")


class VenueForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        "state", validators=[DataRequired()], choices=StateEnum.choices()
    )

    address = StringField("address", validators=[DataRequired()])
    phone = StringField("phone", validators=[DataRequired(), phone_number_validator])
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        "genres",
        validators=[DataRequired()],
        choices=[(genre.name, genre.value) for genre in GenreEnum],
    )
    facebook_link = StringField(
        "facebook_link", validators=[DataRequired(), URL(), validate_facebook_url]
    )
    website_link = StringField("website_link")
    seeking_talent = BooleanField("seeking_talent")
    seeking_description = StringField("seeking_description")
    submit = SubmitField("Save")


class ArtistForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    tate = SelectField(
        "state", validators=[DataRequired()], choices=StateEnum.choices()
    )
    phone = StringField("phone", validators=[DataRequired(), phone_number_validator])
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        "genres",
        validators=[DataRequired()],
        choices=[(genre.name, genre.value) for genre in GenreEnum],
    )
    facebook_link = StringField(
        "facebook_link", validators=[DataRequired(), URL(), validate_facebook_url]
    )

    website_link = StringField("website_link")
    seeking_venue = BooleanField("seeking_venue")
    seeking_description = StringField("seeking_description")
    submit = SubmitField("Save")
