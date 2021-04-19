from invoke import task
from quine_mccluskey.execute import execute
from quine_mccluskey.output import generateExpression
import time

@task
def solve(c, test_case_path):
    _solve(test_case_path)


def _solve(test_case_path):
    with open(test_case_path, "r") as f:
        function = open(test_case_path).readlines()
        size = int(function[0])

    start = time.time()
    expressionTerms, PC, RPC = execute(function)
    exp = generateExpression(size, expressionTerms)
    print(exp)
    print(f"calculation took {time.time()-start} seconds")

_solve('test_cases/test_case4.bool')