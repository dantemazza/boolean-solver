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


