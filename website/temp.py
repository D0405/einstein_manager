from datetime import datetime, timedelta
from collections import defaultdict
from flask import render_template

# ...

@app.route('/match-tutor-child')
def match_tutor_child():
    tutors = Tutor.query.all()
    children = Child.query.all()
    matches = []

    # Dictionaries zur Verfolgung der Anzahl der Termine und der zugewiesenen Lernhelfer für jeden Schüler und Tutor
    child_appointments = defaultdict(int)
    tutor_appointments = defaultdict(int)

    for tutor in tutors:
        for child in children:
            # Überprüfe, ob der Schüler bereits 2 Termine oder der Tutor bereits 2 Schüler hat
            if child_appointments[child.id] >= 2 or tutor_appointments[tutor.id] >= 2:
                continue

            if set(tutor.subjects.split(',')) & set(child.subjects.split(',')) and int(child.grade) <= tutor.max_grade:
                # Suche nach Paaren von Tagen, an denen sowohl der Lernhelfer als auch das Kind verfügbar sind
                matching_days = []
                for tutor_availability in tutor.availability:
                    for child_availability in child.days:
                        if tutor_availability.day == child_availability.day:
                            # Finde den Zeitraum, in dem beide verfügbar sind
                            start_time = max(tutor_availability.start_time, child_availability.start_time)
                            end_time = min(tutor_availability.end_time, child_availability.end_time)

                            # Überprüfe, ob der Zeitraum genau eine Stunde ist
                            start_datetime = datetime.combine(datetime.today(), start_time)
                            end_datetime = datetime.combine(datetime.today(), end_time)
                            time_diff = end_datetime - start_datetime
                            if time_diff == timedelta(hours=1):
                                matching_days.append({
                                    'day': tutor_availability.day,
                                    'start_time': start_time,
                                    'end_time': end_time,
                                })

                # Überprüfe, ob genau zwei Tage gefunden wurden
                if len(matching_days) == 2:
                    # Füge das Match hinzu und aktualisiere die Zähler für den Schüler und den Tutor
                    matches.append({
                        'tutor': tutor,
                        'child': child,
                        'days': matching_days,
                    })
                    child_appointments[child.id] += 2
                    tutor_appointments[tutor.id] += 1

    # Sortiere die Matches basierend auf der Anzahl der Termine pro Schüler
    matches.sort(key=lambda x: child_appointments[x['child'].id])

    # ...

    return render_template("match_tutor_child.html", matches=matches, user=current_user)



###########
def print_matches(matches, children):
    tutor_to_children = {}
    child_to_appointments = {}
    all_children = set(children)
    matched_children = set()

    for match in matches:
        tutor = Tutor.query.get(match.tutor_id)
        child = Child.query.get(match.child_id)
        days = match.days

        print(f"Tutor {tutor.name} wurde dem Schüler {child.name} zugeordnet.")
        print(f"Sie treffen sich an folgenden Tagen:")
        for day in days:
            print(f"- {day.day.capitalize()}: von {day.start_time} bis {day.end_time}")
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
            for day in child.days:
                print(f"- {day.day.capitalize()}: von {day.start_time} bis {day.end_time}")
            print()
    else:
        print("Alle Schüler haben Termine.")

from collections import defaultdict
from collections import defaultdict

# ...

@views.route('/match-tutor-child')
def match_tutor_child():
    # Löschen Sie alle Einträge in der MatchDay und Match Tabelle
    MatchDay.query.delete()
    Match.query.delete()
    db.session.commit()

    tutors = Tutor.query.all()
    children = Child.query.all()
    matches = []

    tutor_appointments = defaultdict(list)  # Dictionary für die Termine der Tutoren
    child_appointments = defaultdict(list)  # Dictionary für die Termine der Kinder

    # Gruppieren Sie die Tutoren nach Verfügbarkeitstagen
    tutors_by_day = defaultdict(list)
    for tutor in tutors:
        for availability in tutor.availability:
            tutors_by_day[availability.day].append(tutor)

    # Zähler für die Anzahl der Tage, an denen ein Tutor zugewiesen ist
    tutor_days_counter = defaultdict(int)

    for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
        available_tutors = tutors_by_day[day]
        if len(available_tutors) < 1:
            continue  # Nicht genügend verfügbare Tutoren an diesem Tag

        for tutor in available_tutors:
            if tutor_days_counter[tutor.id] >= 2:
                continue  # Der Tutor wurde bereits an zwei Tagen zugewiesen

            assigned_children = set()  # Verfolgen Sie die bereits zugewiesenen Kinder für den Tutor

            for child in children:
                if child.id in assigned_children:
                    continue  # Das Kind wurde bereits einem Termin zugewiesen

                if set(tutor.subjects.split(',')) & set(child.subjects.split(',')) and int(child.grade) <= tutor.max_grade:
                    matching_days = []
                    for tutor_availability in tutor.availability:
                        if tutor_availability.day == day:
                            for child_availability in child.days:
                                if child_availability.day == day:
                                    # Überprüfen, ob der Tutor oder das Kind bereits zu dieser Zeit zugewiesen ist
                                    if any(
                                        tutor_appointment[0] <= tutor_availability.start_time < tutor_appointment[1] or
                                        tutor_appointment[0] < tutor_availability.end_time <= tutor_appointment[1]
                                        for tutor_appointment in tutor_appointments[tutor.id]):
                                        continue

                                    # Überprüfen, ob das Kind bereits einem Tutor an diesem Tag zugewiesen ist
                                    if any(
                                        child_appointment[0] <= tutor_availability.start_time < child_appointment[1] or
                                        child_appointment[0] < tutor_availability.end_time <= child_appointment[1]
                                        for child_appointment in child_appointments[child.id]):
                                        continue

                                    # Finde den Zeitraum, in dem beide verfügbar sind
                                    start_time = max(tutor_availability.start_time, child_availability.start_time)
                                    end_time = min(tutor_availability.end_time, child_availability.end_time)

                                    # Überprüfe, ob der Zeitraum genau eine Stunde ist
                                    start_datetime = datetime.combine(datetime.today(), start_time)
                                    end_datetime = datetime.combine(datetime.today(), end_time)
                                    time_diff = end_datetime - start_datetime
                                    if time_diff == timedelta(hours=1):
                                        matching_days.append({
                                            'day': tutor_availability.day,
                                            'start_time': start_time,
                                            'end_time': end_time,
                                        })

                    # Überprüfe, ob genau ein Tag und ein Termin gefunden wurden
                    if len(matching_days) == 1:
                        match = Match(tutor_id=tutor.id, child_id=child.id)
                        db.session.add(match)
                        db.session.commit()

                        day = matching_days[0]['day']
                        start_time = matching_days[0]['start_time']
                        end_time = matching_days[0]['end_time']

                        match_day = MatchDay(match_id=match.id, day=day, start_time=start_time, end_time=end_time)
                        db.session.add(match_day)
                        db.session.commit()

                        tutor_appointments[tutor.id].append((start_time, end_time))
                        child_appointments[child.id].append((start_time, end_time))

                        assigned_children.add(child.id)
                        tutor_days_counter[tutor.id] += 1

    matches = Match.query.all()
    matches.sort(key=lambda x: len(child_appointments[x.child_id]))
    print_matches(matches, children)

    return render_template("match_tutor_child.html", matches=matches, user=current_user,
                           get_child_name_by_id=get_child_name_by_id,
                           get_tutor_name_by_id=get_tutor_name_by_id)