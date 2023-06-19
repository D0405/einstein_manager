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
    


class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'))
    day = db.Column(db.String(50))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

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