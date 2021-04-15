

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
    print()