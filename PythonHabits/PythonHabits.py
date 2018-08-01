#!/usr/bin/env python
import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from tabledef import *

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "user_info.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


class Habit(db.Model):
    """docstring for Habit"""
    habit_title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Habits: {}".format(self.habit_title)


class Daily(db.Model):
    """docstring for Daily"""
    daily_title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Dailies: {}".format(self.daily_title)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        habit = Habit(habit_title=request.form.get("habit_title"))
        db.session.add(habit)
        db.session.commit()

        daily = Daily(daily_title=request.form.get("daily_title"))
        db.session.add(daily)
        db.session.commit()

    habits = Habit.query.all()
    dailies = Daily.query.all()
    
    return render_template("home.html", habits=habits, dailies=dailies)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)

### Original Code (mostly) ###
# engine = create_engine('sqlite:///user_info.db', echo=True)

# class Item(db.Model):
#     """Parent Class for Habits, Dailies, To-Dos and Rewards"""

#     title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

#     def __repr__(self):
#         return "<Title: {}>".format(self.title)
# 
# 
# @app.route('/', methods=["GET", "POST"])
# def home():
#     if not session.get('logged_in'):
#         return render_template('main.html')
#     else:
#         return "Congrats - you've logged in!! <a href='/logout'>Logout</a>"

#     if request.form:
#         habit = Habit(title=request.form.get("title"))

#         db.session.add(habit)
#         db.session.commit(all)
#         habits = Habit.query.all()

#         return render_template("main.html", habits=habits)


# @app.route('/login', methods=["POST"])
# def do_admin_login():

#     POST_USERNAME = str(request.form['username'])
#     POST_PASSWORD = str(request.form['password'])

#     Session = sessionmaker(bind=engine)
#     s = Session()
#     query = s.query(User).filter(User.username.in_(
#         [POST_USERNAME]), User.password.in_([POST_PASSWORD]))
#     result = query.first()

#     if result:
#         session['logged_in'] = True
#     else:
#         flash('please enter the correct user info.')

#     return home()

# if __name__ == '__main__':
#     app.secret_key = os.urandom(12)
#     app.run(debug=True, host='0.0.0.0', port=5000)
