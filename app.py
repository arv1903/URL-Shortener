from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

#########################################################
#-=-=-=--=-=-=-=-=-= INITIALIZATION -=-=--=-=-=-=-=-=-=-#
#########################################################

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    	return Users.query.get(int(user_id))

#########################################################
#-=-=-=--=-=-=-=-=-=-= DB CREATION =-=-=--=-=-=-=-=-=-=-#
#########################################################

class Users(db.Model, UserMixin):
	id              = db.Column("id", db.Integer, primary_key=True)
	username        = db.Column(db.String(128), nullable = False)
	password        = db.Column(db.String(128), nullable = False)
 
class Urls(db.Model):
	id 		= db.Column("id", db.Integer, primary_key=True)
	id_user 	= db.Column("id_user", db.Integer, nullable=False)
	long            = db.Column("long", db.String())
	short           = db.Column("short", db.String(10))
 
	def __init__(self, id_user, long, short):
		self.id_user = id_user
		self.long = long
		self.short = short
  

 
with app.app_context():	
	db.create_all()

#########################################################
#-=-=-=--=-=-=-=-=-=-=-=- FORMS -=-=-=-=--=-=-=-=-=-=-=-#
#########################################################

def exists_username(form, username):    
	user = Users.query.filter_by(username = username.data).first()
	if user:
		raise ValidationError("Username already exists. Please use a different username")

class LoginForm(FlaskForm):
	username             = StringField("Username", validators=[DataRequired()])
	password             = PasswordField("Password", validators=[DataRequired()])
	submit               = SubmitField("Login")

class SignUpForm(FlaskForm):
	username             = StringField("Username", validators=[DataRequired(), Length(min=4, max=12), exists_username])
	password             = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
	confirm_password     = PasswordField("Confirm password", validators=[DataRequired(), Length(min=8), EqualTo("password")])
	submit               = SubmitField("Sign Up")

#########################################################
#-=-=-=--=-=-=-=-=-=-=-=- ROUTES =-=-=-=--=-=-=-=-=-=-=-#
#########################################################

@app.route('/user/<string:username>', methods=['POST', 'GET'])
@login_required
def home(username):
	if request.method == "POST":
		url_received = request.form["nm"]
		desired_short = request.form["short"]
	
		found_url = Urls.query.filter_by(short=desired_short).first()
  
		if(found_url):
			flash("This code is taken", "error")
			return render_template('url_page.html')
		else:
			new_url = Urls(current_user.get_id(), url_received, desired_short)
			db.session.add(new_url)
			db.session.commit()
			return redirect(url_for("display_short_url", url=desired_short))
	else:
		return render_template('url_page.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home', username = current_user.username))

	form = LoginForm()

	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = Users.query.filter_by(username=username).first()
		
		if user and password == user.password:
			login_user(user)
			return redirect(url_for('home', username = current_user.username))
		else:
			flash('Invalid username or password', 'error')
	return render_template('login.html', title="Login", form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        user = Users(
            username = form.username.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f'You have successfully created account "{user.username}"')

        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/<short_url>')
def redirection(short_url):
	long_url = Urls.query.filter_by(short=short_url).first()
	if long_url:
		return redirect(long_url.long)
	else:
		return f'<h1>Url doesnt exist</h1>'

@app.route('/display/<url>')
@login_required
def display_short_url(url):
	original_url = Urls.query.filter_by(short = url).first()
	return render_template('shorturl.html', short_url_display=url, original = original_url.long)

@app.route('/display_all', methods=['GET', 'POST'])
@login_required
def display_all():
	urls = Urls.query.filter_by(id_user = current_user.get_id()).all()
	# for url in urls:
	# 	print(url.short, url.long)
	return render_template("display_all.html", urls = urls)

if __name__ == '__main__':
    	app.run(port=5000, debug=True)
