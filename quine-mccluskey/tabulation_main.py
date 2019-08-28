from functions import *
import sys
function = open("test_cases/test_case2.txt").readlines()
size = int(function[0])

expressionTerms = execute(function, size)

printExpression(size, expressionTerms)