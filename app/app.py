import os
import sqlite3
from datetime import datetime
from tempfile import mkdtemp

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session)
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from .helpers import (FULL_UPLOAD_FOLDER, UPLOAD_FOLDER, allowed_file,
                      erase_picture, find_pic, give_feedback, list_to_html,
                      login_required)

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # limit uploads size to 5MB
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
    try:
        return redirect(f"/profile/{session['username']}")
    except:
        return redirect("/login")


@app.route("/profile/<username>", methods=["GET", "POST"])
@login_required
def profile(username):
    """Display (even other) user's profile page and handle new posts"""

    if request.method == 'GET':

        # check if user has changed the default jokes display order
        try:
            order = session['order']
        except:
            order = 'date_time'

        # connect to the data base
        connection = sqlite3.connect('phun.db')
        # set a cursor to simulate the blinking prompt
        cursor = connection.cursor()

        # get info regarding the user, their posts and all the jokes they voted for
        user_id = cursor.execute('SELECT id FROM users WHERE username = ?', [username]).fetchone()
        user_jokes = cursor.execute(f'SELECT joke, rating, user_id, id FROM jokes WHERE user_id = (?) ORDER BY {order} DESC',
                                    [user_id[0]]).fetchall()
        all_user_votes = cursor.execute('SELECT * FROM votes WHERE user_id = ?', [session['user_id']]).fetchall()
        q = 'SELECT * FROM comments WHERE joke_id IN (SELECT id FROM jokes WHERE user_id = ?)'
        comments = cursor.execute(q, [user_id[0]]).fetchall()

        # close connection(.quit)
        connection.close()

        # look for the user's profile pic
        ppic = find_pic(user_id[0])
        # get commenters profile pictures
        c_pics = {}
        for row in comments:
            c_pics[row[1]] = find_pic(row[1])

        return render_template("profile.html",
                                ppic=ppic,
                                username=username,
                                user_jokes=list_to_html(user_jokes),
                                all_user_votes=all_user_votes,
                                comments=list_to_html(comments),
                                c_pics=c_pics,
                                user_id=user_id[0])
    else:
        # ensure user inputs a joke
        joke = request.form.get('joke')
        if not joke or joke.strip() == '':
            flash('&#128540; Was that supposed to be a joke? &#128540;', 'alert-info')
            return redirect("/")

        # get current date and time
        now = datetime.now()

        connection = sqlite3.connect('phun.db')
        cursor = connection.cursor()

        # register joke in the database, so that we can remember it
        cursor.execute('INSERT INTO jokes (user_id, joke, rating, date_time) VALUES (?, ?, ?, ?)',
                        [session['user_id'], joke, 0, now])

        # save changes to database
        connection.commit()
        connection.close()

        return redirect('/')


@app.route('/sort/<order>', methods=['POST'])
@login_required
def sort(order):
    """Sort jokes in profile page"""

    # storing value in session seemed better than displaying it in the url
    session['order'] = order
    #return None
    return ('', 204)


@app.route('/upload_pic', methods=['POST'])
@login_required
def upload_pic():
    """Handle picture uploads"""

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('&#128533; Something went wrong with the request, please try again &#128533;', 'alert-info')
        return redirect('/')
    f = request.files['file']

    # if user does not select file, browser also submit an empty part without filename
    if f.filename == '':
        flash('&#128528; No selected file &#128528;', 'alert-info')
        return redirect('/')

    # ensure user inputs an allowed file type
    if allowed_file(f.filename):
        # use secure_filename() to protect against malicious filenames, that could mess everything up
        filename = secure_filename(f.filename)
        # get the file extension
        ext = filename.rsplit('.', 1)[1].lower()

        # erase user's former picture, if there is one
        erase_picture(find_pic(session['user_id']))
        # save new picture in the system
        f.save(os.path.join(FULL_UPLOAD_FOLDER, f"{session['user_id']}.{ext}"))
        return redirect('/')
    else:
        flash('&#128556; File type not allowed. Profile pictures must be .png, .jpg, .jpeg or .gif &#128556;', 'alert-warning')
        return redirect('/')


@app.route('/rate/<vote>', methods=["POST"])
@login_required
def rate(vote):
    """Handle joke voting"""

    connection = sqlite3.connect('phun.db')
    cursor = connection.cursor()

    # vote[0] is the joke id and vote[1] is the vote itself, either add or remove
    vote = vote.split(',', 1)
    joke_id = vote[0]

    if vote[1] == 'add':
        # ensure users can't vote more than once for a single joke
        if not cursor.execute('SELECT * FROM votes WHERE user_id = (?) AND joke_id = (?)',
                                [session['user_id'], joke_id]).fetchone():
            # remember user's vote for this joke
            cursor.execute('INSERT INTO votes (user_id, joke_id) VALUES (?, ?)',
                            [session['user_id'], joke_id])
    else:
        # ensure users can only remove their own votes
        if cursor.execute('SELECT * FROM votes WHERE user_id = (?) AND joke_id = (?)',
                            [session['user_id'], joke_id]).fetchone():
            # remove user's vote from this joke
            cursor.execute('DELETE FROM votes WHERE user_id = (?) AND joke_id = (?)',
                            [session['user_id'], joke_id])

    # update votes count
    cursor.execute('UPDATE jokes SET rating = (SELECT COUNT() FROM votes WHERE joke_id = (?)) WHERE id = (?)', [joke_id, joke_id])
    # get that joke's current rating
    rating = cursor.execute('SELECT rating FROM jokes WHERE id = ?', [joke_id]).fetchone()

    connection.commit()
    connection.close()

    # return rating to js as a json, so that the vote count(rating) can be visually updated
    return jsonify(rating)


@app.route('/posts/<sort_order>')
@login_required
def posts(sort_order):
    """ Display all posts """

    # change page's title and heading according to the order of display
    if sort_order == 'newest':
        order_by = 'date_time'
        messages = {
            'title': 'Newest',
            'img': 'Posts_new.png'
        }
    else:
        order_by = 'rating'
        messages = {
            'title': 'Phuniest',
            'img': 'Posts_best.png'
        }

    connection = sqlite3.connect('phun.db')
    cursor = connection.cursor()

    # get all users info, posts and all the jokes they voted for
    all_users = cursor.execute('SELECT id, username FROM users').fetchall()
    all_jokes = cursor.execute(f'SELECT joke, rating, user_id, id FROM jokes ORDER BY {order_by} DESC').fetchall()
    all_user_votes = cursor.execute('SELECT * FROM votes WHERE user_id = ?', [session['user_id']]).fetchall()
    all_comments = cursor.execute('SELECT * FROM comments').fetchall()
    connection.close()

    # get all users profile pictures
    all_pics = {}
    for row in all_users:
        all_pics[row[0]] = find_pic(row[0])

    return render_template('posts.html',
                           all_jokes=list_to_html(all_jokes),
                           all_users=all_users,
                           all_user_votes=all_user_votes,
                           all_pics=all_pics,
                           all_comments=list_to_html(all_comments),
                           messages=messages)


@app.route('/comment/<joke_id>', methods=["POST"])
@login_required
def comment(joke_id):
    """Add comment to a joke"""

    comment = request.form['comment']

    # add comment to database
    connection = sqlite3.connect('phun.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO comments (comment, user_id, joke_id, c_username) VALUES (?, ?, ?, ?)',
                    [comment, session['user_id'], joke_id, session['username']])
    # retrieve the comment_id of the row that have just been inserted
    # if two people are using different cursors, that should be transaction safe
    comment_id = cursor.lastrowid

    connection.commit()
    connection.close()

    info = {
        'user_id': session['user_id'],
        'username': session['username'],
        'ppic': find_pic(session['user_id']),
        'comment_id': comment_id
    }
    return jsonify(info)


@app.route('/delete/<stuff>', methods=["POST"])
@login_required
def delete_post(stuff):

    connection = sqlite3.connect('phun.db')
    cursor = connection.cursor()

    if stuff == 'joke':

        joke_id = request.form['joke_id']
        cursor.execute('DELETE FROM jokes WHERE id = ?', [joke_id])

        # the joke that user wants to delete may or may not have comments and votes,
        # so the try except clause prevents the server from crashing
        try:
            cursor.execute('DELETE FROM comments WHERE joke_id = ?', [joke_id])
            cursor.execute('DELETE FROM votes WHERE joke_id = ?', [joke_id])
        except:
            pass

    if stuff == 'comment':

        comment_id = request.form['comment_id']
        cursor.execute('DELETE FROM comments WHERE comment_id = ?', [comment_id])

    if stuff == 'account':

        # delete user from the users table and anything else that may exist related to him
        cursor.execute('DELETE FROM users WHERE id = ?', [session['user_id']])
        try:
            cursor.execute('DELETE FROM jokes WHERE user_id = ?', [session['user_id']])
            cursor.execute('DELETE FROM comments WHERE user_id = ?', [session['user_id']])

            # fetchall() returns a list of tupples
            jokes_ids = cursor.execute(f"SELECT joke_id FROM votes WHERE user_id = {session['user_id']}").fetchall()
            # so even when iterating over the results, in order to get a 'clean' data
            # we must index into the first and only element of each tupple inside the list
            for joke_id in jokes_ids:
                cursor.execute("UPDATE jokes SET rating = (SELECT COUNT() FROM votes WHERE user_id != (?) AND joke_id = (?)) WHERE id = (?)",
                                [session['user_id'], joke_id[0], joke_id[0]])

            cursor.execute('DELETE FROM votes WHERE user_id = ?', [session['user_id']])
        except:
            pass

        connection.commit()
        connection.close()

        erase_picture(find_pic(session['user_id']))
        session.clear()
        flash("&#128557; Baby please don't go &#128557;", 'alert-info')
        return redirect('/login')

    connection.commit()
    connection.close()

    # that's how we properly return 'None'
    return ('', 204)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget user id and any other information stored in session, but keep flashed messages
    # flashes = session.pop('_flashes', None)
    # session.clear()
    # if flashes:
    #     session['_flashes'] = flashes

    if request.method == 'POST':

        if not request.form.get('username/email'):
            flash("&#128529; Missing username or e-mail &#128529;", "alert-danger")
            return redirect("/login")
        if not request.form.get('password'):
            flash("&#128529; Missing password &#128529", "alert-danger")
            return redirect("/login")

        connection = sqlite3.connect('phun.db')
        cursor = connection.cursor()

        # ensure credentials are correct(fetchone() grabs one result from the query's output and returns a tupple)
        query = cursor.execute('SELECT * FROM users WHERE username = ?',
                                [request.form.get('username/email')]).fetchone()
        if not query:
            query = cursor.execute('SELECT * FROM users WHERE email = ?',
                                    [request.form.get('username/email')]).fetchone()
        if not query or not check_password_hash(query[2], request.form.get('password')):
            flash('&#128528; Invalid username, e-mail and/or password &#128528;', 'alert-danger')
            connection.close()
            return redirect('/login')

        # remember which user has logged in
        session["user_id"] = query[0]
        session['username'] = query[1]
        session['email'] = query[3]
        connection.close()
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        inputs = request.form
        # cool one line if else statement
        all = True if len(inputs) == 4 else False
        feedback = give_feedback(inputs, inputs.keys(), all)

        # that is, if not all inputs are valid
        for key in feedback:
            if feedback[key] != '&#129303; Perfect &#129303;':
                return jsonify(feedback)

        # that is, if user is not submitting the whole form
        if not all:
            return jsonify(feedback)

        # never store plaintext password
        password = generate_password_hash(inputs['password'])

        connection = sqlite3.connect('phun.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?)",
                        [inputs['username'], password, inputs['email'],])

        connection.commit()
        connection.close()

        flash("&#128526; Registration succesfull! &#128526;", "alert-success")
        return jsonify('200 OK')

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # forget any information stored in session
    session.clear()
    flash("&#128546; You are logged out &#128546;", "alert-info")
    return redirect("/")
