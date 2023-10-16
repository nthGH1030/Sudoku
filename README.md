# Sudoku
This is a web application of sudoku written in Flask for backend and HTML for frontend

To do List
1. Refactor the code to separate the "app definition" and "routes"
2. Implement a 9x9 grid system which takes user input and display the question and answer in 9x9 grid

how to make a question an answer 9x9 grid
the first workable version of the game
- make the question into a dictionary (done)
- make the answer into a dictionary (done)
- Get the userinput and assign it to a dictionary in flask (done)
- check if the userinput match the answer, handle correct and incorrect message (Done)
- display the real answer in answer(done)
- Highlight the answer input that is wrong (done)
- Highlight the question inside the answer in different color (done)

Implement data-base
- create tables that save question, answer and user id in schema (done)


- The database shall pre-load solve() to save question and answers before app launch (done)

- replace the sessions implementation inside the script and use database to get question and answers

Implement register and login
- implement user login and logout using session

Additioanl feature
- Add a button in "game" page that allow the question to be reset
