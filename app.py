from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import random
import string
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Urls(db.Model):
	id_ = db.Column("id_", db.Integer, primary_key=True)
	long = db.Column("long", db.String())
	short = db.Column("short", db.String(10))

	def __init__(self, long, short):
		self.long = long
		self.short = short 	

# with app.app_context():	
# 	db.create_all()

@app.route('/', methods=['POST', 'GET'])
def home():
	if request.method == "POST":
		url_received = request.form["nm"]
		desired_short = request.form["short"]
	
		found_url = Urls.query.filter_by(short=desired_short).first()
  
		if(found_url):
			flash("This code is taken")
			return render_template('url_page.html')
		else:
			new_url = Urls(url_received, desired_short)
			db.session.add(new_url)
			db.session.commit()
			return redirect(url_for("display_short_url", url=desired_short))
	else:
		return render_template('url_page.html')

@app.route('/<short_url>')
def redirection(short_url):
	long_url = Urls.query.filter_by(short=short_url).first()
	if long_url:
		return redirect(long_url.long)
	else:
		return f'<h1>Url doesnt exist</h1>'

@app.route('/display/<url>')
def display_short_url(url):
    	return render_template('shorturl.html', short_url_display=url)

if __name__ == '__main__':
    	app.run(port=5000, debug=True)
