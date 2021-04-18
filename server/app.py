from flask import Flask, render_template
from wtforms import Form, StringField, TextAreaField, validators
from quine_mccluskey.__main__ import execute
from quine_mccluskey.output import generateExpression
import os
from server.data import history
app = Flask(__name__)
app.debug = True

_history = history()

@app.route('/', methods=['GET', 'POST'])
def home():
    function = ["4", "m(0,1,2,5,6,13,14,15)", "d(3,11)"]
    size = int(function[0])
    expressionTerms = execute(function, size)
    res = generateExpression(size, expressionTerms)

    html = f"<p>{res}</p>"
    return render_template('index.html', _list=html)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/history')
def history():
    return render_template('history.html', history=_history)

