from flask import Blueprint, render_template, redirect, url_for, request
import os

import json

bp = Blueprint('routes', __name__)


@bp.route('/')
def home():
    return render_template('index.html')


@bp.route('/new_session')
def new_session():
    return render_template('new_session.html')
