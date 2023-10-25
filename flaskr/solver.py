from flask import Flask, Blueprint, flash, redirect, render_template, request, session
import time, random
#from flaskr.db import get_db

def solve():
    def cross(A, B):
        "Cross product of elements in A and elements in B."
        return [a+b for a in A for b in B]

    digits   = '123456789'
    rows     = 'ABCDEFGHI'
    cols     = digits
    squares  = cross(rows, cols)
    unitlist = ([cross(rows, c) for c in cols] + 
                # peers in a column
                [cross(r, cols) for r in rows] +
                #peers in a row
                [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
                #peers in a 3x3 grid

    #Map each square to unitlist which contains the square in it
    units = dict((s, [u for u in unitlist if s in u]) 
                for s in squares)

    #Group the peers paired with their respective key in a dict, the dict value contains the square but excldue the square itself
    peers = dict((s, set(sum(units[s],[]))-set([s]))
                for s in squares)


    def parse_grid(grid):
        """Convert grid to a dict of possible values, {square: digits}, or
        return False if a contradiction is detected."""
        ## To start, every square can be any digit; then assign values from the grid.
        values = dict((s, digits) for s in squares)
        for s,d in grid_values(grid).items():
            if d in digits and not assign(values, s, d):
                return False ## (Fail if we can't assign d to square s.)
        return values


    def grid_values(grid):
        "Convert grid into a dict of {square: char} with '0' or '.' for empties."
        chars = [c for c in grid if c in digits or c in '0.']
        assert len(chars) == 81
        return dict(zip(squares, chars))

    def assign(values, s, d):
        """Eliminate all the other values (except d) from values[s] and propagate.
        Return values, except return False if a contradiction is detected."""
        
        other_values = values[s].replace(d,'')

        if all(eliminate(values, s, d2) for d2 in other_values):
            return values
        else:
            return False

    def eliminate(values, s, d):
        if d not in values[s]:
            return values ## Already eliminated
        
        values[s] = values[s].replace(d,'')

        ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
        if len(values[s]) == 0:
            return False ## Contradiction as there cannot be no possible value
        elif len(values[s]) == 1:
            d2 = values[s]
            if not all (eliminate(values, s2, d2) for s2 in peers[s]): ## if the elimination of the vale 'd2' does not cause contradiction in all peers
                return False
        ## (2) If a unit u is reduced to only one place for a value d, then put it there.
        for u in units[s]:
            dplaces = [s for s in u if d in values[s]]
            if len(dplaces) == 0:
                return False
            elif len(dplaces) == 1:
                # d can only be in one place in unit; assign it there
                if not assign(values, dplaces[0], d):
                    return False
        return values
    
    ################ Display as 2-D grid ################
    def display(values):
        "Display these values as a 2-D grid."
        width = 1+max(len(values[s]) for s in squares)
        line = '+'.join(['-'*(width*3)]*3)
        for r in rows:
            print (''.join(values[r+c].center(width)+('|' if c in '36' else '')for c in cols))
            if r in 'CF': 
                print(line)
        print

    ################ Search ################
    def solve(grid): return search(parse_grid(grid))
    def search(values):
        "Using depth-first search and propagation, try all possible values."
        if values is False:
            return False ## Failed earlier
        if all(len(values[s]) == 1 for s in squares):
            return values ## Solved!
        ## Chose the unfilled square s with the fewest possibilities
        n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
        return some(search(assign(values.copy(), s, d))
                    for d in values[s])
    
    ################ Utilities ################
    def some(seq):
        "Return some element of seq that is true."
        for e in seq:
            if e: return e
        return False

    def from_file(filename, sep='\n'):
        "Parse a file into a list of strings, separated by sep."
        return file(filename).read().strip().split(sep)

    def shuffled(seq):
        "Return a randomly shuffled copy of the input sequence."
        seq = list(seq)
        random.shuffle(seq)
        return seq

    def solve_all(grids, name='', showif=0.0):
        """Attempt to solve a sequence of grids. Report results.
        When showif is a number of seconds, display puzzles that take longer.
        When showif is None, don't display any puzzles."""
        def time_solve(grid):
            start = time.process_time()
            values = solve(grid)
            t = time.process_time()-start
            ## Display puzzles that take long enough
            if showif is not None and t > showif:
                display(grid_values(grid))
                if values: display(values)
                print ('(%.2f seconds)\n' % t)
            return (t, solved(values))
        times, results = zip(*[time_solve(grid) for grid in grids])
        N = len(grids)
        if N > 1:
            print ("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
                sum(results), N, name, sum(times)/N, N/sum(times), max(times)))

    def solved(values):
        "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
        def unitsolved(unit): return set(values[s] for s in unit) == set(digits)
        return values is not False and all(unitsolved(unit) for unit in unitlist)

    def random_puzzle(N=17):
        """
        Make a random puzzle with N or more assignments. Restart on contradictions.
        Note the resulting puzzle is not guaranteed to be solvable, but empirically
        about 99.8% of them are solvable. Some have multiple solutions.
        """
        values = dict((s, digits) for s in squares)
        for s in shuffled(squares):
            if not assign(values, s, random.choice(values[s])):
                break
            ds = [values[s] for s in squares if len(values[s]) == 1]
            if len(ds) >= N and len(set(ds)) >= 8:
                return ''.join(values[s] if len(values[s])==1 else '.' for s in squares)
        return random_puzzle(N) ## Give up and make a new puzzle

    def shuffled(seq):
        """Return a randomly shuffled copy of the input sequence."""
        seq = list(seq)
        random.shuffle(seq)
        return seq

    
    solve_all([random_puzzle() for _ in range(99)], "random", 100.0)
    question = random_puzzle()
    answer = search(parse_grid(question))
    # change . to 0
    returnQuestion = question.replace(".","0")

    returnAnswer =''

    for value in answer.values():
        returnAnswer += value

    #test for question
    print(returnQuestion)
    #test for answer
    print(returnAnswer)

    returnValue = [returnQuestion, returnAnswer]

    return returnValue
    

    


"""
#Route to get question and answer
def getAnsQuestion(question, answer):       
    db = get_db()
    db.execute(
    "INSERT INTO puzzle(question) VALUES(?)", (question,)
    )

    question_id_object = db.execute('SELECT id from puzzle where question = ?',(question,))
    for row in question_id_object:
        question_id = row[0]

    for k,v in answer.items():
        db.execute(
        "INSERT INTO answer(dict_key, dict_value, question_id) VALUES(?,?,?)", 
        (k,v, question_id)
        )

    '''   
    test = db.execute('SELECT * from answer')
    ans = list()
    for row in test:
        ans.append([row[0],row[1],row[2],row[3]])

    return ans
    '''

    test = db.execute('SELECT * from answer')
    ans = {"answer_id":[], "question_id":[], "square":[],"answer":[]}
    anslist= list()
    for row in test:
        ans["answer_id"]= row[0]
        ans["question_id"] = row[1]
        ans["square"] = row[2]
        ans["answer"] = row[3]
        anslist.append(ans.copy())
    return anslist
 
"""