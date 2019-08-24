from functions import *

function = open("test_case1 .txt").readlines()

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
groups = [[] for i in range(size+1)]
for i in range(len(terms)):
      groups[getSetBits(terms[i])].append(str(bin(terms[i]))[2:].zfill(size))

# for i in range(len(groups)):
#     print(groups[i])
groups = [x for x in groups if x != []]


implicants = [[[]] for i in range(size)]

implicants[0] = groups

#storing all implicants in a 3D-list structure, with iterative regrouping of the previous set of implicants
for i in range(1, size-1):
      implicants[i] = regroup(implicants[i-1], size)

implicants = [x for x in implicants if x != [[]] and x != []]

for i in range(len(implicants)):
    print(implicants[i])

