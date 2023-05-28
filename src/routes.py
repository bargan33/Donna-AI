from flask import Blueprint, render_template, redirect, url_for, request, jsonify
import os
from donna_session import DonnaSession
from donna_ranking import DonnaRanking
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
    company_requirements = request.form.get('compReqs')
    path_to_serde = 'serde/'

    session = DonnaSession.create_new_session(
        session_name, path_to_serde, sheets_link, company_requirements)

    # Redirect the user to the home page after creating the new session
    return redirect(url_for('routes.home'))


@bp.route('/delete_session/<session_name>')
def delete_session(session_name):
    path_to_session = 'serde/' + session_name

    if os.path.exists(path_to_session):
        DonnaSession.remove_session(path_to_session)

    # Redirect the user to the home page after deleting the session
    return redirect(url_for('routes.home'))


@bp.route('/inspect_session/<session_name>')
def inspect_session(session_name):
    path_to_session = 'serde/' + session_name
    path_to_ranking_file = path_to_session + '/donna_ranking.json'

    # Check if donna_ranking.json exists
    if os.path.exists(path_to_ranking_file):
        # Load data from donna_ranking.json
        with open(path_to_ranking_file, 'r') as file:
            data = json.load(file)
        dr = DonnaRanking.from_dict(data)
    else:
        # Instantiate DonnaSession and DonnaRanking, call init method
        ds = DonnaSession(path_to_session)
        dr = DonnaRanking()
        dr.init(ds)

    with open(path_to_session + '/donna_ranking.json') as json_file:
        data = json.load(json_file)
    candidates = data['candidates']

    return render_template('inspect_session.html', session_name=session_name, candidates=candidates)


@bp.route('/refresh_session', methods=['POST'])
def refresh_session():
    session_name = request.json['session_name']
    path_to_session = 'serde/' + session_name
    ds = DonnaSession(path_to_session)
    dr = DonnaRanking()
    dr.init(ds)
    return jsonify({'status': 'success'})


@bp.route('/evaluate_session', methods=['POST'])
def evaluate_session():
    session_name = request.json['session_name']
    path_to_session = 'serde/' + session_name
    ds = DonnaSession(path_to_session)
    dr = DonnaRanking()
    dr.init(ds)
    dr.evaluate()
    return redirect(url_for('routes.session_results', session_name=session_name))


@bp.route('/session_results/<session_name>', methods=['GET'])
def session_results(session_name):
    path_to_session = 'serde/' + session_name
    path_to_ranking_file = path_to_session + '/donna_ranking.json'

    # Check if donna_ranking.json exists
    if os.path.exists(path_to_ranking_file):
        with open(path_to_ranking_file, 'r') as file:
            data = json.load(file)
        candidates = data['candidates']
    else:
        candidates = []

    # Get the sorting parameter from the URL, default to 'total_rating' if it's not specified
    sort_by = request.args.get('sort_by', 'total_rating')

    # Sort the candidates by the specified parameter
    if sort_by == 'full_name':
        candidates.sort(key=lambda x: x.get('full_name', ''))
    elif sort_by == 'email':
        candidates.sort(key=lambda x: x.get('email', ''))
    elif sort_by == 'phone_number':
        candidates.sort(key=lambda x: x.get('phone_number', ''))
    elif sort_by == 'soft_skill_rating':
        candidates.sort(key=lambda x: x.get(
            'soft_skill_rating', 0), reverse=True)
    elif sort_by == 'code_check':
        candidates.sort(key=lambda x: x.get('code_check', ''))
    elif sort_by == 'code_rating':
        candidates.sort(key=lambda x: x.get('code_rating', 0), reverse=True)
    elif sort_by == 'utest_rating':
        candidates.sort(key=lambda x: x.get('utest_rating', ''))
    else:
        candidates.sort(key=lambda x: x.get('total_rating', 0), reverse=True)

    return render_template('session_results.html', session_name=session_name, candidates=candidates)
