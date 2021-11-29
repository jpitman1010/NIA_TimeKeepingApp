"""Server for creating time punches."""
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

    # print(request.files, "request-files image-upload")
    # file = request.files['image-upload']
    # app.logger.info('this is the file app logger', file)
    # response = cloudinary.uploader.upload(file)
    # photo = response['url']
    # app.logger.info('this is the photo app logger', photo)

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
        time_punch_list = crud.get_time_punch_object_list(email)
        return render_template("updated-library.html", time_punch_list=time_punch_list)
    else:
        flash("Sorry that is not a valid login email or password.  Please try again, or register as a new user.")
        return redirect('/')


@app.route('/calendar')
def go_to_user_calendar_page():
    """Takes user to their calendar page."""

    email = session['email']
    book_check = crud.check_database_for_completed_books(email)

    author_id = crud.get_user_id(email)
    books = crud.get_book_object_list(author_id)
    app.logger.info("books object-all", books)

    return render_template("calendar.html", books=books)


@app.route('/time_punch_creation', methods=["POST"])
def create_time_punch():
    """Creates time punch."""

    print("this is the start of post time punch creation route")

    email = session['email']
    comments = request.form.get('comments')
    time_punch = crud.create_time_punch(email, comments)
    app.logger.info(time_punch, "time punch")

    print("I am done pulling things from requests")

    time_punch_id = crud.get_time_punch_id(email)
    print("this is the time punch ID", time_punch_id)
    page_number = crud.get_page_number(page_id)

    return redirect(url_for('view_created_time_punch'))


@app.route('/time_punch/<time_punch_id>/add_time_punch/<db_time_punch>')
def view_created_time_punch(time_punch_id, db_time_punch):
    """Takes user to created time punch page."""

    return render_template('created_time_punch.html')


@app.route('/save_and_complete_time_punch')
def save_completed_time_punch():
    """Completes time punch creation and shows completed time punch in calendar."""

    email = session['email']
    comments = session['comments']
    time_punch_id = session['time_punch_id']
    user_id = crud.get_user_id(email)
    time_punch_object_list = crud.get_time_punch_object_list(email)

    return render_template("calendar.html", email=email, comments=comments, time_punch_id=time_punch_id, user_id=user_id, time_punch_object_list=time_punch_object_list)


@app.route("/delete_time_punch/<time_punch_id>")
def delete_time_punch_from_calendar(time_punch_id):
    """Deletes a selected time punch."""

    delete_time_punch = crud.delete_time_punch(time_punch_id)
    app.logger.info("delete_time_punch just called,", delete_time_punch)
    email = session['email']
    user_id = crud.get_user_id(email)
    time_punch_list = crud.get_time_punch_object_list(email)

    return redirect("/calendar")


@app.route('/edit_time_punch/<time_punch_id>')
def edit_time_punch_form(time_punch_id):
    """Takes user to page to correct/change/edit time punch."""

    email = session['email']
    time_punch_object = crud.get_time_punch_object(email, time_punch_id)

    return render_template("edit_time_punch.html", time_punch_object=time_punch_object)


@app.route('/admin_page')
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
