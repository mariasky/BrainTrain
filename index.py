from flask import Flask, jsonify, render_template, request
from sassutils.wsgi import SassMiddleware
from flask_mysqldb import MySQLdb
import random
app = Flask(__name__)
app.config.from_object(__name__)
db = 0

#array of available boards
boards = []
#id of selected board
curboard = 0
#current round time
time = 0
#if saving is needed
saveToDB = 0

def init_db():
    global db
    if not db :
        db =MySQLdb.connect("localhost", "root", "root", "BrainTrain")    
    

#get settinf of all the boards
def get_board_items():
    init_db()
    curs = db.cursor()
    try:
        curs.execute("SELECT * FROM Border")
        rv = curs.fetchall()
    except:
        return "Error: unable to fetch items"
    return rv

#read list of champions for current board
def get_champion_items():
    init_db()
    curs = db.cursor()
    try:
        curs.execute("SELECT ChampionId, ChampionName, ChampionTime FROM Champion WHERE ChampionBoardId  = %s ORDER BY ChampionTime LIMIT 10", (str(curboard)))
        rv = curs.fetchall()
    except:
        return "Error: unable to fetch items"
    return rv

#find board size by id
def get_board_size(idn):
    global boards
    res = 1
    if not len(boards) : 
        boards = get_board_items()
    for board in boards:
        if board[0] == idn:
            res = board[2]
    return res

#row[0] = id, row[1] = name, row[2] = time
def champions_normalize(data, add=False):
    global time
    s = len(data)
    dt  = list(data)
    if add:
        if data[s-1][2]>time:
            global saveToDB 
            saveToDB = 1
            row = []
            row.append(0)
            row.append('')
            row.append(time)                
            dt.append(list(row))
            dt = sorted(dt, key=lambda user: user[2]) 
    if len(dt)<10:
         for i in range(10-len(dt)):
             row = []
             row.append(-1)
             row.append('')
             row.append(0)
             dt.append(list(row))   
    return dt

#generating training board elements for selected size
def board_gen(size=5):
    cont = []
    val=1
    for index in range(size*size):
        cont.append(val)
        val = val+1
    random.shuffle(cont)
    return cont

#call template for generated board
@app.route('/mboard/<size>', methods=['GET'])
def show_board_href(size):
    global curboard
    curboard = int(size)
    ln = get_board_size(curboard)
    data = board_gen(ln)
    return render_template('board.html', size=ln, nums=data, cur = 1)


#show best score for selected board
@app.route('/champion', methods=['GET'])
def show_champion():
    data = get_champion_items()
    data = champions_normalize(data, True)
    return render_template('champions.html', data=data, submit=saveToDB)
    #return jsonify(data)
 
#show best score for selected board
@app.route('/champion', methods=['POST'])
def save_champion():    
    name = request.form["champion_name"]
    sql="INSERT Champion(ChampionName, ChampionBoardId, ChampionTime) VALUES(%s, %s, %s)" 
    init_db()
    curs = db.cursor()
    curs.execute(sql, (name, curboard, time))
    db.commit()
    data = get_champion_items()
    data = champions_normalize(data, False)
    return render_template('champions.html', data=data, submit=0 )

@app.route('/settime', methods=['POST'])
def set_time(): 
    global time   
    time = int(request.form['time'])
    return 1

@app.route('/')
def start():
    global boards
    if not len(boards) : 
        boards = get_board_items()
    return render_template('index.html', data=boards)
   # return jsonify(data)

if __name__ == "__main__":
    app.run()
    #unittest.main()

