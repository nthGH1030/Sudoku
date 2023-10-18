from flask import Flask, flash, redirect, render_template, request, session, url_for, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from . import solver
from flaskr.db import get_db
import random

bp = Blueprint('routes',__name__)

@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@bp.route("/game", methods= ["POST","GET"])
def game():
    '''
    rowInitial = "ABCDEFGHI"
    colInitial = "123456789"
    squares = []
    questionGrid = {}
    answerGrid = {}

    question = session.get("question")
    answer = session.get("answer")

    if "question" not in session or "answer" not in session:
        question, answer = solver.solve()
        session["question"] = question
        session["answer"] = answer

    index = 0
    for char in rowInitial:
        for digit in colInitial:
            squares.append(char + digit)
            questionGrid[char + digit] = question[index]
            answerGrid[char + digit] = answer[index]
            index += 1
    
    session["answerGrid"] = answerGrid
    session["questionGrid"] = questionGrid
    '''
    # thins that got run no matter its get or post
    rowInitial = "ABCDEFGHI"
    colInitial = "123456789"
    squares = []
    index = 0
    for char in rowInitial:
        for digit in colInitial:
            squares.append(char + digit)
            index += 1

    db = get_db()
    question_id = None

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

    # Get the answer from database, compare with user answer and post it 
    if request.method == "POST":
        userAnsDict = {}
        for square in squares:
            userAnsDict[square] = request.form[square]
        #print(userAnsDict)

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
        else:
            message = "Your answer is incorrect"

        session["userAnsDict"] = userAnsDict
        session["message"] = message
        
        return redirect(url_for("routes.answer"))

        #check what the answer is in console
        #print("this is the answer")
        #print(answerGrid)
        
    return render_template("game.html", question_dict = question_dict, 
                           rowInitial = rowInitial, colInitial = colInitial)

@bp.route("/answer", methods= ["POST","GET"])
def answer():

    userAnsDict = session.get("userAnsDict")
    message = session.get("message")

    rowInitial = "ABCDEFGHI"
    colInitial = "123456789"
    squares = []
    index = 0
    for char in rowInitial:
        for digit in colInitial:
            squares.append(char + digit)
            index += 1
    
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
    print("This is the answer_dict from answer")
    print(answer_dict)



    
    return render_template("answer.html", userAnsDict = userAnsDict, message = message, 
                           answer_dict = answer_dict, question_dict = question_dict
                           ,rowInitial = rowInitial, colInitial = colInitial)