from flask import Flask
from flask import render_template
from flask import request


app: Flask = Flask(__name__)


@app.get("/")
def index_page():
    return render_template("index.html")


if "__main__" == __name__: 
    app.run(debug=True)
