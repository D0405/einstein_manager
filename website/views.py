from flask import Blueprint, render_template, request, flash, jsonify
from . import db
import json
from .models import Tutor, Availability, Child, ChildAvailability, Note, Match, MatchDay, ChildUnavailableTimeSlot
from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
from flask_login import login_required, current_user



views = Blueprint('views', __name__)
## This is the home page
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")


    return render_template("home.html", user=current_user)


from datetime import datetime

@views.route('/create-lernhelfer', methods=['GET', 'POST'])
def add_tutor():
    if request.method == 'POST':
        name = request.form.get('name')
        birthdate_str = request.form.get('birthdate')
        start_date_str = request.form.get('start_date')
        birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        max_grade = int(request.form.get('max_grade'))
        subjects = request.form.getlist('subjects[]')
        comment = request.form.get('comment')
        street = request.form.get('street')
        plz = request.form.get('plz')
        email = request.form.get('email')
        phone = request.form.get('phone')
        school_university = request.form.get('school_university')
        area = request.form.get('area')
        semester = request.form.get('semester')
        native_language = request.form.get('native_language')
        qualification = request.form.get('qualification')
        previous_training = request.form.get('previous_training')
        wage = request.form.get('wage')
        hours = int(request.form.get('hours'))
        geschlecht = request.form.get('geschlecht')

        availabilities = []

        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
            start_time_str = request.form.get(f"{day}_start_time")
            end_time_str = request.form.get(f"{day}_end_time")

            if start_time_str is not None:
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
            else:
                start_time = None

            if end_time_str is not None:
                end_time = datetime.strptime(end_time_str, '%H:%M').time()
            else:
                end_time = None

            availability = Availability(day=day, start_time=start_time, end_time=end_time)
            availabilities.append(availability)

        if len(name) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif not birthdate:
            flash('Birthdate is required.', category='error')
        elif not start_date:
            flash('Start date is required.', category='error')
        elif not max_grade:
            flash('Max grade is required.', category='error')
        elif not subjects:
            flash('At least one subject must be entered.', category='error')
        elif not comment:
            flash('Comment is required.', category='error')
        else:
            new_tutor = Tutor(
                name=name, birthdate=birthdate, start_date=start_date, max_grade=max_grade, subjects=subjects,
                comment=comment, street=street, plz=plz, email=email, phone=phone,
                school_university=school_university, area=area, semester=semester,
                native_language=native_language, qualification=qualification,
                previous_training=previous_training, wage=wage,
                availability=availabilities, hours=hours
            )

            db.session.add(new_tutor)
            db.session.commit()

            flash('Tutor created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("create_lernhelfer.html", user=current_user, tutor=None)

from datetime import date
from random import randint

@views.route('/create-child', methods=['GET', 'POST'])
def add_child():
    if request.method == 'POST':
        name = request.form.get('name')
        parent_phone = request.form.get('parent_phone')
        subjects = request.form.getlist('subjects[]')
        grade = request.form.get('grade')
        school = request.form.get('school')
        days = request.form.getlist('days[]')

        start_date_str = request.form.get('start_date')
        year, month, day = map(int, start_date_str.split('-'))
        start_date = date(year, month, day)

        comment = request.form.get('comment')
        street = request.form.get('street')
        plz = request.form.get('plz')
        email = request.form.get('email')
        phone = request.form.get('phone')
        hours = request.form.get('hours')
        native_language = request.form.get('native_language')

        availabilities = []

        for day in days:
            start_time_str = request.form.get(f"{day}_start_time")
            end_time_str = request.form.get(f"{day}_end_time")

            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()

            availability = ChildAvailability(day=day, start_time=start_time, end_time=end_time)
            availabilities.append(availability)

        geb_datum_str = request.form.get('geb_datum')
        year, month, day = map(int, geb_datum_str.split('-'))
        geb_datum = date(year, month, day)

        id = randint(0, 999999999)
        geschlecht = request.form.get('geschlecht')
        geb_ort = request.form.get('geb_ort')
        einreise_deutschland = request.form.get('einreise_deutschland')
        herkunftsland_mutter = request.form.get('herkunftsland_mutter')
        herkunftsland_vater = request.form.get('herkunftsland_vater')
        beruf_mutter = request.form.get('beruf_mutter')
        beruf_vater = request.form.get('beruf_vater')
        bemerkungen = request.form.get('bemerkungen')
        lehrer_name = request.form.get('lehrer_name')
        lehrer_telefon = request.form.get('lehrer_telefon')
        lehrer_email = request.form.get('lehrer_email')
        zahlung_jc = bool(request.form.get('zahlung_jc'))
        zahlung_wohngeld = bool(request.form.get('zahlung_wohngeld'))
        zahlung_kinderzuschlag = bool(request.form.get('zahlung_kinderzuschlag'))
        zahlung_asylbewerber = bool(request.form.get('zahlung_asylbewerber'))
        zahlung_privat = bool(request.form.get('zahlung_privat'))
        bg_nummer = request.form.get('bg_nummer')
        buT_nummer = request.form.get('buT_nummer')
        zeitraum = request.form.get('zeitraum')
        foerderart = request.form.get('foerderart')
        bewilligte_stunden = request.form.get('bewilligte_stunden')
        lernort = request.form.get('lernort')

        unavailable_start_dates = request.form.getlist('unavailable_start_date[]')
        unavailable_end_dates = request.form.getlist('unavailable_end_date[]')
        unavailable_notes = request.form.getlist('unavailable_note[]')

        unavailable_time_slots = []

        for start_date, end_date, note in zip(unavailable_start_dates, unavailable_end_dates, unavailable_notes):
            if start_date and end_date and note:
                start_date_str = request.form.get('start_date')
                year, month, day = map(int, start_date_str.split('-'))
                start_date = date(year, month, day)

                year, month, day = map(int, end_date.split('-'))
                end_date_obj = date(year, month, day)

                unavailable_time_slot = ChildUnavailableTimeSlot(start_date=start_date, end_date=end_date_obj, note=note)
                unavailable_time_slots.append(unavailable_time_slot)

        if len(name) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif not parent_phone:
            flash('Parent\'s phone number is required.', category='error')
        elif not subjects:
            flash('At least one subject must be selected.', category='error')
        elif not grade:
            flash('Grade is required.', category='error')
        elif not school:
            flash('School is required.', category='error')
        elif not days:
            flash('At least one day must be selected.', category='error')
        elif not availabilities:
            flash('Please provide the start and end times for the selected days.', category='error')
        else:
            new_child = Child(
                name=name,
                id=id,
                parent_phone=parent_phone,
                subjects=','.join(subjects),
                grade=grade,
                school=school,
                days=availabilities,
                start_date=start_date,
                comment=comment,
                street=street,
                plz=plz,
                email=email,
                phone=phone,
                hours=hours,
                native_language=native_language,
                geb_datum=geb_datum,
                geschlecht=geschlecht,
                geb_ort=geb_ort,
                einreise_deutschland=einreise_deutschland,
                herkunftsland_mutter=herkunftsland_mutter,
                herkunftsland_vater=herkunftsland_vater,
                beruf_mutter=beruf_mutter,
                beruf_vater=beruf_vater,
                bemerkungen=bemerkungen,
                lehrer_name=lehrer_name,
                lehrer_telefon=lehrer_telefon,
                lehrer_email=lehrer_email,
                zahlung_jc=zahlung_jc,
                zahlung_wohngeld=zahlung_wohngeld,
                zahlung_kinderzuschlag=zahlung_kinderzuschlag,
                zahlung_asylbewerber=zahlung_asylbewerber,
                zahlung_privat=zahlung_privat,
                bg_nummer=bg_nummer,
                buT_nummer=buT_nummer,
                zeitraum=zeitraum,
                foerderart=foerderart,
                bewilligte_stunden=bewilligte_stunden,
                lernort=lernort,
                unavailable_time_slots=unavailable_time_slots
            )

            db.session.add(new_child)
            db.session.commit()

            flash('Child created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("create_child.html", user=current_user)

def addFakes():
    from faker import Faker
    from datetime import datetime, timedelta, time, date
    import random


    fake = Faker('de_DE')  # German locale

    # Define subjects
    subjects = ['mathe', 'englisch', 'deutsch']

    # Define days
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

    # Define time range
    start_hour = 16
    end_hour = 18
    start_minute = 30
    end_minute = 30

    # Create 25 tutors
    for _ in range(25):
        tutor_start_hour = start_hour
        tutor_end_hour = end_hour
        tutor_start_minute = start_minute
        tutor_end_minute = end_minute

        num_subjects = random.randint(1, 3)

        tutor = Tutor(
            name=fake.name(),
            birthdate=fake.date_of_birth(minimum_age=18, maximum_age=65),
            start_date=fake.date_between(start_date='-2y', end_date='today'),
            max_grade=random.randint(1, 13),
            hours=random.choice([2, 4, 6]),
            subjects=','.join(random.sample(subjects, num_subjects)),
            availability=[],
            comment=fake.text(),
            street=fake.street_name(),
            plz=fake.postcode(),
            email=fake.email(),
            phone=fake.phone_number(),
            school_university=fake.company(),
            area=fake.city(),
            semester=str(random.randint(1, 10)),
            native_language=fake.language_name(),
            qualification=fake.job(),
            previous_training=fake.job(),
            wage=str(random.randint(10, 50)),
            gender=fake.random_element(['m', 'f']),
        )
        selected_days = random.sample(days, 4)  # Select four random days
        for day in selected_days:
            valid_range = False
            while not valid_range:
                tutor_start_hour = 16#  random.randint(start_hour, end_hour - 1)
                tutor_end_hour =  18 #random.randint(tutor_start_hour + 1, end_hour)

                tutor_start_minute = 30 #random.choice([0, 30])

                if (tutor_end_hour - tutor_start_hour) == 1:
                    tutor_end_minute = 30 #tutor_start_minute
                else:
                    tutor_end_minute = 30 #random.choice([0, 30])

                if tutor_start_hour < tutor_end_hour:
                    valid_range = True

            start_time = time(tutor_start_hour, tutor_start_minute)
            end_time = time(tutor_end_hour, tutor_end_minute)
            availability = Availability(
                day=day,
                start_time=start_time,
                end_time=end_time,
            )
            tutor.availability.append(availability)
        db.session.add(tutor)

    # Create 50 children
    for _ in range(50):
        child_start_hour = start_hour
        child_end_hour = end_hour
        child_start_minute = start_minute
        child_end_minute = end_minute
        num_subjects = random.randint(1, 3)

        child = Child(
            name=fake.first_name() + " " + fake.last_name(),
            parent_phone=fake.phone_number(),
            subjects=','.join(random.sample(subjects, num_subjects)),
            grade=str(random.randint(1, 13)),
            hours=str(random.randint(2, 4)),
            school=fake.company(),
            start_date=fake.date_between(start_date='-2y', end_date='today'),
            comment=fake.text(),
            street=fake.street_name(),
            plz=fake.postcode(),
            email=fake.email(),
            phone=fake.phone_number(),
            native_language=fake.language_name(),
            geb_datum=fake.date_of_birth(minimum_age=6, maximum_age=18),
            geschlecht=fake.random_element(['m', 'f']),
            geb_ort=fake.city(),
            einreise_deutschland=fake.country(),
            herkunftsland_mutter=fake.country(),
            herkunftsland_vater=fake.country(),
            beruf_mutter=fake.job(),
            beruf_vater=fake.job(),
            bemerkungen=fake.text(),
            lehrer_name=fake.name(),
            lehrer_telefon=fake.phone_number(),
            lehrer_email=fake.email(),
            zahlung_jc=fake.boolean(),
            zahlung_wohngeld=fake.boolean(),
            zahlung_kinderzuschlag=fake.boolean(),
            zahlung_asylbewerber=fake.boolean(),
            zahlung_privat=fake.boolean(),
            bg_nummer=fake.random_number(digits=10),
            buT_nummer=fake.random_number(digits=10),
            zeitraum=fake.month(),
            foerderart=fake.random_element(['A', 'B', 'C']),
            bewilligte_stunden=str(random.randint(2, 4)),
            lernort=fake.random_element(['H', 'S']),
            unavailable_time_slots=[],
        )
        selected_days = random.sample(days, 3)  # Select three random days
        for day in selected_days:
            valid_range = False
            while not valid_range:
                child_start_hour = 16 #random.randint(start_hour, end_hour - 1)
                child_end_hour = 18 #random.randint(child_start_hour + 1, end_hour)

                child_start_minute = 30 #random.choice([0, 30])
                if (child_end_hour - child_start_hour) == 1:
                    child_end_minute = child_start_minute
                else:
                    child_end_minute = 30 # random.choice([0, 30])

                if child_start_hour < child_end_hour:
                    valid_range = True

            start_time = time(child_start_hour, child_start_minute)
            end_time = time(child_end_hour, child_end_minute)
            availability = ChildAvailability(
                day=day,
                start_time=start_time,
                end_time=end_time,
            )
            child.days.append(availability)
        db.session.add(child)

    db.session.commit()


def get_tutor_name_by_id(tutor_id):
    tutor = Tutor.query.get(tutor_id)
    return tutor.name

def get_child_name_by_id(child_id):
    child = Child.query.get(child_id)
    return child.name

def time_overlap(start_time1, end_time1, start_time2, end_time2):
    # Wenn ein Zeitraum vor dem anderen endet, gibt es keine Überschneidung
    return end_time1 >= start_time2 and end_time2 >= start_time1

from datetime import datetime, date, time, timedelta
from datetime import datetime, timedelta
from collections import defaultdict
from flask import render_template

def print_matches():
    # SQLAlchemy Session 

    # Holen Sie sich alle Matches.
    all_matches = db.session.query(Match).all()

    tutor_to_children = {}
    child_to_appointments = {}
    all_children = set(db.session.query(Child).all())
    matched_children = set()

    for match in all_matches:
        tutor = db.session.query(Tutor).get(match.tutor_id)
        child = db.session.query(Child).get(match.child_id)
        days = db.session.query(MatchDay).filter(MatchDay.match_id == match.id).all()

        print(f"Tutor {tutor.name} wurde dem Schüler {child.name} zugeordnet.")
        print(f"Sie treffen sich an folgenden Tagen:")
        for day in days:
            print(f"- {day.day.capitalize()}: von {day.start_time} bis {day.end_time} mit ID {day.id}")
        print()

        if tutor.name in tutor_to_children:
            tutor_to_children[tutor.name].append(child.name)
        else:
            tutor_to_children[tutor.name] = [child.name]

        if child.name in child_to_appointments:
            child_to_appointments[child.name] += len(days)
        else:
            child_to_appointments[child.name] = len(days)

        matched_children.add(child)

    print(f"Zusammenfassung:")
    for tutor, children in tutor_to_children.items():
        print(f"Tutor {tutor} hat {len(children)} Schüler: {', '.join(children)}")
    print()

    print(f"Termine pro Schüler:")
    for child, appointments in child_to_appointments.items():
        print(f"Schüler {child} hat {appointments} Termine.")
    print()

    unmatched_children = all_children - matched_children
    if unmatched_children:
        print(f"Schüler ohne Termin:")
        for child in unmatched_children:
            print(f"{child.name} ist verfügbar an:")
            for day in db.session.query(ChildAvailability).filter(ChildAvailability.child_id == child.id):
                print(f"- {day.day.capitalize()}: von {day.start_time} bis {day.end_time}")
            print()
    else:
        print("Alle Schüler haben Termine.")


from collections import defaultdict
from collections import defaultdict

# ...

from datetime import datetime, time, timedelta

import colorsys

def get_n_hues(n):
    return [colorsys.hsv_to_rgb(i/n, 0.5, 0.95) for i in range(n)]

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))






#Schüler und Lernhelfer haben angegeben an welchen Tagen diese können und wie viele Wochenstunden Sie haben. Es sollen möglichst alle möglichen Wochenstunden (hours) der schüler genutzt werden. Ein Schüler kann pro Tag nur einen Termin haben. Im besten Fall ist der Schüler einem Lernhelfer zugeordnet der an zwei (für beide verfügbare Tage) einen einstündigen termin mit dem Schüler hat. Pro stunde kann ein Lernhelfer nur einen schüler haben. Es ist außerdem angegeben was die Stufe des Schülers und die maximale Stufe des Lernhelfers ist. Dies muss auch passen. Erstelle einen Algorithmus der die Schüler mit lernhelfern zusammenführt. Es soll angestrebt werden, dass jeder Lernhelfer 2 Schüler am tag hat. Ein match kann an einem eine stunde gehen.jeder schüler darf maximal einen Termin pro tag haben. Zwischen start und endzeit soll eine stunde liegen. Außerdem ist es ok wenn ein Termin von 16:30-17:30 geht und der nächste von 17:30-18:30
#TODO  PAsse den Algorithmus an: Es soll zunähst eine Liste mit 2er Paaren von Schülern erstellt werden, die an den gleichen Tagen können. Anschließend soll für jedes Paar ein Lernhelfer gefunden werden, der die beiden betreuen kann. Beide schüler kriegen dann jeweils einen 1h Termin an dem Tag:
import uuid

# #@views.route('/match-tutor-child')
# @views.route('/match-random')
# def match_tutor_child():

#     MatchDay.query.delete()
#     Match.query.delete()
#     db.session.commit()

#     all_children = db.session.query(Child).all()
#     all_tutors = db.session.query(Tutor).all()

#     tutor_day_counts = defaultdict(lambda: defaultdict(int))
#     child_day_counts = defaultdict(lambda: defaultdict(int))
#     tutor_time_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
#     tutor_total_hours = defaultdict(int)  # Add a count for total tutor hours
#     child_total_hours = defaultdict(int)  # Add a count for total child hours
#     matchId = 0

#     single_slot_tutors = set()

#     for child in all_children:
#         # Sortiere Tutoren nach Anzahl der Tage, an denen sie bisher Termine haben
#         all_tutors = sorted(all_tutors, key=lambda x: (x.id in single_slot_tutors, len(set(tutor_day_counts[x.id].values()))))

#         for tutor in all_tutors:
#             if tutor.max_grade < int(child.grade) or tutor_total_hours[tutor.id] >= int(tutor.hours) or child_total_hours[child.id] >= int(child.hours):
#                 continue

#             child_availability = db.session.query(ChildAvailability).filter(ChildAvailability.child_id == child.id).all()
#             tutor_availability = db.session.query(Availability).filter(Availability.tutor_id == tutor.id).all()

#             matched_availability = []
                
                
                
#             for t_availability in tutor_availability:
#                 for c_availability in child_availability:
#                     if c_availability.day == t_availability.day and \
#                         c_availability.start_time <= t_availability.start_time and \
#                         c_availability.end_time >= t_availability.end_time:

#                         current_start_time = max(c_availability.start_time, t_availability.start_time)
#                         while current_start_time < t_availability.end_time and child_total_hours[child.id] < int(child.hours):
#                             if tutor_day_counts[tutor.id][c_availability.day] < 2 and \
#                                 child_day_counts[child.id][c_availability.day] < 1 and \
#                                 tutor_time_counts[tutor.id][c_availability.day][current_start_time] < 1:

#                                 end_time = (datetime.combine(date.today(), current_start_time) + timedelta(hours=1)).time()  

#                                 matched_availability.append({
#                                     'day': c_availability.day,
#                                     'start_time': current_start_time,
#                                     'end_time': end_time
#                                 })

#                                 tutor_time_counts[tutor.id][c_availability.day][current_start_time] += 1
#                                 tutor_day_counts[tutor.id][c_availability.day] += 1
#                                 child_day_counts[child.id][c_availability.day] += 1
#                                 tutor_total_hours[tutor.id] += 1  # Increase the total tutor hours
#                                 child_total_hours[child.id] += 1  # Increase the total child hours

#                                 if len(matched_availability) >= int(child.hours):
#                                     break

#                             current_start_time = (datetime.combine(date.today(), current_start_time) + timedelta(hours=1)).time()

#                     if len(matched_availability) >= int(child.hours):
#                         break

#             if len(matched_availability) >= int(child.hours):
#                 match = Match(id = matchId ,tutor_id=tutor.id, tutor_name = tutor.name, child_name=child.name, child_id=child.id)
#                 db.session.add(match)
#                 db.session.commit()

#                 for availability in matched_availability:
#                     match_day = MatchDay(
#                         match_id=matchId, 
#                         day=availability['day'], 
#                         start_time=availability['start_time'], 
#                         end_time=availability['end_time']
#                     )
#                     db.session.add(match_day)
#                     db.session.commit()

#                 # If tutor has only one slot, add to the single_slot_tutors set
#                 if tutor_day_counts[tutor.id] == 1:
#                     single_slot_tutors.add(tutor.id)
#                 else:
#                     single_slot_tutors.discard(tutor.id)

#                 matchId = matchId + 1


#     matches_list = []
#     matches = db.session.query(Match).all()
#     for match in matches:
#         match_days = db.session.query(MatchDay).filter(MatchDay.match_id == match.id).all()
#         for match_day in match_days:
#             matches_list.append({
#                 'id': match.id,
#                 'tutor_id': match.tutor_id,
#                 'child_id': match.child_id,
#                 'day': match_day.day,
#                 'start_time': match_day.start_time,
#                 'end_time': match_day.end_time
#             })

#     tutor_colors = dict(zip([tutor.id for tutor in all_tutors], map(rgb_to_hex, get_n_hues(len(all_tutors)))))

#     current_week = date.today().isocalendar()[1]

#     print_matches()
#     return redirect(url_for('views.show_matches'))
#    # return render_template("match_tutor_child.html", matches=matches_list, user=current_user, get_tutor_name_by_id=get_tutor_name_by_id, get_child_name_by_id=get_child_name_by_id, tutor_colors=tutor_colors, current_week=current_week)

def time_overlaps(time1_start, time1_end, time2_start, time2_end):
    # Check if two time periods overlap
    return time1_start <= time2_end and time2_start <= time1_end


# Convert availability of children and tutors to dictionary
def get_availability_as_dict(availabilities):
    availability_dict = {}
    for availability in availabilities:
        if availability.day not in availability_dict:
            availability_dict[availability.day] = []
        availability_dict[availability.day].append(availability)
    return availability_dict


def count_appointments(day):
    return MatchDay.query.filter_by(day=day).count()

from itertools import combinations
from datetime import datetime, date, timedelta

@views.route('/match-random')
def match_tutor_child(class_relevance = False):

    class_relevance = True



    MatchDay.query.delete()
    Match.query.delete()
    db.session.commit()

    all_children = db.session.query(Child).all()
    all_tutors = db.session.query(Tutor).all()

    child_combinations = combinations(all_children, 2)

    matched_children = set()
    matched_tutors = set()
    matchId = 0

    # Find pairs of children
    for combo in child_combinations:
        # Extract child1 and child2 from each combination
        child1, child2 = combo

        if child1.id in matched_children or child2.id in matched_children:
            continue

        child1_availability_dict = get_availability_as_dict(child1.days)
        child2_availability_dict = get_availability_as_dict(child2.days)

        # Get the availability days for each child
        child1_days = set(child1_availability_dict.keys())
        child2_days = set(child2_availability_dict.keys())



        # Check if there are at least two days where both children are available
        common_days = child1_days & child2_days


        if len(common_days) < 2:
            continue

        combo_has_tutor = False
        for tutor in all_tutors:
            if tutor.id in matched_tutors:
                continue

            if class_relevance:
                # Check if the tutor can teach the grade level of the children
                if tutor.max_grade < int(child1.grade) or tutor.max_grade < int(child2.grade):
                    continue
                # Check if the children are in the same grade
                if abs(int(child1.grade) - int(child2.grade)) > 2:
                    continue

            if combo_has_tutor: # If the tutor is already matched to this pair of children
                continue


            tutor_availability_dict = get_availability_as_dict(tutor.availability)

            tutor_availability = set(tutor_availability_dict.keys())

            # Use this function to convert the children and tutor availability to dictionary

            tutor_availability_dict = get_availability_as_dict(tutor.availability)

            # check if the tutor is available on the common days
            if not all(day in tutor_availability for day in common_days):
                continue

            # Check if the tutor's available time overlaps with the children's available time on the common days
            if not all(any(time_overlaps(c1_av.start_time, c1_av.end_time, tutor_availability_dict[day][i].start_time, tutor_availability_dict[day][i].end_time) and
                        time_overlaps(c2_av.start_time, c2_av.end_time, tutor_availability_dict[day][i].start_time, tutor_availability_dict[day][i].end_time)
                        for i in range(len(tutor_availability_dict[day])) for c1_av in child1_availability_dict[day] for c2_av in child2_availability_dict[day])
                        for day in common_days):
                            continue

            match1 = Match(id=matchId, tutor_name = tutor.name, tutor_id=tutor.id, child_name = child1.name, child_id=child1.id)
            matchId = matchId + 1
            match2 = Match(id=matchId, tutor_name = tutor.name, tutor_id=tutor.id, child_name = child2.name, child_id=child2.id)
            matchId = matchId + 1
            db.session.add(match1)
            db.session.add(match2)

            # If so, match these children together and assign the tutor
            matched_children.add(child1.id)
            matched_children.add(child2.id)
            matched_tutors.add(tutor.id)

            common_days = sorted(common_days, key=count_appointments)



            # Loop over common days and create match days
            appointments_made = 0
            for day in common_days:
                # If we've already made 2 appointments, we can stop
                if appointments_made >= 2:
                    break                # Filter the availability for this specific day
                tutor_availability_day = [av for av in tutor.availability if av.day == day]
                child1_availability_day = [av for av in child1.days if av.day == day]
                child2_availability_day = [av for av in child2.days if av.day == day]

                one_hour = timedelta(hours=1)
                
                for tutor_av in tutor_availability_day:
                    for child1_av in child1_availability_day:
                        for child2_av in child2_availability_day:
                            if time_overlaps(child1_av.start_time, child1_av.end_time, tutor_av.start_time, tutor_av.end_time) and \
                                time_overlaps(child2_av.start_time, child2_av.end_time, tutor_av.start_time, tutor_av.end_time):
                                    # Subtract 1 hour from the end time
                                    end_time = (datetime.combine(date(1,1,1), tutor_av.end_time) - one_hour).time()

                                    match_day1 = MatchDay(match_id=match1.id, day=day, start_time=tutor_av.start_time, end_time=end_time)
                                    db.session.add(match_day1)

                                    start_time = (datetime.combine(date(1,1,1), tutor_av.start_time) + one_hour).time()
                                    match_day2 = MatchDay(match_id=match2.id, day=day, start_time=start_time, end_time=tutor_av.end_time)
                                    db.session.add(match_day2)
                                    print(f"{tutor.name} is tutoring {child1.name} from {match_day1.start_time} to {match_day1.end_time} and {child2.name} from {match_day2.start_time} to {match_day2.end_time} on {day} from {tutor_av.start_time} to {tutor_av.end_time}")
                                    combo_has_tutor = True
                                    appointments_made += 1
                                    break
    # db.session.commit()

    unmatched_children = [child for child in all_children if child.id not in matched_children]
    for child in unmatched_children:
        print(f"{child.name} has not been matched.")

    unmatched_tutors = [tutor for tutor in all_tutors if tutor.id not in matched_tutors]
    for tutor in unmatched_tutors:
        print(f"{tutor.name} has not been assigned a pair.")
    #################

    db.session.commit()


    #print_matches()
    print("TEST")
    return redirect(url_for('views.show_matches'))
   # return render_template("match_tutor_child.html", matches=matches_list, user=current_user, get_tutor_name_by_id=get_tutor_name_by_id, get_child_name_by_id=get_child_name_by_id, tutor_colors=tutor_colors, current_week=current_week)



@views.route('/show-matches')
@login_required
def show_matches():
    matches_list = []
    matches = db.session.query(Match).all()
    print("TES33T")
    for match in matches:
        match_days = db.session.query(MatchDay).filter(MatchDay.match_id == match.id).all()
        for match_day in match_days:
            matches_list.append({
                'id': match.id,
                'tutor_id': match.tutor_id,
                'child_id': match.child_id,
                'day': match_day.day,
                'start_time': match_day.start_time,
                'end_time': match_day.end_time
            })

    all_tutors = db.session.query(Tutor).all()
    tutor_colors = dict(zip([tutor.id for tutor in all_tutors], map(rgb_to_hex, get_n_hues(len(all_tutors)))))

    current_week = date.today().isocalendar()[1]

    return render_template("show_matches.html", matches=matches_list, user=current_user, get_tutor_name_by_id=get_tutor_name_by_id, get_child_name_by_id=get_child_name_by_id, tutor_colors=tutor_colors, current_week=current_week)


@views.route('/list-childreen')
def list_childreen():

    #addFakes()
    



    childreen = Child.query.all()
    return render_template("list_childreen.html", childreen=childreen, user=current_user)



# Mache die Funktion im Jinja-Umfeld verfügbar
@views.app_context_processor
def inject_tutor_has_availability():
    return dict(tutor_has_availability=tutor_has_availability)


@views.route('/list-tutors')
def list_tutors():
    tutors = Tutor.query.all()

    #print_tutors()
    return render_template('list_tutors.html', tutors=tutors, user=current_user)




@views.route('/list-matches')
def list_matches():
    matches = Match.query.all()
    tutors = Tutor.query.all()
    children = Child.query.all()

    return render_template('list_matches.html', matches=matches, tutors=tutors, children=children, user=current_user)



from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class EditMatchForm(FlaskForm):
    tutor_name = StringField('Tutor Name', validators=[DataRequired()])
    child_name = StringField('Child Name', validators=[DataRequired()])
    duration = IntegerField('Duration', validators=[DataRequired(), NumberRange(min=1, max=5)])
    # Weitere Felder für die Bearbeitung des Matches


from flask_login import current_user

from sqlalchemy import and_
from datetime import datetime



def match_has_day(match, day):
    # Überprüfen, ob ein bestimmter Match an einem bestimmten Tag stattfindet
    return any(match_day.day == day for match_day in match.days)

def get_match_time(match, day, time_type):
    for match_day in match.days:
        if match_day.day == day:
            if time_type == 'start_time':
                return match_day.start_time
            elif time_type == 'end_time':
                return match_day.end_time
    return None

def get_child_time(child, day, time_type):
    for match_day in child.days:
        if match_day.day == day:
            if time_type == 'start_time':
                return match_day.start_time
            elif time_type == 'end_time':
                return match_day.end_time
    return None

def get_tutor_time(tutor, day, time_type):
    for match_day in tutor.availability:
        if match_day.day == day:
            if time_type == 'start_time':
                return match_day.start_time
            elif time_type == 'end_time':
                return match_day.end_time
    return None

from sqlalchemy import and_
@views.route('/edit-match/<int:match_id>', methods=['GET', 'POST'])
@login_required
def edit_match(match_id):
    match = Match.query.get_or_404(match_id)

    if request.method == 'POST':
        checked_days = request.form.getlist('days[]')

        # delete match days for unchecked days
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
            if day not in checked_days:
                match_day = MatchDay.query.filter(and_(MatchDay.match_id == match.id, MatchDay.day == day)).first()
                if match_day:
                    db.session.delete(match_day)

        # update or add match days for checked days
        for day in checked_days:
            start_time_str = request.form.get(f'{day}_start_time')
            end_time_str = request.form.get(f'{day}_end_time')

            match_day = MatchDay.query.filter(and_(MatchDay.match_id == match.id, MatchDay.day == day)).first()
            if start_time_str and end_time_str:

                start_time_str = start_time_str[:5]
                end_time_str = end_time_str[:5]

                print("start_time_str:", start_time_str)
                print("end_time_str:", end_time_str)

                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()

                if match_day:
                    match_day.start_time = start_time
                    match_day.end_time = end_time
                else:
                    match_day = MatchDay(match_id=match.id, day=day, start_time=start_time, end_time=end_time)
                    db.session.add(match_day)

        match.tutor_name = request.form.get('tutor_name')
        tutor = Tutor.query.filter_by(name=match.tutor_name).first()
        if tutor:
            match.tutor_id = tutor.id



        match.child_name = request.form.get('child_name')
        child = Child.query.filter_by(name=match.child_name).first()
        if child:
            match.child_id = child.id
            db.session.commit()

        flash('Match updated!', category='success')
        return redirect(url_for('views.list_matches'))

    tutor = Tutor.query.get(match.tutor_id)
    child = Child.query.get(match.child_id)

    # Aktualisierte Match-Days aus dem Formular lesen
    match_days = {}
    for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
        start_time = request.form.get(f'{day}_start_time')
        end_time = request.form.get(f'{day}_end_time')
        if start_time and end_time:
            match_days[day] = {'start_time': start_time, 'end_time': end_time}
        
    tutors = Tutor.query.all()
    children = Child.query.all()


    return render_template('edit_match.html', children=children, tutors =tutors, match=match, user=current_user, match_has_day=match_has_day, match_days=match_days, get_match_time=get_match_time)
    
from sqlalchemy import and_, func

from sqlalchemy import and_, func

@views.route('/get-availability')
def getAvailability():
    tutor_id = request.args.get('tutor_id')
    # Hier musst du den Code schreiben, um die verfügbaren Schüler für den ausgewählten Tutor abzurufen.
    # Du kannst eine Datenbankabfrage oder eine andere Logik verwenden, um die verfügbaren Schüler basierend auf der Tutor-Verfügbarkeit zu ermitteln.
    # Die Funktion sollte eine Liste von Schüler-IDs zurückgeben, die zur gleichen Zeit wie der ausgewählte Tutor verfügbar sind.
    # Hier ist ein fiktives Beispiel, wie die Funktion aussehen könnte:
    
    tutor = Tutor.query.filter_by(id=tutor_id).first()
    if not tutor:
        return []  # Kein Tutor mit dieser ID gefunden
    
    # Beispiel: Holen der verfügbaren Schüler basierend auf der Tutor-Verfügbarkeit
    available_children = []
    
    # Annahme: Du hast eine Tabelle "Availability" mit Tutor-IDs und Schüler-IDs, um die Verfügbarkeit zu verfolgen
    availabilities = Availability.query.filter_by(tutor_id=tutor.id).all()
    
    for availability in availabilities:
        # Füge die Schüler-IDs zur Liste der verfügbaren Schüler hinzu
        available_children.append(availability.child_id)
    
    return [] #available_children


@views.route('/get-tutors') 
def getTutors():
    child_id = request.args.get('child_id')
    # Hier musst du den Code schreiben, um die verfügbaren Tutoren für den ausgewählten Schüler abzurufen.
    # Du kannst eine Datenbankabfrage oder eine andere Logik verwenden, um die verfügbaren Tutoren basierend auf der Schülerverfügbarkeit zu ermitteln.
    # Die Funktion sollte eine Liste von Tutor-IDs zurückgeben, die zur gleichen Zeit wie der ausgewählte Schüler verfügbar sind.
    # Hier ist ein fiktives Beispiel, wie die Funktion aussehen könnte:
    
    child = Child.query.filter_by(id=child_id).first()
    if not child:
        return []  # Kein Schüler mit dieser ID gefunden
    
    # Beispiel: Holen der verfügbaren Tutoren basierend auf der Schülerverfügbarkeit
    available_tutors = []
    
    # Annahme: Du hast eine Tabelle "Availability" mit Tutor-IDs und Schüler-IDs, um die Verfügbarkeit zu verfolgen
    availabilities = Availability.query.filter_by(child_id=child.id).all()
    
    for availability in availabilities:
        # Füge die Tutor-IDs zur Liste der verfügbaren Tutoren hinzu
        available_tutors.append(availability.tutor_id)
    
    return [] #available_tutors



def findTutorsForChild(child_id, tutors):
    #Filter die Tutoren, die zeitlich nicht zum Schüler passen
    child = Child.query.get(child_id)
    if child:
            print("TEST")
            # Liste der verfügbaren Tutoren
            available_tutors = []
            for tutor in tutors:
                # Prüfen Sie jede Verfügbarkeit des Tutors und des Kindes
                for tutor_availability in tutor.availability:
                    for child_availability in child.days:
                        if tutor in available_tutors:
                            break
                        # Wenn der Wochentag und die Zeiten übereinstimmen, fügen Sie den Tutor der Liste hinzu
                        if tutor_availability.day == child_availability.day and \
                                tutor_availability.start_time <= child_availability.start_time and \
                                tutor_availability.end_time >= child_availability.end_time:
                            print(tutor.name)
                            possibleSlots = findPossibleTimeSlots(child_id, tutor.id)
                            if any(childSlots and tutorSlots for day, childSlots, tutorSlots in possibleSlots):
                                available_tutors.append(tutor)                              
                                break
            print(len(available_tutors))
            return available_tutors
    



def findPossibleTimeSlots(child_id, tutor_id):
    # Holen des Child-Objekts
    child = Child.query.get(child_id)
    if not child:
        print(f"Child with ID {child_id} does not exist.")
        return None
    
    # Holen des Tutor-Objekts
    tutor = Tutor.query.get(tutor_id)
    if not tutor:
        print(f"Tutor with ID {tutor_id} does not exist.")
        return None
    
    # Holen der verfügbaren Tage des Schülers
    child_days = set([availability.day for availability in child.days])
    
    # Holen der verfügbaren Tage des Tutors
    tutor_days = set([availability.day for availability in tutor.availability])
    
    # Gemeinsame verfügbare Tage ermitteln
    available_days = child_days.intersection(tutor_days)
    
    # Holen aller Matches für child_id oder tutor_id
    matches = Match.query.filter((Match.child_id == child_id) | (Match.tutor_id == tutor_id)).all()
    
    available_slots = []
    
    for day in available_days:
        child_slots = []
        tutor_slots = []
        
        # Schüler-Zeitfenster durchlaufen
        for availability in child.days:
            if availability.day == day:
                start_time = availability.start_time
                end_time = availability.end_time
                child_slots.append((start_time, end_time))
        
        # Tutor-Zeitfenster durchlaufen
        for availability in tutor.availability:
            if availability.day == day:
                start_time = availability.start_time
                end_time = availability.end_time
                tutor_slots.append((start_time, end_time))
        
        # Überprüfen auf Überschneidungen mit bereits eingeplanten Matches
        for match in matches:
            match_days = MatchDay.query.filter_by(match_id=match.id, day=day).all()
            for match_day in match_days:
                match_start_time = match_day.start_time
                match_end_time = match_day.end_time
                
                # Überprüfen auf Überschneidungen mit Schüler-Zeitfenstern
                for slot in child_slots[:]:
                    if doTimeSlotsOverlap(slot[0], slot[1], match_start_time, match_end_time):
                        child_slots.remove(slot)
                
                # Überprüfen auf Überschneidungen mit Tutor-Zeitfenstern
                for slot in tutor_slots[:]:
                    if doTimeSlotsOverlap(slot[0], slot[1], match_start_time, match_end_time):
                        tutor_slots.remove(slot)
        
        if child_slots and tutor_slots:
            available_slots.append((day, child_slots, tutor_slots))
    
    print(available_slots)
    return available_slots



def doTimeSlotsOverlap(start_time1, end_time1, start_time2, end_time2):
    return start_time1 <= end_time2 and start_time2 <= end_time1






@views.route('/create-match', methods=['GET', 'POST'])
@login_required
def create_match():
    if request.method == 'POST':
        print("TEST")
        checked_days = request.form.getlist('days[]')

        # Erstelle neues Match
        tutor_id = request.form.get('tutor_name')  # Hier den richtigen Namen des Formularfelds verwenden
        tutor = Tutor.query.filter_by(id=tutor_id).first()
        if not tutor:
            flash('Tutor does not exist!', category='error')
            return redirect(url_for('views.create_match'))
        child_id = request.form.get('child_name')  # Hier den richtigen Namen des Formularfelds verwenden
        child = Child.query.filter_by(id=child_id).first()
        if not child:
            flash('Child does not exist!', category='error')
            return redirect(url_for('views.create_match'))

        max_match_id = db.session.query(func.max(Match.id)).scalar()
        new_match_id = max_match_id + 1 if max_match_id else 1

        match = Match(
            id=new_match_id,
            tutor_id=tutor.id,
            tutor_name=tutor.name,
            child_id=child.id,
            child_name=child.name
        )
        db.session.add(match)

        # Füge Match-Days für ausgewählte Tage hinzu
        for day in checked_days:
            start_time_str = request.form.get(f'{day}_start_time')
            end_time_str = request.form.get(f'{day}_end_time')

            if start_time_str and end_time_str:
                start_time_str = start_time_str[:5]
                end_time_str = end_time_str[:5]
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()

                match_day = MatchDay(
                    match_id=match.id,
                    day=day,
                    start_time=start_time,
                    end_time=end_time
                )
                db.session.add(match_day)

        db.session.commit()

        flash('Match created!', category='success')
        return redirect(url_for('views.list_matches'))

    show_only_students_without_tutor = request.args.get('show_only_students_without_tutor') == 'true'
    show_only_tutors_without_schedule = request.args.get('show_only_tutors_without_schedule') == 'true'

    tutor_id = request.args.get('tutor_id')
    if tutor_id is not None:
        try:
            tutor_id = int(tutor_id)
        except ValueError:
            tutor_id = None
    child_id = request.args.get('child_id')
    if child_id is not None:
        try:
            child_id = int(child_id)
        except ValueError:
            child_id = None    

    tutors = Tutor.query.all()
    children = Child.query.all()
    matches = Match.query.all()


    possibleTimes = {} 
    print("TEST")

    if child_id and tutor_id: # 
        possibleTimes = findPossibleTimeSlots(child_id, tutor_id)
        print(possibleTimes)
    #Tutoren finden die zu Schüler passen würde
    elif child_id:
        tutors = findTutorsForChild(child_id, tutors)
    elif tutor_id:
        print("TODO")


    matched_child_ids = set(match.child_id for match in matches)
    children_without_tutor = [child for child in children if child.id not in matched_child_ids]
    children_without_tutor = [child.to_dict() for child in children_without_tutor]

    if show_only_students_without_tutor:
        children_to_show = children_without_tutor
    else:
        children_to_show = [child.to_dict() for child in children]

    matched_tutor_ids = set(match.tutor_id for match in matches)
    tutors_to_show = []

    for tutor in tutors:
        tutor_dict = tutor.to_dict()
        tutor_dict['weekly_hours'] = sum(1 for match in matches if match.tutor_id == tutor.id for match_day in match.days)
        tutors_to_show.append(tutor_dict)

    if show_only_tutors_without_schedule:
        tutors_to_show = [tutor for tutor in tutors_to_show if tutor['weekly_hours'] == 0]


    return render_template('create_match.html', tutors=tutors_to_show, children=children_to_show, user=current_user, show_only_students_without_tutor=show_only_students_without_tutor,
        show_only_tutors_without_schedule=show_only_tutors_without_schedule, tutor_id=tutor_id, child_id=child_id, possibleTimes=possibleTimes)




# @views.route('/edit-match/<int:match_id>', methods=['GET', 'POST'])
# @login_required
# def edit_match(match_id):
#     match = Match.query.get_or_404(match_id)

#     if request.method == 'POST':
#         # Aktualisiere die Match-Daten
#         match.tutor_id = int(request.form.get('tutor_id'))
#         match.child_id = int(request.form.get('child_id'))

#         # Aktualisiere die MatchDay-Daten
#         days = request.form.getlist('days[]')
#         start_times = request.form.getlist('start_times[]')
#         end_times = request.form.getlist('end_times[]')

#         # Lösche vorhandene MatchDay-Einträge
#         MatchDay.query.filter_by(match_id=match.id).delete()

#         # Erstelle und füge neue MatchDay-Einträge hinzu
#         for i in range(len(days)):
#             day = days[i]
#             start_time_str = start_times[i]
#             end_time_str = end_times[i]

#             start_time = datetime.strptime(start_time_str, '%H:%M').time()
#             end_time = datetime.strptime(end_time_str, '%H:%M').time()

#             match_day = MatchDay(match_id=match.id, day=day, start_time=start_time, end_time=end_time, )
#             db.session.add(match_day)

#         # Speichere die Änderungen in der Datenbank
#         db.session.commit()

#         flash('Match aktualisiert!', category='success')
#         return redirect(url_for('views.list_matches'))

#     # Abrufen der Daten für die Dropdown-Liste der Tutoren und Kinder
#     tutor = Tutor.query.get(match.tutor_id)
#     child = Child.query.get(match.child_id)

#     tutor_availabilities = {a.day: {'start_time': str(a.start_time), 'end_time': str(a.end_time)} for a in tutor.availability}
#     child_availabilities = {a.day: {'start_time': str(a.start_time), 'end_time': str(a.end_time)} for a in child.days}
        

#     return render_template('edit_match.html', match=match, tutor_availabilities=tutor_availabilities, child_availabilities=child_availabilities, user=current_user, match_has_day=match_has_day)



# Route zum Drucken der Schülerdaten
@views.route('/print_tutors')
def print_tutors():
    tutors = Tutor.query.all()  # Alle Tutor-Datensätze abrufen

    for tutor in tutors:
        if tutor:
            print(f"Tutor ID: {tutor.id}")
            print(f"Name: {tutor.name}")
            print(f"Geburtsdatum: {tutor.birthdate}")
            print(f"Startdatum: {tutor.start_date}")
            print(f"Maximale Klasse: {tutor.max_grade}")
            print(f"Wochenstunden: {tutor.hours}")
            print(f"Fächer: {tutor.subjects}")
            print(f"Kommentar: {tutor.comment}")
            print(f"Straße: {tutor.street}")
            print(f"PLZ: {tutor.plz}")
            print(f"E-Mail: {tutor.email}")
            print(f"Telefonnummer: {tutor.phone}")
            print(f"Schule/Universität: {tutor.school_university}")
            print(f"Bereich: {tutor.area}")
            print(f"Semester: {tutor.semester}")
            print(f"Muttersprache: {tutor.native_language}")
            print(f"Qualifikation: {tutor.qualification}")
            print(f"Vorherige Ausbildung: {tutor.previous_training}")
            print(f"Stundenlohn: {tutor.wage}")
            
            print("Verfügbarkeiten:")
            availabilities = Availability.query.filter_by(tutor_id=tutor.id).all()
            for availability in availabilities:
                print(f"Tag: {availability.day}")
                print(f"Startzeit: {availability.start_time}")
                print(f"Endzeit: {availability.end_time}")
                print("------------")
        else:
            print("Tutor nicht gefunden.")

    return "Tutors printed"  # Optional: Rückgabe einer Erfolgsmeldung


# Definiere die Funktion tutor_has_availability
def tutor_has_availability(tutor, day):
    availability = Availability.query.filter_by(tutor_id=tutor.id, day=day).first()
    return availability is not None

def get_availability_time(tutor, day, time_type):
    availability = Availability.query.filter_by(tutor_id=tutor.id, day=day).first()
    if availability:
        if time_type == 'start_time':
            return availability.start_time.strftime('%H:%M') if availability.start_time else ''
        elif time_type == 'end_time':
            return availability.end_time.strftime('%H:%M') if availability.end_time else ''
    return ''

def availability_to_dict(availability):
    return {
        "id": availability.id,
        "tutor_id": availability.tutor_id,
        "day": availability.day,
        "start_time": availability.start_time.strftime('%H:%M') if availability.start_time else None,
        "end_time": availability.end_time.strftime('%H:%M') if availability.end_time else None,
    }


from sqlalchemy import and_
@views.route('/edit-tutor/<int:tutor_id>', methods=['GET', 'POST'])
@login_required
def edit_tutor(tutor_id):
    tutor = Tutor.query.get_or_404(tutor_id)

    # Verfügbarkeitsdaten des Tutors abrufen
    availabilities = Availability.query.filter_by(tutor_id=tutor_id).all()

    if request.method == 'POST':
        # Aktualisiere die Tutor-Daten
        tutor.name = request.form.get('name')
        tutor.birthdate = datetime.strptime(request.form.get('birthdate'), '%Y-%m-%d').date()
        tutor.max_grade = request.form.get('max_grade')
        tutor.subjects = ','.join(request.form.getlist('subjects[]'))

        checked_days = request.form.getlist('availability[]')

        # delete availabilities for unchecked days
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
            if day not in checked_days:
                availability = Availability.query.filter(and_(Availability.tutor_id == tutor.id, Availability.day == day)).first()
                if availability:
                    db.session.delete(availability)

        # update or add availabilities for checked days
        print("TEST")
        for day in checked_days:
            start_time_str = (request.form.get(f'{day}_start_time'))[:5]
            end_time_str = (request.form.get(f'{day}_end_time'))[:5]

            availability = Availability.query.filter(and_(Availability.tutor_id == tutor.id, Availability.day == day)).first()
            if start_time_str and end_time_str:
                print(day)
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()

                if availability:
                    availability.start_time = start_time
                    availability.end_time = end_time
                else:
                    availability = Availability(tutor_id=tutor.id, day=day, start_time=start_time, end_time=end_time)
                    db.session.add(availability)

        # Update the additional tutor fields
        tutor.availability_comment = request.form.get('availability_comment')
        tutor.street = request.form.get('street')
        tutor.plz = request.form.get('plz')
        tutor.email = request.form.get('email')
        tutor.hours = request.form.get('hours')
        tutor.phone = request.form.get('phone')
        tutor.school_university = request.form.get('school_university')
        tutor.area = request.form.get('area')
        tutor.semester = request.form.get('semester')
        tutor.native_language = request.form.get('native_language')
        tutor.qualification = request.form.get('qualification')
        tutor.previous_training = request.form.get('previous_training')
        tutor.wage = request.form.get('wage')

        db.session.commit()

        flash('Tutor updated!', category='success')
        return redirect(url_for('views.list_tutors'))

    match_days = {}
    for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
        start_time = request.form.get(f'{day}_start_time')
        end_time = request.form.get(f'{day}_end_time')
        if start_time and end_time:
            match_days[day] = {'start_time': start_time, 'end_time': end_time}



    return render_template('edit_tutor.html', tutor_has_day=tutor_has_day, match_days = match_days, get_tutor_time = get_tutor_time, tutor=tutor, user=current_user, tutor_has_availability=tutor_has_availability, get_availability_time=get_availability_time, availabilities=availabilities)


# Define the function child_has_availability
def child_has_availability(child, day):
    availability = ChildAvailability.query.filter_by(child_id=child.id, day=day).first()
    return availability is not None

# Define the function child_has_availability
def tutor_has_availability(child, day):
    availability = ChildAvailability.query.filter_by(child_id=child.id, day=day).first()
    return availability is not None

# Get availability time for a child
def get_child_availability_time(child, day, time_type):
    availability = ChildAvailability.query.filter_by(child_id=child.id, day=day).first()
    if availability:
        if time_type == 'start_time':
            return availability.start_time.strftime('%H:%M') if availability.start_time else ''
        elif time_type == 'end_time':
            return availability.end_time.strftime('%H:%M') if availability.end_time else ''
    return ''

# Define function to convert a ChildAvailability to dictionary
def child_availability_to_dict(availability):
    return {
        "id": availability.id,
        "child_id": availability.child_id,
        "day": availability.day,
        "start_time": availability.start_time.strftime('%H:%M') if availability.start_time else None,
        "end_time": availability.end_time.strftime('%H:%M') if availability.end_time else None,
    }



def child_has_day(child, day):
    # Überprüfen, ob ein bestimmter Match an einem bestimmten Tag stattfindet
    return any(match_day.day == day for match_day in child.days)

def tutor_has_day(tutor, day):
    # Überprüfen, ob ein bestimmter Match an einem bestimmten Tag stattfindet
    return any(match_day.day == day for match_day in tutor.availability)

@views.route('/edit-child/<int:child_id>', methods=['GET', 'POST'])
@login_required
def edit_child(child_id):
    child = Child.query.get_or_404(child_id)

    # Get child's availability data
    availabilities = ChildAvailability.query.filter_by(child_id=child_id).all()

    if request.method == 'POST':
        # Update child data
        child.name = request.form.get('name')
        child.grade = request.form.get('grade')
        child.hours = request.form.get('hours')
        child.school = request.form.get('school')
        child.subjects = ','.join(request.form.getlist('subjects[]'))
        start_date_str = request.form.get('start_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        child.start_date = start_date
        child.comment = request.form.get('comment')
        child.street = request.form.get('street')
        child.plz = request.form.get('plz')
        child.email = request.form.get('email')
        child.phone = request.form.get('phone')
        child.native_language = request.form.get('native_language')

        checked_days = request.form.getlist('days[]')

        # delete availabilities for unchecked days
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
            if day not in checked_days:
                availability = ChildAvailability.query.filter(and_(ChildAvailability.child_id == child.id, ChildAvailability.day == day)).first()
                if availability:
                    db.session.delete(availability)

        # update or add availabilities for checked days
        for day in checked_days:
            start_time_str = request.form.get(f'{day}_start_time')
            end_time_str = request.form.get(f'{day}_end_time')

            start_time_str=start_time_str[:5]
            end_time_str=end_time_str[:5]

            availability = ChildAvailability.query.filter(and_(ChildAvailability.child_id == child.id, ChildAvailability.day == day)).first()
            if start_time_str and end_time_str:
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()

                if availability:
                    availability.start_time = start_time
                    availability.end_time = end_time
                else:
                    availability = ChildAvailability(child_id=child.id, day=day, start_time=start_time, end_time=end_time)
                    db.session.add(availability)


        geb_datum_str = request.form.get('geb_datum')
        year, month, day = map(int, geb_datum_str.split('-'))
        child.geb_datum = date(year, month, day)

        child.geschlecht = request.form.get('geschlecht')
        child.geb_ort = request.form.get('geb_ort')
        child.einreise_deutschland = request.form.get('einreise_deutschland')
        child.herkunftsland_mutter = request.form.get('herkunftsland_mutter')
        child.herkunftsland_vater = request.form.get('herkunftsland_vater')
        child.beruf_mutter = request.form.get('beruf_mutter')
        child.beruf_vater = request.form.get('beruf_vater')
        child.bemerkungen = request.form.get('bemerkungen')
        child.lehrer_name = request.form.get('lehrer_name')
        child.lehrer_telefon = request.form.get('lehrer_telefon')
        child.lehrer_email = request.form.get('lehrer_email')
        child.zahlung_jc = bool(request.form.get('zahlung_jc'))
        child.zahlung_wohngeld = bool(request.form.get('zahlung_wohngeld'))
        child.zahlung_kinderzuschlag = bool(request.form.get('zahlung_kinderzuschlag'))
        child.zahlung_asylbewerber = bool(request.form.get('zahlung_asylbewerber'))
        child.zahlung_privat = bool(request.form.get('zahlung_privat'))
        child.bg_nummer = request.form.get('bg_nummer')
        child.buT_nummer = request.form.get('buT_nummer')
        child.zeitraum = request.form.get('zeitraum')
        child.foerderart = request.form.get('foerderart')
        child.bewilligte_stunden = request.form.get('bewilligte_stunden')
        child.lernort = request.form.get('lernort')

        unavailable_time_slots = []
        unavailable_start_dates = request.form.getlist('unavailable_start_date[]')
        unavailable_end_dates = request.form.getlist('unavailable_end_date[]')
        unavailable_notes = request.form.getlist('unavailable_note[]')

        for start_date, end_date, note in zip(unavailable_start_dates, unavailable_end_dates, unavailable_notes):
            if start_date and end_date and note:
                start_date_str = request.form.get('start_date')
                year, month, day = map(int, start_date_str.split('-'))
                start_date = date(year, month, day)

                year, month, day = map(int, end_date.split('-'))
                end_date_obj = date(year, month, day)

                unavailable_time_slot = ChildUnavailableTimeSlot(start_date=start_date, end_date=end_date_obj, note=note)
                unavailable_time_slots.append(unavailable_time_slot)

        child.unavailable_time_slots = unavailable_time_slots

        db.session.commit()

        flash('Child updated!', category='success')
        return redirect(url_for('views.list_childreen'))

    match_days = {}
    for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
        start_time = request.form.get(f'{day}_start_time')
        end_time = request.form.get(f'{day}_end_time')
        if start_time and end_time:
            match_days[day] = {'start_time': start_time, 'end_time': end_time}
        
        #print(availability.day)

    return render_template('edit_child.html', get_child_time=get_child_time, child=child, user=current_user, child_has_day=child_has_day, get_child_availability_time=get_child_availability_time, match_days=match_days)



from datetime import datetime

@views.route('/update-match-day', methods=['POST'])
def update_match_day():
    data = request.get_json()

    match_id = data['matchId']
    original_day = data['originalDay']
    target_day = data['targetDay']
    start_time_string = data['startTime']
    end_time_string = data['endTime']

    print(match_id)
    print(original_day)
    print(target_day)
    print(start_time_string)
    print(end_time_string)

    # Convertiere die Zeitstrings in datetime.time Objekte
    start_time = datetime.strptime(start_time_string, '%H:%M').time()
    end_time = datetime.strptime(end_time_string, '%H:%M').time()

    # Suche das MatchDay-Objekt anhand von match_id und original_day
    match_day = MatchDay.query.filter_by(match_id=match_id, day=original_day).first()

    if match_day:

        # Aktualisiere das MatchDay-Objekt mit den neuen Werten
        match_day.day = target_day
        match_day.start_time = start_time
        match_day.end_time = end_time

        # Speichere die Änderungen in der Datenbank
        db.session.commit()
        print("Updated MatchDay")

        return jsonify({'success': True})
    else:
        print("error")
        return jsonify({'success': False, 'error': 'MatchDay not found'})


@views.route('/update-tutor/<int:tutor_id>', methods=['POST'])
def update_tutor(tutor_id):
    tutor = Tutor.query.get(tutor_id)
    if tutor is None:
        flash('Tutor not found', category='error')
        return redirect(url_for('views.tutor_list'))
    
    tutor.name = request.form.get('name')
    tutor.birthdate = request.form.get('birthdate')
    tutor.max_grade = request.form.get('max_grade')
    tutor.subjects = request.form.getlist('subjects[]')
    db.session.commit()
    flash('Tutor updated successfully', category='success')
    return redirect(url_for('views.tutor_list', user=current_user))


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/delete-match/<int:match_id>', methods=['POST'])
def delete_match(match_id):
    match = Match.query.get_or_404(match_id)
    db.session.delete(match)
    db.session.commit()
    flash('Match has been deleted!', category='success')
    return redirect(url_for('views.list_matches'))

@views.route('/delete-child/<int:child_id>', methods=['POST'])
def delete_child(child_id):
    child = Child.query.get_or_404(child_id)

    # Lösche zugehörige Matches
    matches = Match.query.filter_by(child_id=child_id).all()
    for match in matches:
        db.session.delete(match)
        
    # Lösche den Schüler
    db.session.delete(child)
    db.session.commit()
    return redirect(url_for('views.list_childreen'))  # leitet den Benutzer zur Indexseite um

@views.route('/delete-tutor/<int:tutor_id>', methods=['POST'])
def delete_tutor(tutor_id):
    tutor = Tutor.query.get_or_404(tutor_id)

    # Lösche zugehörige Matches
    matches = Match.query.filter_by(tutor_id=tutor_id).all()
    for match in matches:
        db.session.delete(match)
        
    # Lösche den Schüler
    db.session.delete(tutor)
    db.session.commit()
    return redirect(url_for('views.list_tutors'))  # leitet den Benutzer zur Indexseite um

