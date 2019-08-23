function = open("test_case1.txt").readlines()

size = int(function[0])
minTerms = []
dontCare = len(function) > 2
minTrueMaxFalse = function[1][0] == "m"
#terms = function[1][2:(len(function[1])-2)].split(',')
terms = [int(n) for n in function[1][2:(len(function[1])-2)].split(',')]
if dontCare:
    dcTerms = [int(n) for n in function[2][2:(len(function[2])-1)].split(',')]

print(terms)
print(dcTerms)

minTerms = []

if not minTrueMaxFalse:
    for i in range(2**size):
        if not ((i in terms) or (i in dcTerms)):
            minTerms.append(i)
else:
    minTerms = terms

print(minTerms)