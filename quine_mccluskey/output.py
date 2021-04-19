

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


class PrimeImplicantChart:
    def __init__(self, size, minTerms, primeImplicants, piChart):
        self.size = size
        self.minTerms = minTerms
        self.primeImplicants = primeImplicants
        self.piChart = piChart
        self.generate_html_table()

    def printPIchart(self):
        for i in range(self.size):
            print(' ', end='')
        print('[', end='')
        for i in self.minTerms:
            comma = "" if i == self.minTerms[-1] else ("," if i > 9 else ", ")
            print(f"{str(i)}{comma}", end='')
        print(']')

        for i, boo in enumerate(self.piChart):
            print(self.primeImplicants[i] + str(boo))

    def generate_html_table(self):
        html = """
                <table class="table">
                    <thead>
                        {}
                    </thead>    
                    <tbody>     
                        {}       
                    </tbody>   
                </table>        
                """
        head = "<tr>{}</tr>"
        headrow = "".join([f"<th>{mt}</th>" for mt in [""] + self.minTerms])
        head = head.format(headrow)
        body = []
        for row, pi in zip(self.piChart, self.primeImplicants):
            row_html = "<tr>{}</tr>"
            bodyrow = "".join([f"<td>{entry}</td>" for entry in [pi] + row])
            row_html = row_html.format(bodyrow)
            body.append(row_html)
        body = "".join(body)
        self.html = html.format(head, body)