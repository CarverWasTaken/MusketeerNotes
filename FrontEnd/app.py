from flask import render_template, redirect
from flask import Flask
from flask import request
from flask import url_for
from flask.globals import session
from database import db
from models import Note as Note
from models import User as User
from models import Comment as Comment
from forms import RegisterForm, LoginForm, CommentForm
import bcrypt
from flask import session
from sqlalchemy import and_, or_, not_

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
@app.route("/index")
def index():
    return redirect('/login')


# Login page route
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    # validate_on_submit only validates using POST
    if form.validate_on_submit():
        # form validation included a criteria to check the username does not exist
        # we can know we are safe to add the user to the database
        password_hash = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        new_record = User(first_name, last_name, request.form['email'], password_hash)
        db.session.add(new_record)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        # get the id of the newly created database record
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # save the user's id to the session
        session['user_id'] = the_user.id

        return redirect(url_for('notes'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
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
@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('login'))


# Access to list of notes
@app.route("/notes", methods=['POST', 'GET'])
def notes():
    if session.get('user'):
        if request.method == 'POST':
            pinned = db.session.query(Note).filter_by(user_id=session['user_id'], pinned = True).first()
            searchFor = request.form['search']
            search = db.session.query(Note).filter((or_(Note.title.contains(searchFor), Note.text.contains(searchFor)))).filter_by(user_id=session['user_id'], pinned = False)                                
            return render_template('MainPage.html', notes=search, user=session['user'], pinned = pinned)
        else:
            pinned = db.session.query(Note).filter_by(user_id=session['user_id'], pinned = True).first()
            my_note = db.session.query(Note).filter_by(user_id=session['user_id'], pinned = False).all()                        
            return render_template('MainPage.html', notes=my_note,user=session['user'], pinned = pinned)
    return redirect(url_for('login'))




@app.route('/note/<note_id>')
def viewNote(note_id):
    if session.get('user'):
        my_note = db.session.query(Note).filter_by(id=note_id, user_id=session['user_id']).one()
        
        form = CommentForm()
        return render_template("viewNote.html", note = my_note, user = session['user'], form = form)
    else:
        return redirect(url_for('login'))


# User capibility to add notes -- saves notes to database "db"
@app.route('/addNote', methods=['GET', 'POST'])
def addNote():

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        from datetime import date
        today = date.today()
        today = today.strftime('%m-%d-%Y')
        new_record = Note(title, text, today, False, session['user_id'])
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



@app.route('/notes/<note_id>/comment', methods=['POST'])
def new_comment(note_id):
    if session.get('user'):
        comment_form = CommentForm()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(note_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('viewNote', note_id=note_id))

    else:
        return redirect(url_for('login'))

# Delete Note -- updateing databse to reflect deletion
@app.route('/comment/delete/<comment_id>/<note_id>', methods=['POST'])
def delete_comment(comment_id, note_id):
    my_comment = db.session.query(Comment).filter_by(id=comment_id).one()
    db.session.delete(my_comment)
    db.session.commit()

    return redirect('/note/' + str(note_id))

# Edit note and updating notes -- saving it to database "db"
@app.route('/comment/edit/<comment_id>/<note_id>', methods=['POST'])
def update_comment(comment_id, note_id):
    if request.method == 'POST':
        text = request.form['text']
        comment = db.session.query(Comment).filter_by(id=comment_id).one()

        comment.content = text

        db.session.add(comment)
        db.session.commit()
    return redirect('/note/' + str(note_id))

# part related to pinning comments

@app.route('/note/pin/<note_id>', methods=['POST'])
def pin(note_id):
    if session.get('user'):
        # checking to see if there is a note pinned
        previousPinned = db.session.query(Note).filter_by(user_id=session['user_id'], pinned = True).first()
        if previousPinned:
            previousPinned.pinned = False
            db.session.add(previousPinned)
            db.session.commit()
        
        my_note = db.session.query(Note).filter_by(id=note_id).one()
        my_note.pinned = True
        db.session.add(my_note)
        db.session.commit()

        return redirect('/notes')
    else:
         return redirect('/login')

@app.route('/note/unpin', methods=['POST'])
def unpin():
    if session.get('user'):
        # checking to see if there is a note pinned
        previousPinned = db.session.query(Note).filter_by(user_id=session['user_id'], pinned = True).first()
        if previousPinned:
            previousPinned.pinned = False
            db.session.add(previousPinned)
            db.session.commit()
        return redirect('/notes')
    else:
         return redirect('/login')

    # start the application "app"
if __name__ == "__main__":
    app.run()
