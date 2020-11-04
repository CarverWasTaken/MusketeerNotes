from flask import render_template
from flask import Flask
app = Flask(__name__)

@app.route("/main")
def hello():
  return render_template('MainPage.html')

if __name__ == "__main__":
  app.run()