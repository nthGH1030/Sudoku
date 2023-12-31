from flask import flash, redirect, render_template, g,request, session, url_for, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
import random
import functools

bp = Blueprint('routes',__name__)

# Set up Key for dictionary
rowInitial = "ABCDEFGHI"
colInitial = "123456789"
squares = []
index = 0
for char in rowInitial:
    for digit in colInitial:
        squares.append(char + digit)
        index += 1

#Helper function to require user to login before playing the game
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('routes.index'))

        return view(**kwargs)

    return wrapped_view

#Helper function to check if user is still in session
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

#-----------------Routes--------------------------#
@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@bp.route("/game", methods= ["POST","GET"])
@login_required
def game():

    db = get_db()
    if "question_id" in session:
        question_id = session.get("question_id")
    
    #Get the question from database
    if request.method =="GET":
        question_id = random.randint(0, 19)
        session["question_id"] = question_id
        print(question_id)

        question_db = db.execute (
            'SELECT question_key , question_value FROM question'
            ' WHERE question_id = ?',
            (question_id,)
        ).fetchall()

        question_dict = {}
        for row in question_db:
            question_key = row['question_key']
            question_value = row['question_value']
            question_dict[question_key] = question_value
        print("this is question_dict from database")
        print(question_dict)

        answer_db = db.execute(
            'SELECT ans_key, ans_value FROM answer'
            ' WHERE question_id = ?',
            (question_id,)
        ).fetchall()

        answer_dict = {}
        for row in answer_db:
            answer_key = row['ans_key']
            answer_value = row['ans_value']
            answer_dict[answer_key] = answer_value

        print("This is the answer")
        print(answer_dict)

    # Get the answer from database, compare with user answer and post it 
    if request.method == "POST":
        userAnsDict = {}
        for square in squares:
            userAnsDict[square] = request.form[square]
        print("this is userdict")
        print(userAnsDict)

        answer_db = db.execute(
            'SELECT ans_key, ans_value FROM answer'
            ' WHERE question_id = ?',
            (question_id,)
        ).fetchall()

        answer_dict = {}
        for row in answer_db:
            answer_key = row['ans_key']
            answer_value = row['ans_value']
            answer_dict[answer_key] = answer_value
            
        print("This is the answer_dict from answer")
        print(answer_dict)
        

        if answer_dict == userAnsDict:
            message = "Congrats your answer is correct"
            print("correct")
        else:
            message = "Your answer is incorrect"
            print("incorrect")

        session["userAnsDict"] = userAnsDict
        session["message"] = message
        
        return redirect(url_for("routes.answer"))
        
    return render_template("game.html", question_dict = question_dict, 
                           rowInitial = rowInitial, colInitial = colInitial)

@bp.route("/answer", methods= ["POST","GET"])
@login_required
def answer():

    userAnsDict = session.get("userAnsDict")
    message = session.get("message")
    question_id = session.get("question_id")

    db = get_db()
    question_db = db.execute (
        'SELECT question_key , question_value FROM question'
        ' WHERE question_id = ?',
        (question_id,)
    ).fetchall()

    question_dict = {}
    for row in question_db:
        question_key = row['question_key']
        question_value = row['question_value']
        question_dict[question_key] = question_value
    #print("this is question_dict from database")
    #print(question_dict)

    answer_db = db.execute(
        'SELECT ans_key, ans_value FROM answer'
        ' WHERE question_id = ?',
        (question_id,)
    ).fetchall()

    answer_dict = {}
    for row in answer_db:
        answer_key = row['ans_key']
        answer_value = row['ans_value']
        answer_dict[answer_key] = answer_value
    #print("This is the answer_dict from answer")
    #print(answer_dict)


    return render_template("answer.html", userAnsDict = userAnsDict, message = message, 
                           answer_dict = answer_dict, question_dict = question_dict
                           ,rowInitial = rowInitial, colInitial = colInitial)

@bp.route("/register", methods= ["POST","GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for('routes.login'))

        flash(error)

    return render_template("register.html")

@bp.route("/login", methods= ["POST","GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('routes.index'))

        flash(error)

    return render_template("login.html")


#logout when session is cleared
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.index'))

