from flask import Flask, render_template, request
from boolean_solver.data import get_history_data, solution_html
from boolean_solver.form import TermForm, calculate_from_form
#import multiprocessing
import time
app = Flask(__name__)
# app.debug = True


@app.route('/', methods=['GET', 'POST'])
def home():
    timeout = 5
    form = TermForm(request.form)
    _PC = ""
    _RPC = ""
    expression = f"Time Limit ({timeout}s) Exceeded. Function too complex"
    start = time.time()
#   manager = multiprocessing.Manager()
#   return_list = manager.list()
#   p = multiprocessing.Process(target=calculate_from_form, args=(form, return_list))
#   p.start()
#   p.join(timeout)
#   if p.is_alive():
#       p.kill()
#   else:
    return_list = []
    calculate_from_form(form, return_list)
    _PC, _RPC, expression = return_list
    print(f"time: {time.time()-start}")
    soln = solution_html.format(_PC, _RPC, expression) if _PC else expression
    return render_template('index.html', form=form, expression=expression, solution=soln)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/history')
def history():
    display_history = get_history_data()
    return render_template('history.html', history=display_history)

if __name__ == '__main__':
    app.run()
