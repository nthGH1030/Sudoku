from flask import (
    Blueprint,jsonify
)
#from flaskr.db import get_db

bp = Blueprint('solver', __name__)

@bp.route('/solve')
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

    def display(values):
        "Display these values as a 2-D grid."
        width = 1+max(len(values[s]) for s in squares)
        line = '+'.join(['-'*(width*3)]*3)
        for r in rows:
            print (''.join(values[r+c].center(width)+('|' if c in '36' else '')for c in cols))
            if r in 'CF': 
                print(line)
        print


    '''
    #testing for how unitlist function
    for square in [cross(rows, c) for c in cols]:
        print(square)
    print("this is the result of [cross(rows, c) for c in cols], showing peers in a column")

    for square in [cross(r, cols) for r in rows]:
        print(square)
    print("this is the result of [cross(r, cols) for r in rows], showing peers in a row")

    for square in [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]:
        print(square)
    print("this is the result of [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')], showing peers in the 3x3 square")
    '''
    '''
    #testing for how units and peers works
    def test():
        "A set of unit tests."s
        assert len(squares) == 81
        assert len(unitlist) == 27
        assert all(len(units[s]) == 3 for s in squares)
        assert all(len(peers[s]) == 20 for s in squares)
        assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                            ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                            ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
        assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                                'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                                'A1', 'A3', 'B1', 'B3'])
        return('All tests pass.')

    print(test())
    '''

    grid1 = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
    grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    #print(parse_grid(grid1))
    display(parse_grid(grid1))
    json = [parse_grid(grid1), grid1]
    
    testjson = getAnsQuestion(grid1, parse_grid(grid1))
    
    return jsonify(testjson)

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
 
