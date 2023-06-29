from . import db  # from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note', backref='user')



class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    birthdate = db.Column(db.Date)
    start_date = db.Column(db.Date)
    max_grade = db.Column(db.Integer)
    hours = db.Column(db.String(10))
    subjects = db.Column(db.String(150))
    availability = db.relationship('Availability', backref='tutor')
    comment = db.Column(db.String(1000))
    street = db.Column(db.String(150))
    plz = db.Column(db.String(10))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(20))
    school_university = db.Column(db.String(150))
    area = db.Column(db.String(150))
    semester = db.Column(db.String(10))
    native_language = db.Column(db.String(150))
    qualification = db.Column(db.String(150))
    previous_training = db.Column(db.String(150))
    previous_training_nr = db.Column(db.String(150))
    wage = db.Column(db.String(150))
    gender = db.Column(db.String(1))
    matches = db.relationship('Match', backref='tutor')


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'birthdate': self.birthdate.isoformat() if self.birthdate else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'max_grade': self.max_grade,
            'hours': self.hours,
            'subjects': self.subjects,
            'comment': self.comment,
            'street': self.street,
            'plz': self.plz,
            'email': self.email,
            'phone': self.phone,
            'school_university': self.school_university,
            'area': self.area,
            'semester': self.semester,
            'native_language': self.native_language,
            'qualification': self.qualification,
            'previous_training': self.previous_training,
            'previous_training_nr': self.previous_training_nr,
            'wage': self.wage,
            'gender': self.gender,

        }

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'))
    day = db.Column(db.String(50))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

class UnavailableTimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def to_dict(self):
        return {
            'id': self.id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None
        }

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    parent_phone = db.Column(db.String(20))
    subjects = db.Column(db.String(150))
    grade = db.Column(db.String(10))
    hours = db.Column(db.String(10))
    school = db.Column(db.String(150))
    days = db.relationship('ChildAvailability', backref='child')
    start_date = db.Column(db.Date)
    comment = db.Column(db.String(1000))
    street = db.Column(db.String(150))
    plz = db.Column(db.String(10))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(20))
    native_language = db.Column(db.String(150))
    geb_datum = db.Column(db.Date)
    geschlecht = db.Column(db.String(1))
    geb_ort = db.Column(db.String(150))
    einreise_deutschland = db.Column(db.String(150))
    herkunftsland_mutter = db.Column(db.String(150))
    herkunftsland_vater = db.Column(db.String(150))
    beruf_mutter = db.Column(db.String(150))
    beruf_vater = db.Column(db.String(150))
    bemerkungen = db.Column(db.String(1000))
    lehrer_name = db.Column(db.String(150))
    lehrer_telefon = db.Column(db.String(20))
    lehrer_email = db.Column(db.String(150))
    zahlung_jc = db.Column(db.Boolean)
    zahlung_wohngeld = db.Column(db.Boolean)
    zahlung_kinderzuschlag = db.Column(db.Boolean)
    zahlung_asylbewerber = db.Column(db.Boolean)
    zahlung_privat = db.Column(db.Boolean)
    bg_nummer = db.Column(db.String(150))
    buT_nummer = db.Column(db.String(150))
    zeitraum = db.Column(db.String(150))
    foerderart = db.Column(db.String(150))
    bewilligte_stunden = db.Column(db.String(150))
    lernort = db.Column(db.String(2))
    unavailable_time_slots = db.relationship('ChildUnavailableTimeSlot', backref='child')


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent_phone': self.parent_phone,
            'subjects': self.subjects,
            'grade': self.grade,
            'hours': self.hours,
            'school': self.school,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'comment': self.comment,
            'street': self.street,
            'plz': self.plz,
            'email': self.email,
            'phone': self.phone,
            'native_language': self.native_language,
            'geb_datum': self.geb_datum.isoformat() if self.geb_datum else None,
            'geschlecht': self.geschlecht,
            'geb_ort': self.geb_ort,
            'einreise_deutschland': self.einreise_deutschland,
            'herkunftsland_mutter': self.herkunftsland_mutter,
            'herkunftsland_vater': self.herkunftsland_vater,
            'beruf_mutter': self.beruf_mutter,
            'beruf_vater': self.beruf_vater,
            'bemerkungen': self.bemerkungen,
            'lehrer_name': self.lehrer_name,
            'lehrer_telefon': self.lehrer_telefon,
            'lehrer_email': self.lehrer_email,
            'zahlung_jc': self.zahlung_jc,
            'zahlung_wohngeld': self.zahlung_wohngeld,
            'zahlung_kinderzuschlag': self.zahlung_kinderzuschlag,
            'zahlung_asylbewerber': self.zahlung_asylbewerber,
            'zahlung_privat': self.zahlung_privat,
            'bg_nummer': self.bg_nummer,
            'buT_nummer': self.buT_nummer,
            'zeitraum': self.zeitraum,
            'foerderart': self.foerderart,
            'bewilligte_stunden': self.bewilligte_stunden,
            'lernort': self.lernort
    }

class ChildUnavailableTimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def to_dict(self):
        return {
            'id': self.id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None
        }





        

class ChildAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    day = db.Column(db.String(50))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

class MatchDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'))
    day = db.Column(db.String(50))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_name = db.Column(db.String(150))
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'))
    child_name = db.Column(db.String(150))
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    days = db.relationship('MatchDay', backref='match')