"""Server operations. CRUD == Create,Read,Update,Delete."""

from model import TimeEntry, User, db, connect_to_db


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


def create_time_entry(email, time_entry, comments):
    """Creates and returns a time entry."""

    user_id = get_user_id(email)
    time_entry = TimeEntry(
        user_id=user_id, time_entry=time_entry, comments=comments)

    db.session.add(time_entry)
    db.session.commit()

    return time_entry


def get_time_entry_id(email):
    """Gets time entry id by email."""

    user_id = get_user_id(email)
    time_entry_id = db.session.query(
        TimeEntry.id).filter_by(user_id=user_id).first()

    return time_entry_id[0]


def get_time_entry_object_list(email, time_entry_id):
    """Gets time entry list."""

    user_id = get_user_id(email)
    time_entries = TimeEntries.query.filter_by(user_id=user_id).all()

    return time_entries


def get_time_entry_object_list(email):
    """Gets time entry list."""

    user_id = get_user_id(email)
    time_entries = TimeEntry.query.filter_by(user_id=user_id).all()

    return time_entries


def get_time_entries_for_date_selected(email, date, month, year):
    """Get time entry object list for date selected)"""

    user_id = get_user_id(email)
    time_entry_list = db.session.query(
        TimeEntry.time_entry).filter_by(user_id=user_id).all()
    print(time_entry_list)
    time_entry_by_date = []
    # for time_entry in time_entry_object_list:
    #     print(time_entry)
    #     if time_entry['year'] == year:
    #         if time_entry['month'] == month:
    #             if time_entry['date'] == date:
    #                 time_entry_by_date.append(time_entry)

    return time_entry_by_date


def delete_time_entry(time_entry_id):
    """Deletes a time entry that user no longer wishes to have in time log."""

    deleted_time_entry = db.session.query(
        TimeEntry).filter_by(time_entry_id=time_entry_id).all()
    print(deleted_time_entry,
          "Delete time entry in delete_time_entries(time_entry_id) crud fcn")
    db.session.delete(deleted_time_entry)
    db.session.commit()

    return deleted_time_entry


def admin_check(email):
    """Checks database to see if user that is attempting to enter admin page is listed as admin."""

    admin_confirmation = db.session.query(
        User.admin).filter_by(email=email).first()

    return admin_confirmation


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
