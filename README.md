# BooleanPlus
A python implementation of the [Quine-McCluskey algorithm](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm) and 
[Petrick's method](https://en.wikipedia.org/wiki/Petrick%27s_method), extrapolated from the content of [ECE124](https://ece.uwaterloo.ca/~cgebotys/NEW/124-frameset.htm).

## Running
Here is a sample test case expressed as a minterm expansion:
```
8
m(0,1,2,5,6,13,14,15,137,124,198,199)
d(3,11)
```
Here is a maxterm expansion:
6
M(0,1,2,5,6,35,36,39,41,45,49,62,63)
d(3,11,50,51,54,55,56,57)

The case should be formatted as such:
* The first line is the number of boolean inputs. Rather than writing, for example, f(a,b,c,d), we would put a 4.
* The second line is the max/min expansion. It is important that you include brackets, no spaces, and seperate each value with a comma
* The third line is dontcares, formatted in the same way as the second line. This is optional. 

**Place your case in the test_cases directory and adjust the file name in tabulation_main.py accordingly. Run tabulation_main.py to execute the algorithm.**

## About 
The program uses a prime implicant chart (as specified in the tabulation method) to locate all essential prime implicants. The remaining ones
are covered using a Petrick's method expansion. Algebraic expressions are stored in list data structures as follows:
```
<class 'list'>: [[[0], [2]], [1, 3], [2, 5], [3, 6], [5, 6, 7]]
```
Inner-most lists are products. Lists of the innermost lists are sums. Lists of these lists are products and so on. The program represents our
variables as numbers here. Assuming we map each number to its alphabetical letter (i.e 0->a, 1->b and so on), the equivalent boolean 
expression would be:
(a + c)(bd + cf + dg + fgh)
