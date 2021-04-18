from flask import Flask, render_template, request
import os
from quine_mccluskey.__main__ import execute
from quine_mccluskey.output import generateExpression
from server.data import history
from server.form import TermForm
app = Flask(__name__)
app.debug = True

_history = history()

@app.route('/', methods=['GET', 'POST'])
def home():
    # function = ["4", "m(0,1,2,5,6,13,14,15)", "d(3,11)"]
    # size = int(function[0])
    # expressionTerms = execute(function, size)
    # res = generateExpression(size, expressionTerms)
    form = TermForm(request.form)
    if form.validate():
        print("success!")
    return render_template('index.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/history')
def history():
    return render_template('history.html', history=_history)

