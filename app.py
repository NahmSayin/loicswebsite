from datetime import datetime
import os
from dotenv import load_dotenv   #for python-dotenv method
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy


load_dotenv() 

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('USER')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


#for securing cookies and session data + creating database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/nahomalem/Documents/Current projects/Loics website.blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #this supresses event system warning

db = SQLAlchemy(app)
class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20)) 
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

#Ensures that blogpost table database is created before any requests
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    date_posted = post.date_posted.strftime('%d, %B, %Y')
    return render_template('post.html', post=post)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=["POST"] )
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
    
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route("/email")
def email():
   msg = Message('Hello', sender = app.config.get('MAIL_USERNAME'), recipients = ['MAIL_USERNAME'])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)


