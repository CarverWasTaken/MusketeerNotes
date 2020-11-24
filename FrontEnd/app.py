from flask import render_template, redirect
from flask import Flask
from flask import request
from flask import url_for
app = Flask(__name__)
yourNotes = {
        0: {'title': 'First Note', 'text': 'This is my first note'},
        1: {'title': 'Second Note', 'text': 'This is my second note'},
        2: {'title': 'Third Note', 'text': 'This is my third note'}
    }

def getNotes():
   
   return notes

@app.route("/")
def main():
  return redirect('/login')

@app.route("/login",  methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
      username = request.form['Username']
      password = request.form['Password']

      #fake login functionality
      if password != '' and  username != '':
        return redirect('/notes')
      else:
        return redirect('/login')
  else:
      return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
      username = request.form['Username']
      password = request.form['Password']
      confirmPassword = request.form['Confirm']

      #fake login functionality
      if password == confirmPassword:
        return redirect('/notes')
      else:
        return redirect('/register')
  else:
      return render_template('register.html')

@app.route("/notes")
def notes():
      # _notes = getNotes()
      return render_template('MainPage.html', notes = yourNotes)

@app.route("/addNote", methods=['POST'])
def addNote():
      if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        yourNotes[len(yourNotes)+1] = {'title': title, 'text': text}
        return redirect('/notes')



if __name__ == "__main__":
  app.run()