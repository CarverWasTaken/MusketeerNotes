from flask import render_template, redirect
from flask import Flask
from flask import request
from flask import url_for
from flask.globals import session
from database import db
from models import Note as Note
from models import User as User
from forms import RegisterForm
from forms import LoginForm
import bcrypt
from flask import session

from models import Comment as Comments


# set vairable "app" to flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SE3155'
# Database configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialzie database "db"
db.init_app(app)
with app.app_context():
    db.create_all()


# Homepage route
@app.route("/")
def main():
    return redirect('/login')


# Login page route
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(name=request.form['name']).first()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('notes'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)

# Register page route -- also contains password authentication

@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('notes'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # validate_on_submit only validates using POST
    if form.validate_on_submit():
        # form validation included a criteria to check the username does not exist
        # we can know we are safe to add the user to the database
        name = request.form['name']
        password_hash = bcrypt.hashpw(
        request.form['password'].encode('utf-8'), bcrypt.gensalt())
        new_record = User(request.form['name'], password_hash)
        db.session.add(new_record)
        db.session.commit()
        # save the user's name to the session
        session['user'] = name
        # get the id of the newly created database record
        user = db.session.query(User).filter_by(name=request.form['name']).first()
        # save the user's id to the session
        session['user_id'] = user.id

        return redirect(url_for('notes'))
    return render_template('register.html', form=form)


# Access to list of notes
@app.route("/notes")
def notes():
    # _notes = getNotes()
    if session.get('user'):
        my_note = db.session.query(Note).filter_by(user_id=session['user_id']).all()
        return render_template('MainPage.html', notes=my_note,user=session['user'])
    return render_template('MainPage.html')

# Access to indiviual notes with a unique note id


@app.route('/note/<note_id>')
def viewNote(note_id):
    a_user = db.session.query(User).filter_by(name=User.name)
    my_note = db.session.query(Note).filter_by(id=note_id).one()
    return render_template('viewNote.html', note=my_note, user=a_user)


# User capibility to add notes -- saves notes to database "db"
@app.route('/addNote', methods=['GET', 'POST'])
def addNote():

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        from datetime import date
        today = date.today()
        today = today.strftime('%m-%d-%Y')
        new_record = Note(title, text, today,session['user_id'])
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('notes'))
    else:
        a_user = db.session.query(User).filter_by(name=User.name)
        return render_template('mainPage.html', user=a_user)


# Edit note and updating notes -- saving it to database "db"
@app.route('/note/edit/<note_id>', methods=['POST'])
def update_note(note_id):
    if request.method == 'POST':
        text = request.form['text']
        note = db.session.query(Note).filter_by(id=note_id).one()

        note.text = text

        db.session.add(note)
        db.session.commit()
    return redirect('/note/' + str(note.id))


# Delete Note -- updateing databse to reflect deletion
@app.route('/note/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    my_note = db.session.query(Note).filter_by(id=note_id).one()
    db.session.delete(my_note)
    db.session.commit()

    return redirect('/notes')


# Route to add a comment to an established note
@app.route('/note/<note_id>/comment', methods=['GET', 'POST'])
def new_comment(note_id):
    if request.method == 'POST':
        text = request.form['text']
        from datetime import date
        today = date.today()
        today = today.strftime('%m-%d-%Y')
        new_record = Comment(text, today, note_id)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('notes'))
    else:
        # Redirects back to view if page crashes
        return redirect(url_for('notes'))


# editing an exisiting comment
@app.route('/note/edit/<note_id>/comment', methods=['POST'])
def edit_comment(parent_id):
    if request.method == 'POST':
        # get the data from comment
        text = request.form['text']

        comment = db.session.query(Comment).filter_by(id=parent_id).one()

        # updtae the comment with new text
        comment.text = text
        # add the text to database
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('viewNote.html'))


# Delete exisiting note
@app.route('/note/delete/<note_id>/comment', methods=['POST'])
def delete_comment(note_id, parent_id):

    comment = db.session.query(Comment).filterby(id=parent_id).one()

    # delete the comment from database
    db.session.delete(comment)
    db.session.commit()

    redirect(url_for('viewNote.html'))


    # start the application "app"
if __name__ == "__main__":
    app.run()
