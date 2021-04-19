from flask import Flask, render_template, request
import os
from quine_mccluskey.execute import execute
from quine_mccluskey.output import generateExpression, PrimeImplicantChart
from server.data import history, solution_html
from server.form import TermForm, parse_data, validate_range
app = Flask(__name__)
app.debug = True

_history = history()

@app.route('/', methods=['GET', 'POST'])
def home():
    form = TermForm(request.form)
    expression = ""
    _PC = ""
    _RPC = ""
    if form.validate():
        print(form.data)
        size = form.data["input_size"]
        minterms = f"m({','.join(parse_data(form.data['minmaxterms']))})"
        function = [size, minterms]
        dc = parse_data(form.data['dontcares'])
        if dc:
            function.append(f"m({','.join(dc)})")
        if not validate_range(function):
            expression = "Inputs out of range"
        else:
            expressionTerms, PC, RPC = execute(function)
            expression = generateExpression(size, expressionTerms)
            _PC = PC.html
            _RPC = RPC.html
            # print(_PC)
            # print(_RPC)
    soln = solution_html.format(_PC, _RPC, expression) if expression else ""
    return render_template('index.html', form=form, expression=expression, solution=soln)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/history')
def history():
    return render_template('history.html', history=_history)

