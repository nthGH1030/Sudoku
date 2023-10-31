# Project Title: A Sudoku web application
#### Video Demo:  <https://youtu.be/rF9J_fnLKrw>
#### Description:

This is a web application of sudoku written in Flask for backend and HTML for frontend for the purpose of a CS50 final project

-----Keynote of the project-------

5 html pages will be diaplyed to users:
1. 1 Page for user to register account
2. 1 Page for user to login account
3. 1 Page of index page
4. 1 Page to show the question for user to play
5. 1 Page to compare user's answer to the model answer

Database
1. Sqlite database is used to handle username, password, storing quesetion and answers
2. Before the deployement of the application, a function inside "db.py" called "init_db" is run to preload 20 sets of random question and answer into the database and initialize the database


Sessions
1. User_id is handled by session as it stores the if of user for identification purpses
2. question_id is hanlded by session as it stores the random question generated for user which allow us to retrieve the answer for said quesiton in the database
3. user_ans is the answer submitted by user, which is used to compare with model answer from database to check for right and wrong answers and display to the user.

Hosting & deployment
1. The project is ready to be deployed onto google cloud app engine. For the purpose of submitted CS50 Final project, the video shown will have the app be run locally demonstrate its functionality.

----User journey-------

User journey
1. User is expected to reach the page through a HTTP link
2. User is expected to register and login an account before they can use the application
3. After login , user is expected to click the "Game" button at the top navigation bar and get a random question
4. The random question should contains unfilled square inside a 9x9 grid for user to solve
5. User shall click "Submit" after solving the question
6. User's submitted answer shall be checked for correct and incorrect answers in highlighted color and displayed
7. A model answer shall be displayed for reference
8. A messsage shall show whether the user submitted answer is correct or not

----Reference-------


Reference
1. Solving Every Sudoku Puzzle by Peter Norvig
https://norvig.com/sudoku.html
- Used in "solver.py" to generate Sudoku questions and answers