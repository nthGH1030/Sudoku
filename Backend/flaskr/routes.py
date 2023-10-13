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

    #print(questionGrid)
    #print(squares)
    #print(answerGrid)
    
    if request.method == "POST":
        userAnsDict = {}
        for square in squares:
            userAnsDict[square] = request.form[square]
        #print(userAnsDict)

        if answerGrid == userAnsDict:
            message = "Congrats your answer is correct"
        else:
            message = "Your answer is incorrect"

        session["userAnsDict"] = userAnsDict
        session["message"] = message
        
        return redirect(url_for("routes.answer"))
    
    else:
        #check what the answer is in console
        print(answerGrid)
        return render_template("game.html", questionGrid = questionGrid, rowInitial = rowInitial, colInitial = colInitial)

@bp.route("/answer", methods= ["POST","GET"])
def answer():
    rowInitial = "ABCDEFGHI"
    colInitial = "123456789"
    
    userAnsDict = session.get("userAnsDict")
    message = session.get("message")
    questionGrid = session.get("questionGrid")
    answerGrid = session.get("answerGrid")

    

    return render_template("answer.html", userAnsDict = userAnsDict, message = message, 
                           answerGrid = answerGrid, questionGrid = questionGrid
                           ,rowInitial = rowInitial, colInitial = colInitial)

