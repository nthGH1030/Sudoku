from flask import Flask, flash, redirect, render_template, request, session, url_for, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from . import solver


bp = Blueprint('routes',__name__)
#bp.secret_key = 'your_secret_key'

@bp.route("/", methods=["GET"])
def index():
    #If user click the "Game button", route them to "game"
    return render_template("index.html")

@bp.route("/game", methods= ["POST","GET"])
def game():

    rowInitial = "ABCDEFGHI"
    colInitial = "123456789"
    squares = []
    questionGrid = {}
    question = session.get("question")
    answer = session.get("answer")

    if "question" not in session or "answer" not in session:
        question, answer = solver.solve()
        session["question"] = question
        session["answer"] = answer

    question_index = 0
    for char in rowInitial:
        for digit in colInitial:
            squares.append(char + digit)
            questionGrid[char + digit] = question[question_index]
            question_index += 1

    print(questionGrid)
    #print(squares)
    
    if request.method == "POST":
        userAns = request.form["userAns"]
        answer = session["answer"]
        
        if answer == userAns:
            message = "Congrats your answer is correct"
        else:
            message = "Your answer is incorrect"

        session["userAns"] = userAns
        session["message"] = message
    
        return redirect(url_for("routes.answer"))
    
    else:
        #check what the answer is in console
        print(answer)
        return render_template("game.html", questionGrid = questionGrid, rowInitial = rowInitial, colInitial = colInitial)

@bp.route("/answer", methods= ["POST","GET"])
def answer():
    userAns = session.get("userAns")
    message = session.get("message")
    question = session.get("question")
    answer = session.get("answer")

    return render_template("answer.html", userAns = userAns, message = message, answer = answer, question = question)

