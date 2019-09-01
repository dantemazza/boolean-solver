from functions import *

function = open("test_cases/test_case1.txt").readlines()
size = int(function[0])

expressionTerms = execute(function, size)

printExpression(size, expressionTerms)