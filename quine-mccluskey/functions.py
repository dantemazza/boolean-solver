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
    #print(groups)
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
    regroups = [x for x in regroups if x != []]

    return regroups, list(set(delList))

#only formats prime implicant chart correctly for functions of <7 variables
def printPIchart(size, minTerms, primeImplicants, piChart):
    for i in range(size):
        print(' ', end='')
    print('[', end='')
    for i in minTerms:
        if i > 9:
            print(str(i) + ",", end='')
        else:
            print(str(i) + ', ', end='')
    print(']')

    for i in range(len(piChart)):
        print(primeImplicants[i] + str(piChart[i]))

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
            if SOPsets[i] is not None and SOPsets[j] is not None:
                if SOPsets[i].issuperset(SOPsets[j]):
                    SOPsets[i] = None
                elif SOPsets[i].issubset(SOPsets[j]):
                    SOPsets[j] = None
    res = [list(x) for x in SOPsets if x is not None]
    return res

def getLeastCost(POS, PIterms):
    leastCost = []
    lowest = sys.maxsize
    for i in range(len(POS)):
        currLength = 0
        for j in range(len(POS[i])):
            currLength += PIterms[POS[i][j]]
        leastCost = POS[i] if currLength < lowest else leastCost
    return leastCost

#prints the resulting expression based on implicants
def printExpression(size, implicants):
    for i in range(len(implicants)):
        char = 'a'
        for j in range(size):
            if implicants[i][j] == '-':
                char = chr(ord(char) + 1)
                continue
            print(char, end = '')
            if implicants[i][j] == '0':
                print("'", end = '')
            char = chr(ord(char) + 1)
        if i != len(implicants) - 1:
            print(" + ", end = '')



