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