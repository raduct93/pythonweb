from flask import Flask
from flask import render_template, request, redirect, url_for, session, g
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/data.db'
app.config['SECRET_KEY'] = 'something_secret'

db = SQLAlchemy(app)

@app.before_request
def setup():
    g.username = session.get('username', None)

@app.route('/')
def homepage():
    if not session.get('username', None):
        return  redirect(url_for('loginview'))
    return render_template('home.html', aplicatie = 'osss', tasks = Task.query.all())

@app.route('/login', methods = ("GET", "POST"))
def loginview():
    if request.method == "POST":
        session['username'] = request.form['username']
        return redirect(url_for('homepage'))
    return render_template('login.html')

@app.route('/logout')
def logoutview():
    session['username'] = None
    return redirect(url_for('loginview'))

@app.route('/add-new', methods = ("GET", "POST"))
def add():
    if request.method == "POST":
        new_task = Task(text = request.form['taskname'])
        db.session.add(new_task)
        db.session.commit()
    return render_template('add.html')

@app.route('/setdone/<id>')
def setdone(id):
    task = Task.query.filter_by(id=id).first()
    task.done = True
    db.session.commit()
    return redirect(url_for('homepage'))

@app.route('/delete/<id>')
def delete(id):
    task = Task.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('homepage'))
@app.route('/deletedone')
def deletedone():
    count = 0
    for task in Task.query.all():
        if task.done:
            db.session.delete(task)
            count = count + 1
    db.session.commit()
    return redirect(url_for('homepage'))                    

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String)        
    done = db.Column(db.Boolean, default = False)

db.create_all()
app.run()
