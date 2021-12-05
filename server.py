"""Server for creating time entryes."""
from time import time
from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db
import crud
import os
import sys
from jinja2 import StrictUndefined
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import datetime
import json


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

cloud_name = os.environ['CLOUDINARY_CLOUD_NAME']
cloud_api = os.environ['CLOUDINARY_API_KEY']
cloud_api_secret = os.environ['CLOUDINARY_API_SECRET']

cloudinary.config(
    cloud_name=cloud_name,
    api_key=cloud_api,
    api_secret=cloud_api_secret
)


@app.route('/')
def show_homepage():
    """Homepage."""

    return render_template('login.html')


@app.route('/user_registration_route')
def route_to_registration_page():
    """Takes user to the registration page."""

    return render_template("user_registration.html")


@app.route('/user_registration', methods=['POST'])
def user_reg_post_intake():
    """Takes user registration info and makes yummy cookies."""

    print('In user registration app route at top.')

    email = request.form.get('email')
    password = request.form.get('password')
    print(password)
    fname = request.form.get('fname')
    print(fname)
    lname = request.form.get('lname')
    print(lname)

    photo = 'photo text place holder'
    print(email)
    email_check = crud.check_if_valid_user(email)

    if password == "":
        flash("You must enter in a password.")
        return redirect('user_registration_route')

    if fname == "":
        flash("You must enter in your first name.")
        return redirect('user_registration_route')

    if lname == "":
        flash("You must enter in your last name.")
        return redirect('user_registration_route')

    if email_check:
        if email != "":
            flash("A user already exists with that email.  Please try a different email")
        else:
            flash("You must enter in an email address.")
        return redirect('user_registration_route')
    else:
        create_user = crud.create_user(email, password, fname, lname, photo)
        flash("Please log in.")
        return render_template('/login.html', create_user=create_user, fname=fname, email=email, lname=lname, photo=photo)


@app.route('/login_form', methods=['POST'])
def login_form():
    """Processes login and checks for user in database."""

    password = request.form.get('password')
    email = request.form.get('email')

    fname = crud.get_users_fname(email)

    session['fname'] = fname
    session['email'] = email

    email_check = crud.check_if_valid_user(email)
    password_check = crud.password_check(email, password)
    if email == "" or password == "":
        flash("Sorry that is not a valid login email or password.")
        return redirect('/')
    elif email_check and password_check:
        time_entry_list = crud.get_time_entry_object_list(email)
        date = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year
        print('month-date-year =', month, date, year)
        time_entry_by_date = crud.get_time_entries_for_date_selected(
            email, date, month, year)
        session['time_entry_by_date'] = time_entry_by_date
        return render_template("calendar.html", time_entry_by_date=time_entry_by_date, time_entry_list=time_entry_list)
    else:
        flash("Sorry that is not a valid login email or password.  Please try again, or register as a new user.")
        return redirect('/')


@app.route('/calendar', methods=["POST", "GET"])
def go_to_user_calendar_page():
    """Takes user to their calendar page."""

    email = session['email']
    month = 'September'
    date = 3
    year = 2022

    time_entry_by_date = crud.get_time_entries_for_date_selected(
        email, date, month, year)
    print('time-entries-by date ===', time_entry_by_date)
    session['time_entry_by_date'] = time_entry_by_date

    return render_template("calendar.html", time_entry_by_date=time_entry_by_date)


@app.route('/day_calendar')
def go_to_user_day_calendar_page():
    """Takes user to their day calendar page using date selected on month calendar page."""

    email = session['email']

    return render_template("dayCalendar.html")


@app.route('/time_entry_creation', methods=["POST"])
def create_time_entry():
    """Creates time entry."""

    email = session['email']
    # date_selected = request.form.get('date')
    # month_selected = request.form.get('month')
    # year_selected = request.form.get('year')
    time_hr_to_add = str(request.form.get('hours'))
    time_min_to_add = str(request.form.get('minutes'))

    time_entry = time_hr_to_add + ":" + time_min_to_add
    print('time entry ======= ', time_entry, type(time_entry))
    comments = request.form.get('comments')

    time_entered = crud.create_time_entry(email, time_entry, comments)

    return redirect(url_for('view_created_time_entry'))


@ app.route('/time_entry_added')
def view_created_time_entry():
    """Takes user to created time entry page."""

    email = session['email']

    # time_entry_by_date = crud.get_time_entries_for_date_selected(
    #     email, date_selected, month_selected, year_selected)
    # print('time_entry_by_date on save and complete time entry server.py =',
    #       time_entry_by_date)
    time_entry_object_list = crud.get_time_entry_object_list(email)
    print('time_entry_object_list', time_entry_object_list)
    # session['time_entry_by_date'] = time_entry_by_date

    return render_template("calendar.html", email=email, time_entry_object_list=time_entry_object_list)


@ app.route("/delete_time_entry/<time_entry_id>")
def delete_time_entry_from_calendar(time_entry_id):
    """Deletes a selected time entry."""

    delete_time_entry = crud.delete_time_entry(time_entry_id)
    app.logger.info("delete_time_entry just called,", delete_time_entry)
    email = session['email']
    user_id = crud.get_user_id(email)
    time_entry_list = crud.get_time_entry_object_list(email)

    return redirect("/calendar")


@ app.route("/edit_time_entry")
def edit_time_entry_form(time_entry_id):
    """Takes user to page to correct/change/edit time entry."""

    email = session['email']
    time_entry_object = crud.get_time_entry_object(email, time_entry_id)

    return render_template("edit_time_entry.html", time_entry_object=time_entry_object)


@ app.route('/admin_page')
def admin_page():
    """Checks admin access rights and if admin, takes administrator to the admin management page."""

    email = session['email']
    admin_check = crud.admin_check(email)

    if admin_check:
        if admin_check != True:
            flash("Sorry you do not have administration privelages.  If you believe this to be a mistake, please contact your admin team.")
        else:
            return render_template("admin.html")


if __name__ == '__main__':

    connect_to_db(app)

    app.run(host='0.0.0.0', debug=False, use_reloader=True)
