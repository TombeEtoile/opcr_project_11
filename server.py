import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
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
def login_and_register():
    # LOGIN
    if request.method == 'POST':
        form_type = request.form['form_type']

        if form_type == 'login':
            email = request.form['email']
            password = request.form['password']
            club = next((club for club in load_clubs() if club['email'] == email), None)

            if club and check_password_hash(club['password'], password):
                session['email'] = email
                return redirect(url_for('homepage'))

            else:
                flash("Invalid email or password. Please try again.")
                return redirect(url_for('login_and_register'))

        # REGISTER
        elif form_type == 'register':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            with open("clubs.json", "r") as file:
                clubs = json.load(file)

            if any(club['email'] == email for club in clubs['clubs']):
                flash("This email is already in use. Please choose another one.")
                return redirect(url_for('login_and_register'))

            new_club = \
                {
                    'name': name,
                    'email': email,
                    'password': hashed_password,
                    'points': 15
                }

            if new_club['email'] == '':
                flash("Please enter an email address.")
                return redirect(url_for('login_and_register'))

            if '@' not in new_club['email']:
                flash("Please enter a valid email address.")
                return redirect(url_for('login_and_register'))

            special_characters = "!@#$%^&*()_+-=[]{}|;':,./<>?"
            if not any(char in special_characters for char in new_club['password']):
                flash("Please enter a password containing at least one special character "
                      "(!@#$%^&*()_+-=[]{}|;':,./<>?).")
                return redirect(url_for('login_and_register'))

            clubs['clubs'].append(new_club)

            with open("clubs.json", "w") as c:
                json.dump(clubs, c, indent=4)

            flash("Your club has been registered.")
            return redirect(url_for('login_and_register'))

    return render_template('login_and_register.html')


@app.route('/competition_registration', methods=['GET', 'POST'])
def competition_registration():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        available_places = int(request.form['available_places'])

        with open('competitions.json', 'r') as file:
            competitions = json.load(file)

        new_competition = \
            {
                'name': name,
                'date': f'{date} {time}',
                'available_places': available_places
            }

        if date <= str(datetime.now()):
            flash("The start date of the competition cannot be lower than today.")
            return redirect(url_for('competition_registration'))

        if available_places <= 0:
            flash("The number of places available must be at least 1.")
            return redirect(url_for('competition_registration'))

        competitions['competitions'].append(new_competition)

        with open('competitions.json', 'w') as c:
            json.dump(competitions, c, indent=4)
        flash('Your competition has been registered in the database. Clubs can now register for your event.')
        return redirect(url_for('competition_registration'))

    return render_template('competition_registration.html')


@app.route('/homepage')
def homepage():
    email = session.get('email')
    if not email:
        flash("Accès non autorisé.")
        return redirect(url_for('login_and_register'))
    club = next((club for club in load_clubs() if club['email'] == email), None)

    competitions_good_date = []
    for competition in load_competitions():
        if competition['date'] >= str(datetime.now()):
            competitions_good_date.append(competition)

    if not club:
        flash("Club non trouvé.")
        return redirect(url_for('login_and_register'))
    return render_template('homepage.html', club=club, competitions=competitions_good_date)
    # return render_template('homepage.html', club=club, competitions=load_competitions())


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

    elif places_required > 12:
        flash("You cannot reserve more than 12 places.")
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
        flash(f"Your reservation of {places_required} places in the {competition['name']} "
              f"competition has been taken into account.")
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
    return redirect(url_for('login_and_register'))
