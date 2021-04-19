from flask import Flask, render_template, request
import os
from quine_mccluskey.__main__ import execute
from quine_mccluskey.output import generateExpression
from server.data import history
from server.form import TermForm, parse_data, validate_range
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
    expression = ""
    PIchart = ""
    reduced_PIchart = ""

    if form.validate():
        print(form.data)
        size = form.data["input_size"]
        minterms = f"m({','.join(parse_data(form.data['minmaxterms']))})"
        function = [size, minterms]
        dc = parse_data(form.data['dontcares'])
        # function = ["4", "m(0,1,2,5,6,13,14,15)", "d(3,11)"]
        # print(function)
        if not validate_range(function):
            expression = "Inputs out of range"
        else:
            expressionTerms = execute(function)
            expression = generateExpression(size, expressionTerms)
    return render_template('index.html', form=form, expression=expression)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/history')
def history():
    return render_template('history.html', history=_history)

