from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL
import math
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configuring the app to run at flask server
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connecting the database to the appication
db = SQL("sqlite:///sports.db")


# Base route
@app.route("/")
def index():
    #return render_template("index.html")
    return redirect("/leaderboard")


# Login redirect page
@app.route("/login")
def login():
    #return render_template("login.html")
    return redirect("/institute-login")


# Login as student
'''@app.route("/student-login", methods=["GET", "POST"])
def student_login():

    """ Clearing currently logged in user """
    session.clear()

    # Check if user reached via post
    if request.method == "POST":
        # Check for the credentials
        return render_template("student_login.html")

    else:
        return render_template("student_login.html")'''


# Login as institute
@app.route("/institute-login", methods=["GET", "POST"])
def insti_login():

    """ Clearing currently logged in user """
    session.clear()

    # Check if user reached via post
    if request.method == "POST":
        # Check for the credentials
        # Query database for institute name
        rows = db.execute(
            "SELECT * FROM institute WHERE insti_name = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("insti_login.html", wrong=1)

        # Remember which user has signed in
        session["user_id"] = rows[0]["id"]

        # Return to home screen
        return redirect("/")

    # User reached via GET
    else:
        return render_template("insti_login.html")


# Register redirect page
@app.route("/register")
def register():
    #return render_template("register.html")
    return redirect("/institute-register")


# Register as student
'''@app.route("/student-register", methods=["GET", "POST"])
def student_register():

    # Check if user reached via post
    if request.method == "POST":
        # Check for the credentials
        return render_template("student_register.html")

    else:
        return render_template("student_register.html")'''


# Register as institute
@app.route("/institute-register", methods=["GET", "POST"])
def insti_register():

    # Check if user reached via post
    if request.method == "POST":
        ''' Register the institute '''

        # Ensure institute isnt already registered
        data = db.execute("SELECT insti_name FROM institute")

        # Looping over all the availabe institue names
        for name in data:
            if name["insti_name"].lower() == request.form.get("username").lower():
                return render_template("institute_register.html", exist=1)

        # Ensure the password and confirmation are same
        if request.form.get("password") != request.form.get("confirm_password"):
            return render_template("institute_register.html", password=1)

        # Generating password hash
        hash = generate_password_hash(request.form.get("password"))

        # Inserting new user
        db.execute(
            "INSERT INTO institute (insti_name, hash) VALUES (?,?)",
            request.form.get("username"),
            hash
        )

        return redirect("/")

    # User reached via GET
    else:
        return render_template("institute_register.html")


@app.route("/logout")
def logout():
    """" For user logout """

    session.clear()

    return redirect("/")


@app.route("/insti-admin")
@login_required
def insti_admin():

    # Retriving all the sports the current institute is registered for
    data = db.execute(
        "SELECT sport FROM sport_reg, institute WHERE institute.id = ? AND institute.insti_name = sport_reg.insti_name",
        session["user_id"]
        )

    # Passing all the sports to the html file
    return render_template("insti_admin.html", data=data)


@app.route("/view_sport")
@login_required
def viewsport():
    """ Returning user to registered sport screen """

    return redirect("/insti-admin")


@app.route("/add_sport", methods=["POST","GET"])
@login_required
def addsport():
    """ Allowing institute admins to add sports they are participating for """

    # User reached via POST
    if request.method == "POST":
        # Retriving sports currently registered for
        data = db.execute(
            "SELECT sport FROM sport_reg as sr, institute as i WHERE sr.insti_name = i.insti_name AND i.id = ?",
            session["user_id"]
            )

        # Checking if already registered
        for element in data:
            if element["sport"].lower() == request.form.get("sport").lower():
                return render_template("add_sport.html", exists=1)

        # Retriving the current institue name
        name = db.execute(
            "SELECT insti_name FROM institute WHERE id = ?",
            session["user_id"]
            )

        # Adding sport to the database
        db.execute(
            "INSERT INTO sport_reg (insti_name, sport) VALUES (?, ?)",
             name[0]["insti_name"],
             request.form.get("sport")
             )

        return redirect("/view_sport")

    # User reached via GET
    else:
        return render_template("add_sport.html")


@app.route("/rem_sport", methods=["POST", "GET"])
@login_required
def rem_sport():
    """ Allowing institute to remove a sport earlier registered for """

    # User reached via post
    if request.method == "POST":
        # Ensuring user selected a sport
        if not request.form.get("sport"):
            # Retriving sports currently registered for
            data = db.execute(
            "SELECT sport FROM sport_reg as sr, institute as i WHERE sr.insti_name = i.insti_name AND i.id = ?",
             session["user_id"]
             )

            return render_template("rem_sport.html", data=data, not_sel=1)

        # Retriving the current institue name
        name = db.execute(
            "SELECT insti_name FROM institute WHERE id = ?",
            session["user_id"]
            )

        # Deleting the selected sport
        db.execute(
            "DELETE FROM sport_reg WHERE sport = ? AND insti_name = ?",
            request.form.get("sport"),
            name[0]["insti_name"]
            )

        return redirect("/view_sport")

    # User reached via get
    else:
        # Retriving sports currently registered for
        data = db.execute(
            "SELECT sport FROM sport_reg as sr, institute as i WHERE sr.insti_name = i.insti_name AND i.id = ?",
             session["user_id"]
             )

        return render_template("rem_sport.html", data=data)


@app.route("/leaderboard", methods=["GET", "POST"])
def leader():
    # User reached via POST
    if request.method == "POST":
        """ Loading the leaderboard """

        # Retriving all the unique sports
        data = db.execute("SELECT DISTINCT sport FROM sport_reg")

        # Checking if user didnt pass an input
        if not request.form.get("sport"):
            return redirect("/leaderboard")

        # Selecting scores related to the sport chosen by the user
        scores = db.execute(
            "SELECT insti_name, sport, score FROM sport_reg WHERE sport = ? ORDER BY score DESC",
              request.form.get("sport")
              )

        return render_template("leader.html", data=data, scores=scores, table=1)


    # User reached via GET
    else:
        # Retriving all the unique sports
        data = db.execute("SELECT DISTINCT sport FROM sport_reg")

        # Selecting overall scores
        scores = db.execute("SELECT insti_name, SUM(score) as total FROM sport_reg GROUP BY insti_name ORDER BY total DESC")

        return render_template("leader.html", data=data, scores=scores, table=0)


@app.route("/list_tourney", methods=["GET", "POST"])
def list_tourney():
    """ Showing List of currently running tourney """

    # User reached via POST
    if request.method == "POST":
        # If user selected a location
        if request.form.get("location"):
            # Retriving tournaments running at the selected location
            data = db.execute(
            "SELECT insti_name, name_of_tourney, sport, location, prize_pool FROM tournament WHERE location = ?",
              request.form.get("location")
              )

        else:
            # Retriving all the currently running tourney
            data = db.execute("SELECT insti_name, name_of_tourney, sport, location, prize_pool FROM tournament")

        # Retriving all the different locations tournaments are running at
        locations = db.execute("SELECT DISTINCT location FROM tournament")

        return render_template("list_tourney.html", locations=locations, data=data)

    # User reached via GET
    else:
        # Retriving all the currently running tourney
        data = db.execute("SELECT insti_name, name_of_tourney, sport, location, prize_pool FROM tournament")

        # Retriving all the different locations tournaments are running at
        locations = db.execute("SELECT DISTINCT location FROM tournament")

        return render_template("list_tourney.html", data=data, locations=locations)


@app.route("/create_tourney", methods=["GET", "POST"])
@login_required
def create():
    """ Allowing user to create torunament """

    # User reached via POST
    if request.method == "POST":
        # Retriving current institute name
        name = db.execute("SELECT insti_name FROM institute as i WHERE i.id = ?", session["user_id"])

        # Rounding the prize to the floor value
        prize = math.floor(float(request.form.get("prize")))

        # Adding the tournament to list of live tournaments
        db.execute(
            "INSERT INTO tournament (insti_name, name_of_tourney, sport, location, prize_pool) VALUES (?, ?, ?, ?, ?)",
            name[0]["insti_name"],
            request.form.get("name_tourney"),
            request.form.get("sport"),
            request.form.get("location"),
            prize
            )

        return redirect("/list_tourney")

    # User reached via GET
    else:
        # Retriving all the sports institute has registered for
        sports = db.execute(
            "SELECT DISTINCT sport FROM sport_reg as sr, institute as i WHERE sr.insti_name = i.insti_name AND i.id = ?",
              session["user_id"]
              )

        return render_template("create_tourney.html", sports=sports)


@app.route("/rem_tourney", methods=["GET", "POST"])
@login_required
def rem_tourney():
    """ Allowing user to remove tournament """

    # User reached via POST
    if request.method == "POST":
        # Retrivng name of currently logged in institute
        name = db.execute("SELECT insti_name FROM institute as i WHERE i.id = ?", session["user_id"])

        # Removing the tournament
        db.execute(
            "DELETE FROM tournament as t WHERE t.insti_name = ? AND t.name_of_tourney = ?",
              name[0]["insti_name"],
              request.form.get("name_tourney")
              )

        return redirect("/list_tourney")

    # User reached via GET
    else:
        # Retriving the name of currently logged in institute
        name = db.execute("SELECT insti_name FROM institute as i WHERE i.id = ?", session["user_id"])

        # Retriving name of all currently live tournaments from the institute
        tourneys = db.execute(
            "SELECT name_of_tourney FROM tournament as t WHERE t.insti_name = ?",
             name[0]["insti_name"]
             )

        return render_template("rem_tourney.html", tourneys=tourneys)


@app.route("/prize")
def points():
    """ For explaining the points distribution system """

    return render_template("prize.html")


@app.route("/link_tut")
def link_tut():
    """ Links to tutorials and information to various sports """

    return render_template("link_tut.html")


@app.route("/link_shop")
def link_shop():
    """ Links to various shops to purchase sports equipments """

    return render_template("link_shop.html")


@app.route("/contact")
def contact():
    """ Giving contact information to user """

    return render_template("contact.html")
