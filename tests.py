from treesearch import *
def test_ucs_1():
    g = ListCostTree('G')
    d = ListCostTree('D', [g], [3])
    c = ListCostTree('C', [d,g], [1,2])
    b = ListCostTree('B', [d], [3])
    a = ListCostTree('A', [b,c], [3,1])
    s = ListCostTree('S', [a,g], [1,12])
    print(ucs(s, lambda l: l=='G'))
    print("expect GCAS")

def test_ucs_2(x, y):
    m = [[23, 580, 36, 35, 27, 27, 43, 49, 25, 25],
         [42, 49, 360, 40, 58, 46, 58, 49, 36, 29],
         [52, 420, 52, 24, 32, 58, 50, 25, 34, 44],
         [46, 330, 26, 37, 33, 33, 40, 30, 28, 24],
         [25, 300, 21, 38, 52, 55, 42, 26, 39, 35],
         [34, 34, 47, 55, 58, 47, 54, 40, 34, 20],
         [28, 45, 26, 57, 31, 29, 57, 49, 46, 32],
         [47, 38, 23, 20, 30, 25, 22, 34, 36, 24],
         [33, 37, 47, 31, 24, 41, 40, 29, 42, 29],
         [30, 50, 32, 46, 30, 39, 41, 37, 31, 25]]
    mt = []
    for i in range(len(m)):
        mt.append([ListCostTree((j,i)) for j in range(len(m[i]))])
    for i in range(len(mt)):
        for j in range(len(mt[i])):
            if i>0:
                mt[i][j].add_bc(mt[i-1][j], m[i-1][j])
            if j>0:
                mt[i][j].add_bc(mt[i][j-1], m[i][j-1])
            if i<len(mt)-1:
                mt[i][j].add_bc(mt[i+1][j], m[i+1][j])
            if j<len(mt[i])-1:
                mt[i][j].add_bc(mt[i][j+1], m[i][j+1])
    tree = mt[0][0]
    sol = ucs(tree, lambda p: p==(x, y))#[0][::-1]
    print(sol)
    for p in sol[0]:
        m[p[1]][p[0]]='■■'
    for r in m:
        print(*r)
