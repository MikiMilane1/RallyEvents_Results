from flask import Blueprint, render_template, request, redirect, url_for
from db import db
import os
from forms import NewDriverForm
from models import TeamModel
from sqlalchemy.exc import IntegrityError

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, "templates", "team")

blp = Blueprint("team", __name__, template_folder=TEMPLATE_PATH)


# ALL TEAMS ROUTE
@blp.route('/all_teams')
def all_teams():
    return render_template('all_teams.html')


@blp.route("/team/<int:team_id>")
def team(team_id):
    current_team = db.get_or_404(TeamModel, team_id)
    return render_template('team.html')
