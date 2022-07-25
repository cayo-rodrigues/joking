import os
import re
import sqlite3
from functools import wraps

from decouple import config
from flask import redirect, session
from markdown2 import markdown

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = f"{os.getcwd()}/static/images/profile_pics/"
EMAIL_USERNAME = config('USER')


# From CS50 staff
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def find_pic(user_id):
    """Look for users profile pictures and return their path"""
    for ext in ALLOWED_EXTENSIONS:
        try:
            with open(f'{UPLOAD_FOLDER}{user_id}.{ext}') as pic:
                return pic.name.split('Phun', 1)[1]
        except:
            pass
    return f'{UPLOAD_FOLDER}default.jpg'.split('Phun', 1)[1]


def allowed_file(filename):
    """Ensure the uploaded picture is either a gif, jpg or png file"""
    if filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True
    return False


def check_key(dictionary, key):
    """Check if a given dictionary has a certain key"""
    if key in dictionary.keys():
        return True
    else:
        return False


def erase_picture(picture):
    """Erase a profile picture"""
    # if user's current profile pic is not the default pic
    if picture != f"{UPLOAD_FOLDER.split('Phun')[1]}default.jpg":
        os.remove(os.path.join(UPLOAD_FOLDER, picture.split('profile_pics/', 1)[1]))


def list_to_html(l):
    """Converts a list of tupples from markdown to html"""
    for i in range(len(l)):
        l[i] = list(l[i])
        l[i][0] = markdown(l[i][0])
    return l


def give_feedback(inputs, flags, all=False):
    """
    Ensure correct input and give dinamic feedback
    to user when filling the registration form
    """
    feedback = {}

    connection = sqlite3.connect('phun.db')
    cursor = connection.cursor()

    # the flags represent which fields the feedback should be given to
    if 'username' in flags or all:

        if not inputs['username']:
            feedback['username'] = "&#128551; Missing username &#128551;"

        # that is, if there is no feedback for the username field yet
        if not check_key(feedback, 'username'):
            # re.findall returns a list with all matching characters
            special_characters = re.findall(r"[\\/=&? ]", inputs['username'])
            # reject usernames with dangerous URL characters
            if special_characters:
                feedback['username'] = r'&#129300; Username may not contain " \ ", " / ", " ? ", " = ", " & " or white spaces &#129300;'

        # to fill placeholders we gotta pass in a list
        if cursor.execute("SELECT * FROM users WHERE username = ?", [inputs['username']]).fetchone():
            connection.close()
            feedback['username'] = '&#128556; Username already exists &#128556;'

    if 'password' in flags or 'confirmation' in flags or all:

        if not inputs['password']:
            feedback['password'] = "&#128551; Missing password &#128551;"

        if not check_key(feedback, 'password'):
            if re.findall(r'[ ]', inputs['password']):
                feedback['password'] = '&#129300; White spaces are not allowed &#129300;'

        if not check_key(feedback, 'password'):
            if len(inputs['password']) < 8:
                feedback['password'] = "&#128528; Password must be at least 8 characters long &#128528;"

        if not check_key(feedback, 'password'):
            # these are all the required patterns in the password
            lowercase = re.findall(r"[a-z]", inputs['password'])
            uppercase = re.findall(r"[A-Z]", inputs['password'])
            numeric = re.findall(r"[0-9]", inputs['password'])
            # only accept passwords containing lowercase, uppercase and numeric characters
            if len(lowercase) < 1 or len(uppercase) < 1 or len(numeric) < 1:
                feedback['password'] = "&#128565; Password must contain at least one lowercase, uppercase and numeric character &#128565;"

        if not inputs['confirmation']:
            feedback['confirmation'] = "&#128551; Missing password confirmation &#128551;"

        if not check_key(feedback, 'confirmation'):
            if inputs['confirmation'] != inputs['password']:
                feedback['confirmation'] = "&#128558; Passwords did not match &#128558;"

    if 'email' in flags or all:

        if not inputs['email']:
            feedback['email'] = '&#128551; Missing e-mail &#128551;'

        if not check_key(feedback, 'email'):
            already_exists = cursor.execute('SELECT email FROM users WHERE email = ?', [inputs['email']]).fetchone()
            if already_exists:
                feedback['email'] = '&#128556; E-mail already in use &#128556;'

        # yes, checking the same condition again, to avoid two feedback beeing given at once
        if not check_key(feedback, 'email'):
            valid_email = re.search(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', inputs['email'])

            if not valid_email:
                feedback['email'] = '&#128558; Invalid e-mail adress &#128558;'

    # if any of the inputs provided has not yet been added to the feedback dict,
    # it means that no problems were found and we can return a positive feedback
    for key in inputs:
        if not check_key(feedback, key):
            feedback[key] = '&#129303; Perfect &#129303;'

    connection.close()
    return feedback
