from wtforms import Form, StringField, IntegerField, ValidationError
from datetime import datetime
import uuid
from quine_mccluskey.execute import execute
from quine_mccluskey.output import generateExpression, PrimeImplicantChart, gen_f
from server.data import history_data

def parse_data(data):
    values = [x.replace(" ", "") for x in data.split(",") if x]
    return values


def validate_inputs(s, form):
    values = parse_data(form.data)
    print(values)
    for value in values:
        if not value.isdecimal():
            raise ValidationError('Please ensure your input consists of comma-seperated integers')
    if len(values) != len(set(values)):
        raise ValidationError('Please ensure your inputs are unique')

def check_empty(s, form):
    values = parse_data(form.data)
    if not values:
        raise ValidationError('Please ensure your input consists of comma-seperated positive integers')


def check_null(s, form):
    value = form.data
    if not value:
        raise ValidationError('Integer value from 1-6 required')


def validate_range(function):
    size = int(function[0])
    dontCare = len(function) > 2
    terms = [int(n) for n in function[1][2:(len(function[1]) - 1)].split(',')]
    dcTerms = [int(n) for n in function[2][2:(len(function[2]) - 1)].split(',')] if dontCare else []
    for term in terms + dcTerms:
        if term >= 2**size:
            return False
    return True



def validate_unique(function):
    dontCare = len(function) > 2
    terms = [int(n) for n in function[1][2:(len(function[1]) - 1)].split(',')]
    dcTerms = [int(n) for n in function[2][2:(len(function[2]) - 1)].split(',')] if dontCare else []
    if len(set(terms+dcTerms)) != len(terms) + len(dcTerms):
        return False
    return True

class TermForm(Form):
    input_size = IntegerField("Number of Variables", [check_null])
    minmaxterms = StringField("Minterms", [check_empty, validate_inputs])
    dontcares = StringField("Don't-cares", [validate_inputs])


def calculate_from_form(form, return_list):
    expression = ""
    _PC = ""
    _RPC = ""
    if form.validate():
        size = form.data["input_size"]
        minterms = f"m({','.join(parse_data(form.data['minmaxterms']))})"
        function = [size, minterms]
        s_function = f"{gen_f(size)} = {minterms}"
        dc = parse_data(form.data['dontcares'])
        if dc:
            dc = f"d({','.join(dc)})"
            function.append(dc)
            s_function += f", {dc}"
        if not validate_range(function):
            expression = "Inputs out of range"
        elif not validate_unique(function):
            expression = "Don't-cares and minterms cannot have overlap"
        else:
            expressionTerms, PC, RPC = execute(function)
            expression = generateExpression(size, expressionTerms)
            _PC = PC.html
            _RPC = RPC.html
        history_obj = {
            'id': uuid.uuid4(),
            'function': s_function,
            'solution': expression,
            "pi_chart": _PC,
            "reduced_pi_chart": _RPC,
            'time_created': datetime.strftime(datetime.now(), "%Y-%m-%d:%H:%M:%S")

        }
        history_data.append(history_obj)
    return_list.extend([_PC, _RPC, expression])