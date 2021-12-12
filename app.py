from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

app = Blueprint('app', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/details')
@login_required
def weatherDetails():
    return render_template('weatherDetails.html', name=current_user.firstName)