"""Server operations. CRUD == Create,Read,Update,Delete."""

from model import TimePunches, User, db, connect_to_db


def create_user(email, password, fname, lname, photo):
    """Creates and returns a new user."""

    user = User(email=email, password=password,
                fname=fname, lname=lname, photo=photo)

    db.session.add(user)
    db.session.commit()

    return user


def get_user_id(email):
    """Returns the user object by ID."""

    user_id = db.session.query(User.id).filter_by(email=email).first()

    return user_id[0]


def get_users_fname(email):
    """Gets user's fname for return users."""

    fname = db.session.query(User.fname).filter_by(email=email).first()

    return fname[0]


def get_user_name(email):
    """Gets users's name."""

    fname = db.session.query(User.fname).filter_by(email=email).first()
    fname = fname[0]
    lname = db.session.query(User.lname).filter_by(email=email).first()
    lname = lname[0]
    user_name = f'{fname} {lname}'

    return user_name


def check_if_valid_user(email):
    """Return user email from registration."""

    user_exists_check = db.session.query(User).filter_by(email=email).first()

    return not not user_exists_check


def password_check(email, password):
    """Verifies that login information matches database of registered users."""

    valid_password = db.session.query(
        User).filter_by(password=password).first()

    return not not valid_password


def create_time_punch(email, comments):
    """Creates and returns a time punch."""

    user_id = db.session.query(User.id).filter_by(email=email).first()
    time_punch = TimePunches(user_id=user_id, comments=comments)

    db.session.add(time_punch)
    db.session.commit()

    new_time_punch = db.session.query(TimePunches.created_date).last()
    return new_time_punch


def get_time_punch_id(email):
    """Gets time punch id by email."""

    user_id = get_user_id(email)
    time_punch_id = db.session.query(
        TimePunches.id).filter_by(user_id=user_id).first()

    return time_punch_id[0]


def get_time_punch_object(email, time_punch_id):
    """Gets time punch list."""

    user_id = get_user_id(email)
    time_punches = TimePunches.query.filter_by(user_id=user_id).all()

    return time_punches


def get_time_punch_object_list(email):
    """Gets time punch list."""

    user_id = get_user_id(email)
    time_punches = TimePunches.query.filter_by(user_id=user_id).all()

    return time_punches


def delete_time_punch(time_punch_id):
    """Deletes a time punch that user no longer wishes to have in time log."""

    deleted_time_punch = db.session.query(
        TimePunches).filter_by(time_punch_id=time_punch_id).all()
    print(deleted_time_punch,
          "Delete time punch in delete_time_punches(time_punch_id) crud fcn")
    db.session.delete(deleted_time_punch)
    db.session.commit()

    return deleted_time_punch


def admin_check(email):
    """Checks database to see if user that is attempting to enter admin page is listed as admin."""


    admin_confirmation = db.session.query(User.admin).filter_by(email=email).first()

    return admin_confirmation


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
