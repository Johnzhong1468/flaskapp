

from flask import Flask, render_template, url_for, jsonify, session, request
import pandas as pd
import numpy as np

app = Flask(__name__)

### Parameters ###
TABLIST = ["tab1", "tab2", "interval_update"]

### APP Secret ###
app.secret_key = "custom_secret_key"


@app.route('/', methods=["GET", "POST"])
def homepage():
    return render_template("index.html", tablist=TABLIST)


@app.route('/tab1')
def tab1():
    return render_template("tab1.html", tablist=TABLIST)


@app.route('/tab2')
def tab2():
    return render_template("tab2.html", tablist=TABLIST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)