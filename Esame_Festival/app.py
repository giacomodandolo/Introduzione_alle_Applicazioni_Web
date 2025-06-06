# GIT AND SECURITY
import git, hmac, hashlib, json, os
from dotenv import load_dotenv

# FLASK
from flask import Flask, render_template, request, redirect, url_for, flash

# DAO
import artist_dao, performance_dao, user_dao, stage_dao
from datetime import datetime

# AUTHENTICATION
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

# IMAGE REMODELING
from PIL import Image

PROFILE_IMG_HEIGHT = 400
PERFORMANCE_IMG_HEIGHT = 1920
PERFORMANCE_IMG_WIDTH = 1080

# DATES
DATES = ["2025-07-18T00:00", "2025-07-19T00:00", "2025-07-20T00:00"]
FORMAT = '%Y-%m-%dT%H:%M'

# APP RUN
def configure():
    load_dotenv()

app = Flask(__name__)
configure()
app.config["SECRET_KEY"] = os.getenv('secret_key')

login_manager = LoginManager()
login_manager.init_app(app)

"""
Obtain the duration of a performance for a given artist

:param artist: artist to obtain the duration from
:return: formatted minutes
"""
def obtain_duration(artist):
    duration = (datetime.strptime(artist["fine"], FORMAT) - datetime.strptime(artist["inizio"], FORMAT)).total_seconds()
    minutes = int(duration / 60)
    return'{} min'.format(minutes)


def obtain_duration_for_all(artists):
    durations = {}
    
    for artist in artists:
        durations[artist["id_artista"]] = obtain_duration(artist)
    
    return durations


"""
Retrieves artists (with their respective performance) and loads the homepage

:return: the template render of homepage.html
"""
@app.route("/")
def homepage():
    artists = performance_dao.get_published_performances()
    durations = {}
    stages = stage_dao.get_stages()
    music_genres = performance_dao.get_music_genres()
    
    for artist in artists:
        durations[artist["id_artista"]] = obtain_duration(artist)
    
    return render_template("homepage.html", p_artists = artists, p_durations = durations, p_dates = DATES, p_stages = stages, p_music_genres = music_genres)

"""
Retrieves artists (with their respective performance) and loads the homepage

:return: the template render of homepage.html
"""
@app.route("/", methods=['POST'])
def homepage_post():
    filters = request.form.to_dict()
    filters_sql = [filters['date_filter'], filters['stage_filter'], filters['music_genre_filter']]
    
    artists = performance_dao.get_published_performances_filter(filters_sql)
    durations = {}
    stages = stage_dao.get_stages()
    music_genres = performance_dao.get_music_genres()
    
    for artist in artists:
        durations[artist["id_artista"]] = obtain_duration(artist)
    
    return render_template("homepage.html", p_artists = artists, p_durations = durations, p_dates = DATES, p_stages = stages, p_music_genres = music_genres)


"""
Retrieves the artist's and perfomance's info and loads the artist page

:return: the template render of artist.html
"""
@app.route("/artist/<int:artist_id>")
def artist(artist_id):
    artist = artist_dao.get_artist(artist_id)
    performance = performance_dao.get_performance_from_artist(artist_id)
    duration = obtain_duration(performance)
    
    return render_template(
        "artist.html", 
        p_artist = artist, 
        p_extra_image = performance['performance_image'],
        p_date = performance['inizio'].split("T")[0],
        p_hour = performance['inizio'].split("T")[1], 
        p_duration = duration,
        p_stage = performance['palco_nome']
    )
    

"""
Loads the signup page

:return: the template render of signup.html
"""
@app.route("/signup")
def signup():
    return render_template("signup.html")


"""
Registers the user inserted in signup page

:return: the template render of login.html after POST
"""
@app.route("/signup", methods=["POST"])
def signup_post():
    user_form = request.form.to_dict()
    user_db = user_dao.get_user_by_email(user_form.get("userEmail"))

    if user_db:
        flash("Email già registrata", "danger")
        return redirect(url_for("signup"))
    else:
        user_form["password"] = generate_password_hash(user_form.get("password"))
        success = user_dao.add_user(user_form)

        if success:
            flash("Utente creato correttamente.", "success")
            return redirect(url_for("login"))
        else:
            flash("Errore nella creazione dell'utente: riprova!", "danger")

    return render_template("signup.html")


"""
Loads the login page

:return: the template render of signup.html
"""
@app.route("/login")
def login():
    return render_template("login.html")


"""
Loads the login page after the form has been submit

:return: the template render of homepage.html after POST
"""
@app.route("/login", methods=["POST"])
def login_post():
    user_form = request.form.to_dict()
    user_db = user_dao.get_user_by_email(user_form["email"])

    if not user_db or not check_password_hash(user_db["password"], user_form["password"]):
        flash("Credenziali non valide, riprova", "danger")
        return redirect(url_for("login"))
    else:
        new = User(
            id=user_db["id"],
            name=user_db["nome"],
            surname=user_db["cognome"],
            email=user_db["email"],
            password=user_db["password"],
            type=user_db["tipologia"],
        )
        login_user(new, True)
        flash("Bentornato " + new.name + " " + new.surname + "!", "success")

        return redirect(url_for("homepage"))


"""
Load the user into session

:param user_id: id of the user to load
:return: loaded user
"""
@login_manager.user_loader
def load_user(user_id):
    user_db = user_dao.get_user(user_id)
    
    if user_db:
        user = User(
            id=user_db["id"],
            name=user_db["nome"],
            surname=user_db["cognome"],
            email=user_db["email"],
            password=user_db["password"],
            type=user_db["tipologia"],
        )
    else:
        user = None

    return user


"""
Logout the current logged in user

:return: the template render of homepage.html
"""
@login_required
@app.route("/logout")
def logout():
    logout_user()
    return homepage()    


"""
Loads the tickets page

:return: the template render of tickets.html
"""
@login_required
@app.route("/tickets")
def tickets():
    ticket = user_dao.get_ticket_by_user_id(current_user.id)
    people_count_days = performance_dao.get_people_count_days()
    
    return render_template("tickets.html", p_ticket = ticket, p_people_count_days = people_count_days)


"""
Loads the tickets page after POST

:return: the template render of the profile page
"""
@login_required
@app.route("/tickets", methods=["POST"])
def tickets_post():
    ticket_form = request.form.to_dict()
    ticket_db = user_dao.get_ticket_by_user_id(current_user.id)
    
    if ticket_db:
        flash("Biglietto già comprato.", "danger")
        return profile()
    else:
        ticket_type = ticket_form["submitBtn"]
        ticket_choice = 0
        
        match ticket_type:
            case "0": # Biglietto singolo giorno
                ticket_choice = int(ticket_form["choice1"])
            case "1": # Biglietto doppio giorno
                ticket_choice = int(ticket_form["choice2"])
            case "2": # Biglietto tutti i giorni
                ticket_choice = 0
        
        ticket = {
            "id": current_user.id,
            "start_date": DATES[ticket_choice],
            "type": ticket_type
        }
        
        print(ticket)
        success = user_dao.add_ticket_to_user(ticket)
        
        if success:
            flash("Biglietto comprato con successo.", "success")
            return profile()
        else:
            flash("Errore durante l'acquisto del biglietto, riprova!", "danger")
            return tickets()
        

@login_required
@app.route("/profile", methods=["POST"])
def profile_post():
    performance_form = request.form.to_dict()
    performances_db = performance_dao.get_performances()
    sovrapposizione = False

    for performance_db in performances_db:
        if (performance_db["pubblicata"] and (performance_form["stage"] == performance_db["id_palco"] or (performance_form["start_date"] < performance_db["fine"] and performance_form["end_date"] > performance_db["inizio"]))):
            sovrapposizione = True
    
    timestamp = int(datetime.now().timestamp())

    img_artist = ""
    artist_image = request.files["artist_image"]
    if artist_image:
        img = Image.open(artist_image)

        width, height = img.size
        new_width = PROFILE_IMG_HEIGHT * width / height
        size = new_width, PROFILE_IMG_HEIGHT
        img.thumbnail(size, Image.Resampling.LANCZOS)
        left = new_width / 2 - PROFILE_IMG_HEIGHT / 2
        top = 0
        right = new_width / 2 + PROFILE_IMG_HEIGHT / 2
        bottom = PROFILE_IMG_HEIGHT
        img = img.crop((left, top, right, bottom))
        
        ext = artist_image.filename.split(".")[-1]
        newFilename = performance_form.get("name").lower() + "_" + str(timestamp) + "." + ext
        img.save("static/" + newFilename)

        img_artist = newFilename

    performance_form["artist_image"] = img_artist

    img_performance = ""
    performance_image = request.files["performance_image"]
    if performance_image:
        img = Image.open(performance_image)
        ext = performance_image.filename.split(".")[-1]
        newFilename = performance_form.get("name").lower() + "_performance_" + str(timestamp) + "." + ext
        img.save("static/" + newFilename)

        img_performance = newFilename

    performance_form["performance_image"] = img_performance

    success = performance_dao.add_performance(performance_form)
    
    if success and sovrapposizione:
        flash("Performance in sovrapposizione con un'altra performance pubblicata.", "warning")
        return profile()
    elif success:
        flash("Performance creata correttamente.", "success")
        return profile()
    else:
        flash("Errore nella creazione della performance: riprova!", "danger")
        return performance()


@login_required
@app.route("/performance")
def performance():
    stages = stage_dao.get_stages()
    
    return render_template("performance.html", p_stage = stages, p_request_type = 0)

@login_required
@app.route("/profile")
def profile():
    if (current_user.type == 2):
        published_performances = performance_dao.get_published_performances()
        unpublished_performances = performance_dao.get_unpublished_performances(current_user.id)
        published_durations = obtain_duration_for_all(published_performances)
        unpublished_durations = obtain_duration_for_all(unpublished_performances)
        people_count_days = performance_dao.get_people_count_days()
        tickets_count_type = performance_dao.get_tickets_per_type()
        prices = [7.99, 11.99, 16.99]
        tickets_value = []
        for i in range (0, 3):
            tickets_value.append(round(prices[i]*tickets_count_type[i], 2))
            
        tickets_value.append(round(tickets_value[0] + tickets_value[1] + tickets_value[2], 2))
            
        return render_template("profile.html", p_people_count_days = people_count_days, p_published_performances = published_performances, p_unpublished_performances = unpublished_performances, p_published_durations = published_durations, p_unpublished_durations = unpublished_durations, p_tickets_value = tickets_value)
    else:
        ticket = user_dao.get_ticket_by_user_id(current_user.id)
        data_fine = ""
        if ticket:
            data_fine = performance_dao.get_next_day(ticket["giorno_inizio"])
            print(ticket["giorno_inizio"], data_fine)
        return render_template("profile.html", p_ticket = ticket, p_data_fine = data_fine)

@login_required
@app.route("/update_performance/<int:artist_id>")
def update_performance(artist_id):
    performance_db = performance_dao.get_performance_from_artist(artist_id)
    stages = stage_dao.get_stages()
    
    return render_template("performance.html", p_performance = performance_db, p_stage = stages, p_request_type = 1)
    
@login_required
@app.route("/update_performance/<int:artist_id>", methods=["POST"])
def update_performance_post(artist_id):
    performance_form = request.form.to_dict()
    performances_db = performance_dao.get_performances()
    overlap = False

    for performance_db in performances_db:
        if (performance_db["pubblicata"] and (performance_form["stage"] == performance_db["id_palco"] or (performance_form["start_date"] < performance_db["fine"] and performance_form["end_date"] > performance_db["inizio"]))):
            overlap = True
    
    success = performance_dao.update_performance(performance_form, artist_id, overlap)
    
    if success and overlap:
        flash("Performance in sovrapposizione con un'altra performance pubblicata.", "warning")
        return performance()
    elif success:
        flash("Performance aggiornata correttamente.", "success")
        return performance()
    else:
        flash("Errore nell'aggiornamento della performance: riprova!", "danger")
        return performance()
    
    return render_template("performance.html", p_performance = performance_db, p_request_type = 0)
    
def is_valid_signature(x_hub_signature, data, private_key):
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method != 'POST':
        return 'OK'
    else:
        abort_code = 418
        # Do initial validations on required headers
        if 'X-Github-Event' not in request.headers:
            abort(abort_code)
        if 'X-Github-Delivery' not in request.headers:
            abort(abort_code)
        if 'X-Hub-Signature' not in request.headers:
            abort(abort_code)
        if not request.is_json:
            abort(abort_code)
        if 'User-Agent' not in request.headers:
            abort(abort_code)
        ua = request.headers.get('User-Agent')
        if not ua.startswith('GitHub-Hookshot/'):
            abort(abort_code)

        event = request.headers.get('X-GitHub-Event')
        if event == "ping":
            return json.dumps({'msg': 'Hi!'})
        if event != "push":
            return json.dumps({'msg': "Wrong event type"})

        x_hub_signature = request.headers.get('X-Hub-Signature')
        # webhook content type should be application/json for request.data to have the payload
        # request.data is empty in case of x-www-form-urlencoded
        if not is_valid_signature(x_hub_signature, request.data, os.getenv(secret_key)):
            print('Deploy signature failed: {sig}'.format(sig=x_hub_signature))
            abort(abort_code)

        payload = request.get_json()
        if payload is None:
            print('Deploy payload is empty: {payload}'.format(
                payload=payload))
            abort(abort_code)

        if payload['ref'] != 'refs/heads/master':
            return json.dumps({'msg': 'Not master; ignoring'})

        repo = git.Repo(self.rorepo.working_tree_dir)
        origin = repo.remotes.origin

        pull_info = origin.pull()

        if len(pull_info) == 0:
            return json.dumps({'msg': "Didn't pull any information from remote!"})
        if pull_info[0].flags > 128:
            return json.dumps({'msg': "Didn't pull any information from remote!"})

        commit_hash = pull_info[0].commit.hexsha
        build_commit = f'build_commit = "{commit_hash}"'
        print(f'{build_commit}')
        return 'Updated PythonAnywhere server to commit {commit}'.format(commit=commit_hash)
