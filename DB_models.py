from flask import Flask
from flask_sqlalchemy import SQLAlchemy


application = Flask(__name__)
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'

    UserId = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(120))
    Password = db.Column(db.String(500))
    IsActive = db.Column(db.Boolean)
    CreatedAt = db.Column(db.DateTime)
    EditedAt = db.Column(db.DateTime)
    CreatedBy = db.Column(db.Integer)
    EditedBy = db.Column(db.Integer)
    RoleId = db.Column(db.Integer)
    CountryID = db.Column(db.Integer)
    RegionID = db.Column(db.Integer, nullable=True)
    CityID = db.Column(db.Integer, nullable=False)

class Admin(db.Model):
    __tablename__ = 'Admin'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    user_id = db.Column(db.Integer)


class Guest(db.Model):
    __tablename__ = 'Guest'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))
    mobile = db.Column(db.String(120))
    date_of_birth = db.Column(db.DateTime)
    user_id = db.Column(db.Integer)
    gender_id = db.Column(db.Integer)

class Gender(db.Model):
    __tablename__ = 'Gender'

    id = db.Column(db.Integer, primary_key=True)
    gender_type = db.Column(db.String(20))


class Event_Organizer(db.Model):
    __tablename__ = 'Event_Organizer'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    company_name = db.Column(db.String(120))
    contact_no = db.Column(db.String(120))
    cr_file = db.Column(db.String(120))
    user_id = db.Column(db.Integer)
    mobile = db.Column(db.String(120))

class Roles(db.Model):
    __tablename__ = 'Roles'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(120))

class Sellers(db.Model):
    __tablename__ = 'Sellers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    national_id = db.Column(db.Integer)
    time_counter = db.Column(db.Time)
    user_id = db.Column(db.Integer)

class Site_Manager(db.Model):
    __tablename__ = 'Site_Manager'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    national_id = db.Column(db.Integer)
    time_counter = db.Column(db.Time)
    user_id = db.Column(db.Integer)

class Countries(db.Model):
    __tablename__ = 'Countries'

    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(120))

class Regions(db.Model):
    __tablename__ = 'Regions'

    region_id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String(120))
    country_id = db.Column(db.Integer)

class Cities(db.Model):
    __tablename__ = 'Cities'

    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(120))
    country_id = db.Column(db.Integer)
    region_id = db.Column(db.Integer)
    Image = db.Column(db.String(120), nullable=True)

class Event(db.Model):
    __tablename__ = 'Event'

    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    num_of_tickets = db.Column(db.Integer)
    country_id = db.Column(db.Integer)
    region_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    location_lang = db.Column(db.Float(50), nullable=True)
    location_lat = db.Column(db.Float(50), nullable=True)
    location_url = db.Column(db.String(500), nullable=True)
    TextLocation = db.Column(db.String(50))
    EventImage = db.Column(db.String(120))
    Summary = db.Column(db.String(6000))
    HaveMoreLikeThis = db.Column(db.Boolean)
    EventTypeID = db.Column(db.Integer)
    MinimumAge = db.Column(db.Integer)
    AudienceTypeID = db.Column(db.Integer)
    GEA_ID = db.Column(db.String(120), nullable=True)

class Event_Days(db.Model):
    __tablename__ = 'Event_Days'

    id = db.Column(db.Integer, primary_key=True)
    event_date = db.Column(db.String(120))
    event_days = db.Column(db.String(120))
    event_id = db.Column(db.Integer)
    event_day_duration = db.Column(db.String(120), nullable=True)
    event_total_duration = db.Column(db.String(120), nullable=True)

class Event_Categories(db.Model):
    __tablename__ = 'Event_Categories'

    category_id = db.Column(db.Integer, primary_key=True)
    supercategory_id = db.Column(db.Integer)
    category_nameEn = db.Column(db.String(120))
    category_nameAr = db.Column(db.String(120))
    category_image = db.Column(db.String(120), nullable=True)
    GEA_Code = db.Column(db.Integer, nullable=True)

class Event_SuperCategories(db.Model):
    __tablename__ = 'Event_SuperCategories'

    supercategory_id = db.Column(db.Integer, primary_key=True)
    category_nameEn = db.Column(db.String(120))
    category_nameAr = db.Column(db.String(120))
    category_image = db.Column(db.String(120), nullable=True)
    GEA_Code = db.Column(db.Integer, nullable=True)

class Event_SubCategories(db.Model):
    __tablename__ = 'Event_SubCategories'

    subcategory_id = db.Column(db.Integer, primary_key=True)
    supercategory_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    category_nameEn = db.Column(db.String(120))
    category_nameAr = db.Column(db.String(120))
    category_image = db.Column(db.String(120), nullable=True)
    GEA_Code = db.Column(db.Integer, nullable=True)

class Event_Categories_Details(db.Model):
    __tablename__ = 'Event_Categories_Details'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    supercategory_id = db.Column(db.Integer)
    subcategory_id = db.Column(db.Integer)
    event_id = db.Column(db.Integer)

class Tickets(db.Model):
    __tablename__ = 'Tickets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float(50))
    event_id = db.Column(db.Integer)
    ticket_type_id = db.Column(db.Integer)
    seats_total_number = db.Column(db.Integer)
    special_note = db.Column(db.String(5000))
    duration = db.Column(db.String(120), nullable=True)
    isHaveSeats = db.Column(db.Boolean)

class Ticket_type(db.Model):
    __tablename__ = 'Ticket_type'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    GEA_ExternalId = db.Column(db.String(50))

class seats(db.Model):
    __tablename__ = 'seats'

    id = db.Column(db.Integer, primary_key=True)
    seat_num = db.Column(db.String(50))

class Services_Log(db.Model):
    __tablename__ = 'Services_Log'

    id = db.Column(db.Integer, primary_key=True)
    Service_Name = db.Column(db.String(120))
    Email = db.Column(db.String(120))
    CreatedAt = db.Column(db.DateTime)
    Channel = db.Column(db.Integer)
    Log_Type = db.Column(db.Integer)
    Json_Req = db.Column(db.String(5000))
    Json_Res = db.Column(db.String(5000))

class Menu(db.Model):
    __tablename__ = 'Menu'

    ID = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(50))
    Role = db.Column(db.Integer)
    IsActive = db.Column(db.Boolean)

class Slider(db.Model):
    __tablename__ = 'Slider'

    ID = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(50))
    Image = db.Column(db.String(120), nullable=True)
    IsActive = db.Column(db.Boolean)
    Role = db.Column(db.Integer)

class Event_FAQs(db.Model):
    __tablename__ = 'Event_FAQs'

    ID = db.Column(db.Integer, primary_key=True)
    EventId = db.Column(db.Integer)
    Question = db.Column(db.String(100))
    Answer = db.Column(db.String(500))

class Event_TermsAndConditions(db.Model):
    __tablename__ = 'Event_TermsAndConditions'

    ID = db.Column(db.Integer, primary_key=True)
    EventId = db.Column(db.Integer)
    Header = db.Column(db.String(100))
    Context = db.Column(db.String(500))

class Users_Tickets(db.Model):
    __tablename__ = 'Users_Tickets'

    ID = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer)
    TicketId = db.Column(db.Integer)
    TicketTypeId = db.Column(db.Integer)
    EventId = db.Column(db.Integer)
    SeatNum = db.Column(db.String(50))
    CreatedAt = db.Column(db.DateTime)
    IsActive = db.Column(db.Boolean)
    QR = db.Column(db.String(1000))
    CheckedIn = db.Column(db.Boolean)
    CheckedInTime = db.Column(db.DateTime)

class Event_Type(db.Model):
    __tablename__ = 'Event_Type'

    ID = db.Column(db.Integer, primary_key=True)
    DescEn = db.Column(db.String(120))
    DescAr = db.Column(db.String(120))

class AudienceType(db.Model):
    __tablename__ = 'AudienceType'

    ID = db.Column(db.Integer, primary_key=True)
    GEA_Code = db.Column(db.Integer, nullable=True)
    DescEn = db.Column(db.String(120))
    DescAr = db.Column(db.String(120))