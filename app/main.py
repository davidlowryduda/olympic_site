from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from markupsafe import escape
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = "A key"


@app.route("/", methods=['POST', 'GET'])
def main():
    sport_form = SportForm()
    if sport_form.validate_on_submit():
        sport = sport_form.sport.data.lower()
        flash(f"Received data: {sport}")
        if is_olympic_sport(sport):
            flash(f"{sport} is an olympic sport")
        else:
            flash(f"{sport} is not an olympic sport")
    else:
        flash("Invalid data entry")
    return render_template('index.html', form=sport_form)


@app.route("/<sport>")
def repeat(sport):
    return f"<p>Hi. You typed {escape(sport)}!"


@app.route("/about")
def about():
    pass


class SportForm(FlaskForm):
    sport = StringField("Sport", validators=[DataRequired()])
    submit = SubmitField("Is that a sport?")


def make_decider():
    with open("olympic_sports.txt", "r") as infile:
        print("Opening file")
        sportlist = infile.readlines()
        sportlist = [sport.strip() for sport in sportlist]

        def decider(sport):
            return sport in sportlist

    return decider


is_olympic_sport = make_decider()
