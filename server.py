"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify,render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/')
def index():
    """Homepage."""
    #show homepage.html template
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    #query and display all users in database
    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register')
def user_signin():
    """User sign in form."""
    
    return render_template('user_form.html')

@app.route('/register',methods=['POST'])
def register_process():
    """User sign in form."""


    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    age = request.form["age"]
    zipcode = request.form["zipcode"]


    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("You have been added! Please log in.")
    return redirect("/")

# add user to the db
 # commit the new user
 # log them in and redirect (add to new_user to the session)

    # if not user:
    #     flash("No such email address.")
    #     return redirect('/register')

    # if user.password != password:
    #     flash("Incorrect password.")
    #     return redirect("/register")

    # # session["logged_in_customer_email"] = user.username
    # # flash("Logged in.")
    # return redirect("/")

    # error = None
    # if request.method == 'POST':
    #     if request.form['username'] != 'username' or \
    #             request.form['password'] != 'password':
    #         error = 'Invalid credentials'
    #     else:
    #         flash('You were successfully logged in')
        

    # for user in users:
    #     username  = User.query.get(1)
    #     if username not in users:
    #         ratings.make_new_user(username, password)




    # return redirect('/',username=username, password=password)

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/login')
def login():
    """Log In."""

    
    flash("Logged In.")
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def confirm():
    """Log In."""

    email = request.form["email"]

    user = User.query.filter_by(email=email).one()

    session["user_id"] = user.user_id
    flash("Logged In.")
    return redirect("/users/" + str(user.user_id))


@app.route('/users/<user_id>')
def user_info(user_id):
    """shows user info"""

    user = User.query.filter_by(user_id=user_id).one()


    return render_template("user_info.html", user=user)

@app.route('/movies')
def show_movies():

    """Shows list of movies"""

    movies = Movie.query.order_by(Movie.title).all()

    return render_template("movielist.html", movies=movies)


@app.route('/movies/<movie_id>')
def show_movie_details(movie_id):

    """Shows movie details"""

    movie = Movie.query.filter_by(movie_id=movie_id).one()

    return render_template("movie-detail.html", movie=movie)


@app.route('/ratemovie')
def rate_movie():
    """Movie rating form"""
    
    return render_template("movie-detail.html", movie=movie)

@app.route('/ratemovie',methods=['POST'])
def rating_process():
    """Process movie rating form."""

    # Get form variables
    score = request.form["score"]
    movie_id = request.form['movie_id']
    #get user_id from existing session
    user_id = session.get('user_id')
    #create variable that calls the class Ratings and passes variables
    new_rate = Rating(score=score, movie_id=movie_id, user_id=user_id)
    #add new_rate to the database
    db.session.add(new_rate)
    #commit new_rate to the database
    db.session.commit()

    #check to see if user has already added score to database
    #If score already exists, update it
    #If score does not exist yet, add it to the database

    rating_query = Rating.query.filter(Rating.user_id==user_id, Rating.movie_id==movie_id).all()[0].score

    if rating_query.score[-1]:
        rating_query.score(new_rate)
        db.session.add(new_rate)
        db.session.commit()
    else:
        



   
  
    flash("Your score has been added!")



    return redirect("/movies")





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000)
