# Importing important libraries for project
import random
import string
from  flask import redirect, Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os

################## Setting Up Database ###############
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')

db = SQLAlchemy(app)

############# Model Creation #######################
class URL (db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(5))

    def __int__(self, long, short):
        self.long = long
        self.short = short

@app.before_request
def create_tables():
    db.create_all()

def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while (True):
        choices = random.choices(letters, k=5)
        choices = ''.join(choices)
        url_ = URL.query.filter_by(short=choices).first()
        if not url_:
            return choices


@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        url_entered = request.form['name']
        found_url = URL.query.filter_by(long=url_entered).first()
        if found_url:
            return redirect(url_for('display_url', url=found_url.short))
        else:
            short_url = shorten_url()
            new_url = URL(long=url_entered, short=short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for('display_url', url=short_url))
    else:
        return render_template('home.html')

@app.route('/display/<url>')
def display_url(url):
    return render_template('short_url.html', shortened_url=url)

@app.route('/<short_url>')
def redirection(short_url):
    long_url = URL.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return "<h1> Url was not found </h1>"

if __name__ == '__main__':
    app.run(debug=True)
