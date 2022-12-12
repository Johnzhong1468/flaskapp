from flask import Flask, render_template, url_for, jsonify, session, request
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def homepage():
    return render_template(
        "index.html",
        app_list=[
        ]
    )


@app.route('/tab1')
def tab1():
    return render_template("tab1.html", tablist=TABLIST)