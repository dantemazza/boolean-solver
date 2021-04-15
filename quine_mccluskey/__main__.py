from quine_mccluskey.logic import *

def execute(function, size):
    if len(function[1]) == 3:
        return []
    minTerms = []
    dontCare = len(function) > 2

    minTrueMaxFalse = function[1][0] == "m"

    terms = [int(n) for n in function[1][2:(len(function[1]) - 1 - dontCare)].split(',')]
    if dontCare:
        dcTerms = [int(n) for n in function[2][2:(len(function[2]) - 1)].split(',')]


    expressionTerms = []
    minTerms = []

    if not minTrueMaxFalse:
        for i in range(2 ** size):
            if not ((i in terms) or (i in dcTerms)):
                minTerms.append(i)
    else:
        minTerms = terms

    terms = minTerms + dcTerms if dontCare else minTerms

    if len(terms) == 2**size:
        return ['----']
    # mapping minterms and don't cares to respective boolean value to keep record of the term type
    termTypes = {}
    for i in minTerms:
        termTypes[i] = True

    if dontCare:
        for i in dcTerms:
            termTypes[i] = False

    # associating the amount of set bits with a list index to facilitate implicant grouping
    minBin = []
    groups = [[] for i in range(size + 1)]
    for term in terms:
        groups[getSetBits(term)].append(str(bin(term))[2:].zfill(size))
        if termTypes[term]:
            minBin.append(str(bin(term))[2:].zfill(size))

    groups = [x for x in groups if x]

    implicants = [[[]] for i in range(size)]

    implicants[0] = groups

    # storing all implicants in a 3D-list structure, with iterative regrouping of the previous set of implicants
    for i in range(1, size):
        delList = []
        implicants[i], delList = regroup(implicants[i - 1], size)
        for k in range(len(implicants[i - 1])):
            implicants[i - 1][k] = [p for p in implicants[i - 1][k] if p not in delList]

    for i in range(len(implicants)):
        implicants[i] = [x for x in implicants[i] if x != []]

    implicants = [x for x in implicants if x != []]
    primeImplicants = []

    for i in implicants:
        for j in i:
            primeImplicants += j


    piChart = [[0 for i in range(len(minBin))] for j in range(len(primeImplicants))]

    # assembing the prime implicant chart
    for i, PI in enumerate(primeImplicants):
        for j, BIN in enumerate(minBin):
            match = True
            for PI2, BIN2 in zip(PI, BIN):
                if PI2 != '-' and BIN2 != PI2:
                    match = False
                    break
            piChart[i][j] = int(match)

    print("Prime implicant chart:")
    printPIchart(size, minTerms, primeImplicants, piChart)

    EPIs = []

    # locating essential prime implicants
    for i in range(len(minBin)):
        sum = 0
        currImplicant = ""
        index = 0
        for j, PI in enumerate(primeImplicants):
            if piChart[j][i]:
                sum += 1
                currImplicant = PI
            if sum > 1:
                currImplicant = ""
                break;
        if currImplicant:
            EPIs.append(currImplicant)

    EPIs = set(list(EPIs))

    expressionTerms.extend(EPIs)
    # removing the essential prime implicants and corresponding columns from the PIchart in preperation for Petrick's Method
    for i in range(len(primeImplicants) - 1, -1, -1):
        if not primeImplicants[i] in EPIs:
            continue
        for j in range(len(minTerms) - 1, -1, -1):
            if piChart[i][j]:
                minTerms.pop(j)
                for k in piChart:
                    del k[j]

        piChart.pop(i)

    primeImplicants = [x for x in primeImplicants if x not in EPIs]

    print("Reduced prime implicant chart:")
    printPIchart(size, minTerms, primeImplicants, piChart)

    # to determine the expression with the least terms, we will map each implicant to its number of variables
    # and determine the least cost circuit once the function is condensed with Petrick's method

    PIterms = {}

    for i, PI in enumerate(primeImplicants):
        PIterms[i] = size - PI.count('-')

    # we begin Petrick's method by assembling a product of sums for uncovered minterms
    # using all non-essential prime implicants
    POS = []

    # the product of sums is assembled in a series of lists, with the first product having the terms in lists
    # themselves to be appended to using the foil method
    for i in range(len(minTerms)):
        currSum = []
        for j in range(len(primeImplicants)):
            if piChart[j][i] == 1:
                if i == 0:
                    term = []
                    term.append(j)
                    currSum.append(term)
                else:
                    currSum.append(j)
        POS.append(currSum)

    # print(POS)

    condensedPOS = simplify(distributePOS(POS)) if len(POS) > 1 else POS
    # print(condensedPOS)

    # determining least cost circuit using implicant mappings and a condensed product of sums
    leastCost = getLeastCost(condensedPOS, PIterms)
    expressionTerms.extend([primeImplicants[x] for x in leastCost])
    print(expressionTerms)

    return expressionTerms
