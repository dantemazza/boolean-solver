from wtforms import Form, StringField, IntegerField, ValidationError


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
        raise ValidationError('Please ensure your input consists of comma-seperated integers')


def check_null(s, form):
    value = form.data
    if not value:
        raise ValidationError('Integer value from 1-6 required')


class TermForm(Form):
    input_size = IntegerField("Number of Variables", [check_null])
    minmaxterms = StringField("Minterms", [check_empty, validate_inputs])
    dontcares = StringField("Don't-cares", [validate_inputs])

