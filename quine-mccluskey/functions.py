import sys

def getSetBits(x):
    bits = 0
    while x:
        bits += x & 1
        x >>= 1
    return bits

def regroup(groups, size):
    delList = []
    groupSize = len(groups)
    regroups = [[] for i in range(groupSize-1)]
    #all groups

    for i in range(groupSize - 1):
        #all strings in preceding group
        for j in range(len(groups[i])):
            #all strings in succeeding group
            for k in range(len(groups[i+1])):
                different = 0
                binString = ''
                #all bits
                for l in range(size):
                    binString += groups[i][j][l] if groups[i+1][k][l] == groups[i][j][l] else '-'
                    different += 0 if groups[i+1][k][l] == groups[i][j][l] else 1
                if different < 2:
                    regroups[i].append(binString)
                    delList += groups[i][j], groups[i+1][k]
            regroups[i] = list(dict.fromkeys(regroups[i]))
    regroups = [x for x in regroups if x]

    return regroups, list(set(delList))

#only formats prime implicant chart correctly for functions of <7 variables
def printPIchart(size, minTerms, primeImplicants, piChart):
    for i in range(size):
        print(' ', end='')
    print('[', end='')
    for i in minTerms:
        comma = "" if i == minTerms[-1] else ("," if i > 9 else ", ")
        print(f"{str(i)}{comma}", end='')
    print(']')

    for i, boo in enumerate(piChart):
        print(primeImplicants[i] + str(boo))

#iteratively using foil to distribute the product of sums into a sum of products
def distributePOS(POS):
    SOP = POS[0]
    for i in range(len(POS)-1):
        SOP = foil(SOP, POS[i+1])

    return [list(t) for t in set(tuple(x) for x in SOP)]

#foil method designed for brute force expansion of POS. t1 is a list of lists of the initial terms
#each list from t1 is appendeded every possible combination from t2 and returned
def foil(t1, t2):
    term = []
    a = 0
    for i in range(len(t1)):
        for j in range(len(t2)):
            # print(t1[i])
            term.append(t1[i].copy())
            if t2[j] not in term[a]:
                term[a].append(t2[j])
            a += 1
    return term

def simplify(SOP):
    SOPsets = [set(i) for i in SOP]
    result = []
    for i in range(len(SOPsets)):
        for j in range(i+1, len(SOPsets)):
            if SOPsets[i] and SOPsets[j]:
                if SOPsets[i].issuperset(SOPsets[j]):
                    SOPsets[i] = None
                elif SOPsets[i].issubset(SOPsets[j]):
                    SOPsets[j] = None
    res = [list(x) for x in SOPsets if x]
    return res

def getLeastCost(POS, PIterms):
    leastCost = []
    lowest = sys.maxsize
    for i in POS:
        currLength = 0
        for j in i:
            currLength += PIterms[j]
        leastCost = i if currLength < lowest else leastCost
    return leastCost

#prints the resulting expression based on implicants
def printExpression(size, implicants):
    if implicants == ['----']:
        print("TRUE")
        return
    elif not implicants:
        print("FALSE")
        return
    for i, implicant in enumerate(implicants):
        char = 'a'
        for j in range(size):
            if implicant[j] == '-':
                char = chr(ord(char) + 1)
                continue
            print(char, end='')
            if not int(implicant[j]):
                print("'", end='')
            char = chr(ord(char) + 1)
        if implicant != implicants[-1]:
            print(" + ", end='')

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

