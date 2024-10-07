import json
from flask import Flask, render_template, request, redirect, flash, url_for, session
from slugify import slugify


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


def clean_club_name():
    for club in load_clubs():
        clean_name = slugify(club['name'], separator='_')
        return clean_name


def clean_competition_name():
    for competition in load_competitions()['name']:
        clean_name = slugify(competition['name'], separator='_')
        return clean_name


app = Flask(__name__)
app.secret_key = 'something_special'

# Ajout du filtre 'slugify' à Jinja2
app.jinja_env.filters['slugify'] = slugify


@app.route('/', methods=['GET', 'POST'])
def registration():

    if request.method == 'POST':
        email = request.form['email']
        club = next((club for club in load_clubs() if club['email'] == email), None)
        if club:
            session['email'] = email
            return redirect(url_for('homepage'))
        else:
            flash("Email non valide. Veuillez réessayer.")
            return redirect(url_for('registration'))
    return render_template('registration.html')


@app.route('/homepage')
def homepage():
    email = session.get('email')
    if not email:
        flash("Accès non autorisé.")
        return redirect(url_for('registration'))
    club = next((club for club in load_clubs() if club['email'] == email), None)
    if not club:
        flash("Club non trouvé.")
        return redirect(url_for('registration'))
    return render_template('homepage.html', club=club, competitions=load_competitions())


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = next((c for c in load_clubs() if slugify(c['name'], separator='-') == club), None)
    found_competition = next((c for c in load_competitions() if slugify(c['name'], separator='-') == competition),
                             None)
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('homepage.html', club=club, competitions=load_competitions())


@app.route('/booking', methods=['POST'])
def purchase_places():

    competition = [c for c in load_competitions() if c['name'] == request.form['competition']][0]
    club = [c for c in load_clubs() if c['name'] == request.form['club']][0]
    club_email = session.get('email')
    club_point = int(club['points'])
    places_required = int(request.form['places'])
    competition['available_places'] = int(competition['available_places']) - places_required

    if competition['available_places'] < 0:
        flash("There is not enough space for your request, please enter fewer places.")
        return redirect(url_for('book',
                                competition=slugify(competition['name'], separator='-'),
                                club=slugify(club['name'], separator='-')))
    elif places_required > club_point:
        flash("You don't have enough points to reserve that many places.")
        return redirect(url_for('book',
                                competition=slugify(competition['name'], separator='-'),
                                club=slugify(club['name'], separator='-')))
    elif places_required < 0:
        flash("You cannot reserve a negative number of places.")
        return redirect(url_for('book',
                                competition=slugify(competition['name'], separator='-'),
                                club=slugify(club['name'], separator='-')))
    else:
        # CLUB UPDATED DATA
        with open('clubs.json', 'r') as f:
            data = json.load(f)

        for each_club in data['clubs']:
            if each_club['email'] == club_email:
                updated_point_data_club = club['points'] - places_required
                each_club['points'] = updated_point_data_club

        with open("clubs.json", "w") as c:
            json.dump(data, c, indent=4)

        # COMPETITION UPDATED DATA
        with open('competitions.json', 'r') as f:
            data = json.load(f)

        for each_competition in data['competitions']:
            if each_competition['name'] == competition['name']:
                updated_point_data_competition = competition['available_places']
                each_competition['available_places'] = updated_point_data_competition

        with open("competitions.json", "w") as c:
            json.dump(data, c, indent=4)
        return redirect(url_for('homepage'))


@app.route('/clubs')
def clubs_list():
    clubs = load_clubs()
    competitions = load_competitions()
    name = session.get('name')
    return render_template('clubs.html', clubs=clubs, competitions=competitions, name=name)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    session.pop('email', None)
    flash("Vous avez été déconnecté.")
    return redirect(url_for('registration'))
