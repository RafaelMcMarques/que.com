import os
from flask import Flask, session, request, render_template, redirect, jsonify
import sqlite3

# configure aplication
app = Flask(__name__)

# configure session
app.secret_key = "bkdsh gdi1769231uh31 y9712"
@app.before_request
def make_session_permanent():
    session.permanent = True

# ensure responses are not cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# database path
db_path = os.path.dirname(os.path.abspath(__file__)) + "/que.db"

# app's url
url = "http://127.0.0.1:5000"

# home
@app.route("/")
def home():
    if "queue_id" in session:
        # redirect to management screen
        return redirect("/manage")

    if "user_id" in session:
        # redirect to waiting sreen
        return redirect("/wait")
    return render_template("index.html")        

# create new queue
@app.route("/create", methods=["POST", "GET"])
def create():
    if "queue_id" in session:
        # redirect to management screen
        return redirect("/manage")

    if "user_id" in session:
        # redirect to waiting sreen
        return redirect("/wait")

    if request.method == "GET": 
        return render_template("create.html")
    
    # check if a name was provided
    if not request.form.get("name"):
        return render_template("create.html")
    
    # connect to database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # insert into database
    name = request.form.get("name")
    message = None
    if request.form.get("message") :
        message = request.form.get("message")
    cur.execute("INSERT INTO queues (name, message) VALUES (?, ?)", (name, message,))
    queue_id = cur.lastrowid
    conn.commit()
    
    # close connection to databse
    cur.close()
    conn.close()

    # store in session that user is a queue owner
    session["queue_id"] = queue_id
    return redirect("/manage")

# manage queue
@app.route("/manage")
def manage_GET():
    # user not an owner of a queue
    if "queue_id" not in session:
        return redirect("/")
    
    # connect to database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    queue_id = str(session["queue_id"])

    # check if queue exists
    cur.execute("SELECT * FROM queues WHERE id = ?", [queue_id])
    if not cur.fetchall():
        cur.close()
        conn.close()
        session.clear()
        return redirect("/")

    # get first in queue
    cur.execute("SELECT name FROM users WHERE queue_id = ? AND position=1", [queue_id])
    first = cur.fetchall()
    if first:
        first = first[0][0]  

    # get number of people in queue
    cur.execute("SELECT COUNT(*) FROM users WHERE queue_id = ?", [queue_id])
    number_of_people = cur.fetchall()[0][0] - 1    
        
    # close connection to database
    cur.close()
    conn.close()

    return render_template("manage.html",queue_id=queue_id,first=first, number_of_people=number_of_people, url=url)

@app.route("/manage", methods=["POST"])
def manage_POST():
    # get queue id
    queue_id = str(session["queue_id"])

    # connect to database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # call next
    if request.form.get("next"):
        cur.execute("DELETE FROM users WHERE queue_id = ? AND position=1", [queue_id])
        conn.commit
        cur.execute("UPDATE users SET position = position - 1 WHERE queue_id = ?", [queue_id])
        conn.commit()

    # end queue 
    if request.form.get("end"):
        cur.execute("DELETE FROM users WHERE queue_id = ?", [queue_id])
        conn.commit()
        cur.execute("DELETE FROM queues WHERE id = ?", [queue_id])
        conn.commit()
        session.clear()

    # close connection to database
    cur.close()
    conn.close()
    return redirect("/manage")

# find a queue via its id
@app.route("/findque")
def findque():
    if "queue_id" in session:
        # redirect to management screen
        return redirect("/manage")

    if "user_id" in session:
        # redirect to waiting sreen
        return redirect("/wait")

    if not request.args.get("id"):
        return render_template("findque.html")

    id = request.args.get("id")

    # check if id is valid
    if not id.isdigit() :
        return render_template("findque.html") 
    
    # connect to database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # check if queue exists. If it does, get name
    cur.execute("SELECT name FROM queues WHERE id = ?", [id])
    name = cur.fetchall()
    if not name:
        cur.close()
        conn.close()
        return render_template("findque.html")
    name = name[0][0]

    # close connection to database
    cur.close()
    conn.close()

    # redirect to joining form
    queue_url = "/join?id=" + id + "&name=" + name
    return redirect(queue_url)

# render joining form
@app.route("/join")
def join_GET():
    if "queue_id" in session:
        # redirect to management screen
        return redirect("/manage")

    if "user_id" in session:
        # redirect to waiting sreen
        return redirect("/wait")

    if not request.args.get("id") or not request.args.get("name"):
        return redirect("/findque")
    id = request.args.get("id")
    name = request.args.get("name")
    return render_template("join.html", id=id, name=name) 

# join a que
@app.route("/join", methods=["POST"])
def join_POST():
    # get name and id
    id = request.form.get("id")
    name = request.form.get("name")
    if not name or not id:
        return redirect("/findque")

    # connect to database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # check if queue exists
    cur.execute("SELECT * FROM queues WHERE id = ?", [id])
    if not cur.fetchall():
        cur.close()
        conn.close()
        return redirect("/findque")

    # insert user into queue
    cur.execute("SELECT position FROM users WHERE queue_id = ? ORDER BY POSITION DESC LIMIT 1", [id])
    last_position = cur.fetchall()
    if not last_position:
        position = 1
    else:
        position = int(last_position[0][0]) + 1
    cur.execute("INSERT INTO users (name, position, queue_id) VALUES (?,?,?)", (name, position, id,))
    user_id = cur.lastrowid
    conn.commit()

    # store user id in session
    session["user_id"] = user_id

    # close connection to database
    cur.close()
    conn.close()
    return redirect("/wait")

# wait for turn
@app.route("/wait")
def wait():
    if "queue_id" in session:
        # redirect to management screen
        return redirect("/manage")

    if "user_id" not in session:
        return redirect("/")
    
    user_id = str(session["user_id"])

    # connect to database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # get user position
    cur.execute("SELECT position FROM users WHERE id = ?", [user_id])
    position = cur.fetchall()
    if not position:
        # user not in database
        session.clear()
        cur.close()
        conn.close()
        return redirect("/")
    position = position[0][0]

    # get queue name
    cur.execute("SELECT queue_id FROM users WHERE id = ?", [user_id])
    queue_id =  str(cur.fetchall()[0][0])
    cur.execute("SELECT name FROM queues WHERE id = ?", [queue_id])
    queue_name = cur.fetchall()[0][0]

    if position > 1:
        cur.close()
        conn.close()
        return render_template("wait.html", position=position, queue_name=queue_name)
    
    # its user's turn
    # get message
    cur.execute("SELECT message FROM queues WHERE id = ?", [queue_id])
    message = cur.fetchall()[0][0]
    cur.close()
    conn.close()
    return render_template("yourturn.html", queue_name=queue_name, message=message )

# exit queue
@app.route("/exit", methods=["POST"])
def exit():
    user_id = str(session["user_id"])
    
    # connect to database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # get queue id and user position
    cur.execute("SELECT queue_id, position FROM users WHERE id = ?", [user_id])
    results = cur.fetchall()
    if not results:
        cur.close()
        conn.close()
        return redirect("/")
    queue_id = results[0][0]
    position = results[0][1]

    # remove user
    cur.execute("DELETE FROM users WHERE id = ?", [user_id])
    conn.commit()

    # update positions
    cur.execute("UPDATE users SET position = position - 1 WHERE queue_id = ? AND position > ?", (queue_id, position,))
    conn.commit()

    # close connection to database
    cur.close()
    conn.close()
    session.clear()
    return redirect("/")

# clear session and redirect user to menu
@app.route("/back", methods=["POST"])
def end():
    session.clear()
    return redirect("/")

# return position of the user in queue, does not render a template
@app.route("/getPosition")
def getPosition():
    if "user_id" not in session:
        return jsonify({'position': None})

    user_id = str(session["user_id"])

    # connect to database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # get user position
    cur.execute("SELECT position FROM users WHERE id = ?", [user_id])
    position = cur.fetchall()
    if position:
        position = position[0][0]

    # close connection to database
    cur.close()
    conn.close()

    return jsonify({'position': position})
    
# get number of people in a queue, does not render a template
@app.route("/getPeople")
def getPeople():
    if "queue_id" not in session:
        return jsonify({'number': None})
    
    queue_id = str(session["queue_id"])

    # connect to database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # get number of people
    cur.execute("SELECT COUNT(*) FROM users WHERE queue_id = ?", [queue_id])
    number = cur.fetchall()
    if number:
        number = number[0][0]
    
    # close connection to databse
    cur.close()
    conn.close()

    return jsonify({'number': number})

if __name__ == "__main__":
    app.run()
