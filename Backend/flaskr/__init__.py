import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from . import solver

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(solver.bp)


@app.route("/", methods=["GET"])
def index():
    #If user click the "Game button", route them to "game"
    return render_template("index.html")

@app.route("/game", methods= ["POST","GET"])
def game():
    
    question = session.get("question")
    answer = session.get("answer")

    if "question" not in session or "answer" not in session:
        question, answer = solver.solve()
        session["question"] = question
        session["answer"] = answer

    
    if request.method == "POST":
        userAns = request.form["userAns"]
        answer = session["answer"]
        
        if answer == userAns:
            message = "Congrats your answer is correct"
        else:
            message = "Your answer is incorrect"

        session["userAns"] = userAns
        session["message"] = message
    
        return redirect(url_for("answer"))
    else:
        #check what the answer is in console
        print(answer)
        return render_template("game.html", question = question)

@app.route("/answer", methods= ["POST","GET"])
def answer():
    userAns = session.get("userAns")
    message = session.get("message")
    question = session.get("question")
    answer = session.get("answer")

    return render_template("answer.html", userAns = userAns, message = message, answer = answer, question = question)



if __name__ == "__main__":
    app.run()