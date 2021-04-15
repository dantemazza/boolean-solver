from invoke import task
from quine_mccluskey.__main__ import execute
from quine_mccluskey.output import printExpression
import time

@task
def solve(c, test_case_path):
    with open(test_case_path, "r") as f:
        function = open(test_case_path).readlines()
        size = int(function[0])

    start = time.time()
    expressionTerms = execute(function, size)
    printExpression(size, expressionTerms)
    print(f"calculation took {time.time()-start} seconds")