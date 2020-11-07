from flask import render_template, redirect
from flask import Flask
from flask import request
from flask import url_for
app = Flask(__name__)

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

@app.route("/register")
def register():
  return render_template('register.html')

@app.route("/notes")
def notes():
      return render_template('MainPage.html')



if __name__ == "__main__":
  app.run()