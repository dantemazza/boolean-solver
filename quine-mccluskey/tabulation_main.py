from functions import *

function = open("test_cases/test_case1.txt").readlines()

expressionTerms = []
size = int(function[0])
minTerms = []
dontCare = len(function) > 2
safety = 1 if dontCare else 0
minTrueMaxFalse = function[1][0] == "m"
#terms = function[1][2:(len(function[1])-2)].split(',')
terms = [int(n) for n in function[1][2:(len(function[1])-1-safety)].split(',')]
if dontCare:
    dcTerms = [int(n) for n in function[2][2:(len(function[2])-1)].split(',')]

# print(terms)
# print(dcTerms)

minTerms = []

if not minTrueMaxFalse:
    for i in range(2**size):
        if not ((i in terms) or (i in dcTerms)):
            minTerms.append(i)
else:
    minTerms = terms

# for i in range(len(minTerms)):
#     print(minTerms[i])
if dontCare:
    terms = minTerms + dcTerms
else:
    terms = minTerms

# mapping minterms and don't cares to respective boolean value to keep record of the term type
termTypes = {}
for i in range(len(minTerms)):
    termTypes[minTerms[i]] = True

if dontCare:
    for i in range(len(dcTerms)):
        termTypes[dcTerms[i]] = False

# associating the amount of set bits with a list index to facilitate implicant grouping
minBin = []
groups = [[] for i in range(size+1)]
for i in range(len(terms)):
      groups[getSetBits(terms[i])].append(str(bin(terms[i]))[2:].zfill(size))
      if termTypes[terms[i]]:
        minBin.append(str(bin(terms[i]))[2:].zfill(size))


# for i in range(len(groups)):
#     print(groups[i])
groups = [x for x in groups if x != []]


implicants = [[[]] for i in range(size)]

implicants[0] = groups

#storing all implicants in a 3D-list structure, with iterative regrouping of the previous set of implicants
for i in range(1, size-1):
    delList = []
    implicants[i], delList = regroup(implicants[i-1], size)
    for k in range(len(implicants[i-1])):
        implicants[i-1][k] = [p for p in implicants[i-1][k] if p not in delList]

for i in range(len(implicants)):
    implicants[i] = [x for x in implicants[i] if x != []]

implicants = [x for x in implicants if x != []]
primeImplicants = []

for i in range(len(implicants)):
    for j in range(len(implicants[i])):
        primeImplicants += implicants[i][j]

print(primeImplicants)
print(minBin)

piChart = [[0 for i in range(len(minBin))] for j in range(len(primeImplicants))]

#assembing the prime implicant chart
for i in range(len(primeImplicants)):
    for j in range(len(minBin)):
        match = True
        for k in range(size):
            if primeImplicants[i][k] != '-' and minBin[j][k] != primeImplicants[i][k]:
                match = False
                break
        piChart[i][j] = 1 if match else 0
printPIchart(size, minTerms, primeImplicants, piChart)

EPIs = []

#locating essential prime implicants
for i in range(len(minBin)):
    sum = 0
    currImplicant = ""
    index = 0
    for j in range(len(primeImplicants)):
        if piChart[j][i] == 1:
            sum += 1
            currImplicant = primeImplicants[j]
            index = j
        if sum > 1:
            currImplicant = ""
            break;
    if currImplicant:
        EPIs.append(currImplicant)

print(primeImplicants)
print(EPIs)

expressionTerms.extend(EPIs)
#removing the essential prime implicants and corresponding columns from the PIchart in preperation for Petrick's Method
for i in range(len(primeImplicants)-1,-1,-1):
    if not primeImplicants[i] in EPIs:
        continue
    for j in range(len(minTerms)-1, -1, -1):
        if piChart[i][j] == 1:
            minTerms.pop(j)
            for k in piChart:
                del k[j]

    piChart.pop(i)

primeImplicants = [x for x in primeImplicants if x not in EPIs]

printPIchart(size, minTerms, primeImplicants, piChart)