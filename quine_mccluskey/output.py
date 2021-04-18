

#prints the resulting expression based on implicants
def generateExpression(size, implicants):
    if implicants == ['----']:
        return "TRUE"
    elif not implicants:
        return "FALSE"
    res = ""
    for i, implicant in enumerate(implicants):
        char = 'a'
        for j in range(size):
            if implicant[j] == '-':
                char = chr(ord(char) + 1)
                continue
            res += char
            if not int(implicant[j]):
                res += "'"
            char = chr(ord(char) + 1)
        if implicant != implicants[-1]:
            res += " + "
    return res