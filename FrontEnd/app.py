from flask import render_template, redirect
from flask import Flask
app = Flask(__name__)

@app.route("/")
def main():
  return redirect('/login')

@app.route("/login")
def login():
  return render_template('login.html')

@app.route("/register")
def register():
  return render_template('register.html')

@app.route("/notes")
def notes():
  return render_template('MainPage.html')



if __name__ == "__main__":
  app.run()