from flask import Blueprint, render_template, redirect, url_for, request
import os

import json

bp = Blueprint('routes', __name__)


@bp.route('/')
def home():
    return render_template('index.html')
