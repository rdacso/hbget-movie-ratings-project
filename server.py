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


@app.route('/')
def index():
    """Homepage."""
 
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register')
def user_signin():
    """User sign in form."""
    
    return render_template('user_form.html')

@app.route('/register',methods=['POST'])
def register_process():
    """User sign in form."""

    email = request.form.get('email')
    password = request.form.get('password')

   
    existing_user = User.query.filter_by(email=email).first()

    if not existing_user:
        flash("Try Again.")
        return render_template("testuser.html")
    
    if not password != password:
        flash("Try again.")
        return render_template("testuser.html")

    session["user_id"] = existing_user.user_id

    # make query to check if email already in db
        # if there log them(add new_user to the session) in and redirect 


    new_user  = User(email=email, password=password)
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




    db.session.add(new_user)
    db.session.commit()
    # return redirect('/',username=username, password=password)





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000)
