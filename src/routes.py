from flask import Blueprint, render_template, redirect, url_for, request
import os
from donna_session import DonnaSession
import json

bp = Blueprint('routes', __name__)


@bp.route('/')
def home():
    serde_dir = 'serde/'  # path to serde directory
    try:
        # get all dirs inside serde
        session_names = next(os.walk(serde_dir))[1]
    except StopIteration:
        session_names = []

    session_names.reverse()  # reverse the order of the list
    return render_template('index.html', sessions=session_names)


@bp.route('/new_session')
def new_session():
    return render_template('new_session.html')


@bp.route('/create_new_session', methods=['POST'])
def create_new_session():
    session_name = request.form.get('sessionName')
    sheets_link = request.form.get('sheetsLink')
    path_to_serde = 'serde/'

    session = DonnaSession.create_new_session(
        session_name, path_to_serde, sheets_link)

    # Redirect the user to the home page after creating the new session
    return redirect(url_for('routes.home'))


@bp.route('/delete_session/<session_name>')
def delete_session(session_name):
    path_to_session = 'serde/' + session_name

    if os.path.exists(path_to_session):
        DonnaSession.remove_session(path_to_session)

    # Redirect the user to the home page after deleting the session
    return redirect(url_for('routes.home'))
