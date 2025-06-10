# *******************************************************
# IMPORTS AND CONSTANTS
# *******************************************************

# GIT AND SECURITY
import git, hmac, hashlib, json, os
from dotenv import load_dotenv

# FLASK
from flask import Flask, render_template, request, redirect, url_for, flash

# DAOs
import performance_dao, user_dao, stage_dao

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

# VALIDATION
import re
EMAIL_REGEX = '^[A-Za-z0-9._]+@[A-Za-z]+\.[A-Z|a-z]{2,7}$'
PASSWORD_REGEX = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
ALLOWED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]

# IMAGE REMODELING
from PIL import Image
PROFILE_IMG_HEIGHT = 400

# DATES
from datetime import datetime
DATES = ["2025-07-18T00:00", "2025-07-19T00:00", "2025-07-20T00:00"]
FORMAT = '%Y-%m-%dT%H:%M'

# VALUES
PRICES = [7.99, 11.99, 16.99]


# *******************************************************
# INITIALIZE THE APP
# *******************************************************
app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv('secret_key')
login_manager = LoginManager()
login_manager.init_app(app)

# *******************************************************
# SUPPORTING FUNCTIONS
# *******************************************************
"""
Obtain the duration of a performance for a given artist.

:param performance: performance to obtain the duration from
:return: duration in minutes 
"""
def obtain_duration(performance):
    duration = (datetime.strptime(performance["end_date"], FORMAT) - datetime.strptime(performance["start_date"], FORMAT)).total_seconds()
    minutes = int(duration / 60)
    return'{} min'.format(minutes)


"""
Obtain the duration of a performance for a given artist.

:param performances: performances to obtain the durations from
:return: list with all the formatted minutes
"""
def obtain_duration_for_all(performances):
    durations = {}
    
    for performance in performances:    
        durations[performance["performance_id"]] = obtain_duration(performance)
    
    return durations


"""
Checks if the email has a valid format.

:return: Match object if matching, None if not matching
"""
def is_email_valid(email):
    return re.fullmatch(EMAIL_REGEX, email)


"""
Checks if the password has a valid format.

:return: Match object if matching, None if not matching
"""
def is_password_valid(password):
    return re.fullmatch(PASSWORD_REGEX, password)


"""
Checks if two performances overlap.

:return: True if overlap, False if not
"""
def check_overlap(first_performance, second_performance):
    return second_performance["published"] and (first_performance["stage"] == second_performance["stage_id"] or (first_performance["start_date"] < second_performance["end_date"] and first_performance["end_date"] > second_performance["start_date"]))


# *******************************************************
# HOMEPAGE
# *******************************************************
"""
Renders the homepage by getting the performances and, for each of them, music genre, stage and duration.

:return: the template render of homepage.html
"""
@app.route("/")
def homepage():
    performances = performance_dao.get_published_performances()
    music_genres = performance_dao.get_music_genres()

    stages = stage_dao.get_stages()
    
    durations = obtain_duration_for_all(performances)
    dates = DATES
    
    return render_template(
        "homepage.html", 
        p_performances = performances, 
        p_music_genres = music_genres, 
        p_stages = stages, 
        p_durations = durations,
        p_dates = dates
    )

"""
Renders the homepage by getting the filtered performances and, for each of them, music genre, stage and duration.

:return: the template render of homepage.html
"""
@app.route("/", methods=['POST'])
def homepage_post():
    filters = request.form.to_dict()
    filters_sql = [filters['date_filter'], filters['stage_filter'], filters['music_genre_filter']]
        
    performances = performance_dao.get_published_performances_filter(filters_sql)
    music_genres = performance_dao.get_music_genres()
    stages = stage_dao.get_stages()
    
    durations = obtain_duration_for_all(performances)
    dates = DATES
    
    return render_template(
        "homepage.html", 
        p_performances = performances,
        p_music_genres = music_genres,
        p_stages = stages,
        p_durations = durations,
        p_dates = dates
    )


# *******************************************************
# ARTIST PAGE
# *******************************************************
"""
Renders the artist page by getting the specific artist info and his performance info.

:param artist_id: identifier of the artist
:return: the template render of artist.html
"""
@app.route("/artist/<int:artist_id>")
def artist(artist_id):
    performance = performance_dao.get_performance_from_artist(artist_id)
    duration = obtain_duration(performance)
    
    if performance["published"] == 0:
        if current_user.is_authenticated and current_user.type != 2 or not current_user.is_authenticated:
            return homepage()
    
    return render_template(
        "artist.html", 
        p_performance = performance,
        p_duration = duration
    )
    

# *******************************************************
# SIGNUP PAGE
# *******************************************************
"""
Loads the signup page.

:return: the template render of signup.html
"""
@app.route("/signup")
def signup():
    if current_user.is_authenticated:
        return homepage()
    
    return render_template("signup.html")


"""
Registers the user inserted in the signup page.

:return: the template render of login.html (success) or signup.html (failure)
"""
@app.route("/signup", methods=["POST"])
def signup_post():
    if current_user.is_authenticated:
        return homepage()
    
    user_form = request.form.to_dict()
    email_form = user_form["email"]
    password_form = user_form["password"]
    password_verify_form = user_form["verify_password"]
    
    if password_form != password_verify_form:
        flash("Le due password sono diverse.", "danger")
        return redirect(url_for("signup"))
    
    if not is_email_valid(email_form):
        flash("L'email ha un formato invalido, riprova.", "danger")
        return redirect(url_for("signup"))
    
    user_db = user_dao.get_user_by_email(email_form)

    if user_db:
        flash("Email già registrata.", "danger")
        return redirect(url_for("signup"))
    else:
        if not is_password_valid(password_form):
            flash("La password ha un formato invalido, riprova.", "danger")
            return redirect(url_for("signup"))
        
        user_form["password"] = generate_password_hash(password_form)
        success = user_dao.add_user(user_form)

        if success:
            flash("Utente creato correttamente.", "success")
            return redirect(url_for("login"))
        else:
            flash("Errore nella creazione dell'utente: riprova!", "danger")
            return redirect(url_for("signup"))


# *******************************************************
# LOGIN, LOGOUT AND USER LOADING
# *******************************************************
"""
Loads the login page.

:return: the template render of login.html
"""
@app.route("/login")
def login():
    if current_user.is_authenticated:
        return homepage()
    
    return render_template(
        "login.html"
    )


"""
Logins the user inserted in the login page.

:return: the template render of homepage.html (success) or login.html (failure)
"""
@app.route("/login", methods=["POST"])
def login_post():
    if current_user.is_authenticated:
        return homepage()
    
    user_form = request.form.to_dict()
    email_form = user_form["email"]
    password_form = user_form["password"]
    
    if (not is_email_valid(email_form)):
        flash("L'email ha un formato invalido, riprova.", "danger")
        return redirect(url_for("login"))

    user_db = user_dao.get_user_by_email(email_form)
    
    if not user_db or not check_password_hash(user_db["password"], password_form):
        flash("Credenziali non valide, riprova.", "danger")
        return redirect(url_for("login"))
    else:
        new = User(
            id = user_db["id"],
            name = user_db["name"],
            surname = user_db["surname"],
            email = user_db["email"],
            password = user_db["password"],
            type = user_db["type"],
        )
        login_user(new, True)
        flash("Bentornato, " + new.name + " " + new.surname + "!", "success")

        return homepage()


"""
Loads the user into session.

:param user_id: id of the user to load
:return: loaded user
"""
@login_manager.user_loader
def load_user(user_id):
    user_db = user_dao.get_user(user_id)
    
    if user_db:
        user = User(
            id = user_db["id"],
            name = user_db["name"],
            surname = user_db["surname"],
            email = user_db["email"],
            password = user_db["password"],
            type = user_db["type"],
        )
    else:
        user = None

    return user


"""
Logouts the current logged in user

:return: the template render of homepage.html
"""
@login_required
@app.route("/logout")
def logout():
    if not current_user.is_authenticated:
        return homepage()
    
    logout_user()
    return homepage()


# *******************************************************
# TICKETS PAGE
# *******************************************************
"""
Loads the tickets page.

:return: the template render of tickets.html
"""
@login_required
@app.route("/tickets")
def tickets():
    if not current_user.is_authenticated:
        return homepage()
    
    ticket = user_dao.get_ticket_by_user_id(current_user.id)
    people_count_days = performance_dao.get_count_people_days()
    
    return render_template(
        "tickets.html", 
        p_ticket = ticket, 
        p_people_count_days = people_count_days
    )


"""
Registers the ticket inserted in the tickets page.

:return: the template render of the profile page (success) or another page (failure)
"""
@login_required
@app.route("/tickets", methods=["POST"])
def tickets_post():
    if not current_user.is_authenticated:
        return homepage()

    if current_user.type != 1:
        flash("Impossibile acquistare il biglietto con questo profilo.", "danger")
        return homepage()

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
        
        success = user_dao.add_ticket_to_user(ticket)
        
        if success:
            flash("Biglietto comprato con successo.", "success")
            return profile()
        else:
            flash("Errore durante l'acquisto del biglietto, riprova!", "danger")
            return tickets()
        

# *******************************************************
# PERFORMANCE PAGE
# *******************************************************
"""
Loads the performance page.

:return: the template render of the performance page (success) or homepage (failure)
"""
@login_required
@app.route("/performance")
def performance():
    if not current_user.is_authenticated or current_user.type != 2:
        return homepage()
    
    stages = stage_dao.get_stages()
    
    return render_template(
        "performance.html", 
        p_stage = stages, 
        p_request_type = 0
    )


"""
Registers the performance inserted in the performance page.

:return: the template render of the profile page (success) or another page (failure)
"""
@login_required
@app.route("/profile", methods=["POST"])
def performance_post():
    if not current_user.is_authenticated:
        return homepage()
    
    if current_user.type != 2:
        return homepage()
    
    performance_form = request.form.to_dict()
    performances_db = performance_dao.get_performances()
    overlap = False

    for performance_db in performances_db:
        if (check_overlap(performance_form, performance_db)):
            overlap = True
            break
    
    timestamp = int(datetime.now().timestamp())

    img_artist = ""
    if performance_form["artist_image"]:
        artist_image = request.files["artist_image"]
        if artist_image:
            ext = artist_image.filename.split(".")[-1]
            if ext not in ALLOWED_IMAGE_EXTENSIONS:
                flash("Estensione dei file non permessa.", "danger")
                return homepage()
            
            img = Image.open(artist_image)

            # change dimensions of the image to PROFILE_IMG_HEIGHT x PROFILE_IMG_HEIGHT
            width, height = img.size
            new_width = PROFILE_IMG_HEIGHT * width / height
            size = new_width, PROFILE_IMG_HEIGHT
            img.thumbnail(size, Image.Resampling.LANCZOS)
            left = new_width / 2 - PROFILE_IMG_HEIGHT / 2
            top = 0
            right = new_width / 2 + PROFILE_IMG_HEIGHT / 2
            bottom = PROFILE_IMG_HEIGHT
            img = img.crop((left, top, right, bottom))
            
            # change the name of the file and save it in the static folder
            new_filename = performance_form.get("name").lower() + "_" + str(timestamp) + "." + ext
            img.save("static/" + new_filename)
            img_artist = new_filename

    img_performance = ""
    if performance_form["performance_image"]:
        performance_image = request.files["performance_image"]
        if performance_image:
            ext = performance_image.filename.split(".")[-1]
            if ext not in ALLOWED_IMAGE_EXTENSIONS:
                flash("Estensione dei file non permessa.", "danger")
                return homepage()
            
            img = Image.open(performance_image)
            new_filename = performance_form.get("name").lower() + "_performance_" + str(timestamp) + "." + ext
            img.save("static/" + new_filename)
            img_performance = new_filename

    performance_form["artist_image"] = img_artist
    performance_form["performance_image"] = img_performance

    success = performance_dao.add_performance(performance_form)
    
    if success and overlap:
        flash("Performance in sovrapposizione con un'altra performance pubblicata.", "warning")
        return profile()
    elif success:
        flash("Performance creata correttamente.", "success")
        return profile()
    else:
        flash("Errore nella creazione della performance: riprova!", "danger")
        return performance()
    

"""
Renders the performance page in update mode.

:param artist_id: identifier of the artist
:return: the template render of the performance page in update mode
"""
@login_required
@app.route("/update_performance/<int:artist_id>")
def update_performance(artist_id):
    if not current_user.is_authenticated:
        return homepage()
    
    if current_user.type != 2:
        return homepage()
    
    performance_db = performance_dao.get_performance_from_artist(artist_id)
    stages = stage_dao.get_stages()
    
    return render_template(
        "performance.html", 
        p_performance = performance_db, 
        p_stage = stages, 
        p_request_type = 1
    )
    

"""
Updates the performance updated in the performance page in update mode.

:param artist_id: identifier of the artist
:return: 
"""
@login_required
@app.route("/update_performance/<int:artist_id>", methods=["POST"])
def update_performance_post(artist_id):
    if not current_user.is_authenticated:
        return homepage()
    
    if current_user.type != 2:
        return homepage()
    
    performance_form = request.form.to_dict()
    performances_db = performance_dao.get_performances()
    
    if not performances_db:
        return homepage()
    
    artist_db = performance_dao.get_artist(artist_id)
    overlap = False

    for performance_db in performances_db:
        if (check_overlap(performance_form, performance_db)):
            overlap = True
            break
    
    timestamp = int(datetime.now().timestamp())

    img_artist = artist_db["image"]
    artist_image = request.files["artist_image"]
    if artist_image:
        ext = artist_image.filename.split(".")[-1]
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            flash("Estensione dei file non permessa.", "danger")
            return homepage()
        
        img = Image.open(artist_image)

        # change dimensions of the image to PROFILE_IMG_HEIGHT x PROFILE_IMG_HEIGHT
        width, height = img.size
        new_width = PROFILE_IMG_HEIGHT * width / height
        size = new_width, PROFILE_IMG_HEIGHT
        img.thumbnail(size, Image.Resampling.LANCZOS)
        left = new_width / 2 - PROFILE_IMG_HEIGHT / 2
        top = 0
        right = new_width / 2 + PROFILE_IMG_HEIGHT / 2
        bottom = PROFILE_IMG_HEIGHT
        img = img.crop((left, top, right, bottom))
        
        # change the name of the file and save it in the static folder
        new_filename = performance_form.get("name").lower() + "_" + str(timestamp) + "." + ext
        os.remove("static/" + img_artist)
        img.save("static/" + new_filename)
        img_artist = new_filename

    img_performance = performance_db["image"]
    performance_image = request.files["performance_image"]
    if performance_image:
        ext = performance_image.filename.split(".")[-1]
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            flash("Estensione dei file non permessa.", "danger")
            return homepage()
        
        img = Image.open(performance_image)
        new_filename = performance_form.get("name").lower() + "_performance_" + str(timestamp) + "." + ext
        os.remove("static/" + img_performance)
        img.save("static/" + new_filename)
        img_performance = new_filename

    performance_form["artist_image"] = img_artist
    performance_form["performance_image"] = img_performance
    
    success = performance_dao.update_performance(performance_form, artist_id, overlap)
        
    if success and overlap:
        flash("Performance in sovrapposizione con un'altra performance pubblicata.", "warning")
        return update_performance(artist_id)
    elif success:
        flash("Performance aggiornata correttamente.", "success")
        return artist(artist_id)
    else:
        flash("Errore nell'aggiornamento della performance: riprova!", "danger")
        return update_performance(artist_id)


# *******************************************************
# PROFILE PAGE
# *******************************************************
"""
Renders the profile page for the requested user.

:return: the template render of the profile page 
"""
@login_required
@app.route("/profile")
def profile():
    if not current_user.is_authenticated:
        return homepage()
    
    if (current_user.type == 2):
        published_performances = performance_dao.get_published_performances()
        published_durations = obtain_duration_for_all(published_performances)
        
        unpublished_performances = performance_dao.get_unpublished_performances(current_user.id)
        unpublished_durations = obtain_duration_for_all(unpublished_performances)
        
        people_count_days = performance_dao.get_count_people_days()
        tickets_count_type = performance_dao.get_tickets_per_type()
        tickets_value = []
        for i in range (0, 3):
            tickets_value.append(round(PRICES[i]*tickets_count_type[i], 2))
            
        tickets_value.append(round(tickets_value[0] + tickets_value[1] + tickets_value[2], 2))
            
        return render_template(
            "profile.html", 
            p_published_performances = published_performances, 
            p_published_durations = published_durations, 
            p_unpublished_performances = unpublished_performances, 
            p_unpublished_durations = unpublished_durations, 
            p_people_count_days = people_count_days, 
            p_tickets_value = tickets_value
        )
    else:
        ticket = user_dao.get_ticket_by_user_id(current_user.id)
        
        end_date = ""
        if ticket:
            end_date = performance_dao.get_next_day(ticket["start_date"])
            
        return render_template(
            "profile.html", 
            p_ticket = ticket, 
            p_end_date = end_date
        )
