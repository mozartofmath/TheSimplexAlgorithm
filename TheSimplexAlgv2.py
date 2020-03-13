def toSlackForm(A,b,c):
    n = len(A) + len(A[0]) + 1
    m = len(A)
    Obj = [0] + c + [0]*m
    N = [x for x in range(1,len(A[0])+1)]
    B = [len(A[0]) + x for x in range(1,len(A)+1)]
    newA = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        newA[i][0] = b[i]
    for i in range(len(A)):
        for j in range(len(A[0])):
            newA[i][j+1] = -A[i][j]
    for i in range(m):
        newA[i][len(A[0])+i+1] = 1
    return N,B,newA,Obj

def choose_leaving_var(N,Obj):
    for x in N:
        if Obj[x]>0:
            return x
    return -1
def choose_entering_var(B,A,Obj,l):
    Min = float('inf')
    e = B[0]
    for i in range(len(A)):
        if A[i][l] >= 0:
            continue
        if -A[i][0]/A[i][l] < Min:
            Min = -A[i][0]/A[i][l]
            e = B[i]
    if Min < float('inf'):
        return e
    return -1

def Pivot(N,B,A,Obj,e,l):
    for i in range(len(B)):
        if B[i] == e:
            break
    A[i][e] = -1
    for j in range(len(A[0])):
        if j!=l:
            A[i][j] = -A[i][j]/A[i][l]
    A[i][l] = 1
    vector = A[i].copy()
    vector[l] = 0
    for j in range(len(Obj)):
        if j!=l:
            Obj[j] = Obj[j] + Obj[l]*vector[j]
    Obj[l] = 0
    for k in range(len(A)):
        if k!=i:
            for j in range(len(vector)):
                A[k][j] = A[k][j] + A[k][l]*vector[j]
            A[k][l] = 0
    N.remove(l)
    N.append(e)
    B[i] = l
    return N,B,A,Obj

def newObj(B,A,Obj):
    for i in range(len(B)):
        if Obj[B[i]] != 0:
            for j in range(len(Obj)):
                if j!=B[i]:
                    Obj[j] = Obj[j] + Obj[B[i]]*A[i][j]
            Obj[B[i]] = 0
    return Obj
def Auxiliary(A,b,c):
    k = 0
    for i in range(len(b)):
        if b[i]<b[k]:
            k = i
    if b[k] >= 0:
        N,B,A,Obj = toSlackForm(A,b,c)
        return N,B,A,Obj,''
    Aaux, baux = A.copy(), b.copy()
    for i in range(len(Aaux)):
        Aaux[i].append(-1)
    caux = [0]*len(c) + [-1]
    N,B,A,Obj = toSlackForm(Aaux,baux,caux)
    e = B[k]
    x0 = len(c)+1
    
    N,B,A,Obj = Pivot(N,B,A,Obj,e,x0)
    while choose_leaving_var(N,Obj) != -1:
        l = choose_leaving_var(N,Obj)
        e = choose_entering_var(B,A,Obj,l)
        if e == -1:
            return N,B,A,Obj,'unbounded'
        N,B,A,Obj = Pivot(N,B,A,Obj,e,l)
    X = [0 for i in range(len(A[0])-1)]
    for i in range(len(B)):
        X[B[i]-1] = A[i][0]
    if X[-1] == 0:
        if x0 in B:
            for nb in N:
                if A[B.index(x0)][nb]!=0:
                    break
            N,B,A,Obj = Pivot(N,B,A,Obj,x0,nb)
        N.remove(x0)
        for i in range(len(A)):
            A[i] = A[i][:x0]+A[i][x0+1:]
        Obj = Obj[:x0]+Obj[x0+1:]
        for i in range(len(N)):
            if N[i]>len(c):
                N[i]-=1
        for i in range(len(B)):
            if B[i]>len(c):
                B[i]-=1
        Obj = newObj(B,A,[0] + c + [0]*len(A))
        return N,B,A,Obj,''
    
    return N,B,A,Obj,'infeasible'

def Simplex(A,b,c):
    N,B,A,Obj,v = Auxiliary(A,b,c)
    if v!='':
        return v
    while choose_leaving_var(N,Obj) != -1:
        l = choose_leaving_var(N,Obj)
        e = choose_entering_var(B,A,Obj,l)
        if e == -1:
            return 'unbounded'
        N,B,A,Obj = Pivot(N,B,A,Obj,e,l)
    X = [0 for i in range(len(A[0])-1)]
    for i in range(len(B)):
        X[B[i]-1] = A[i][0]
    return X,Obj[0]

A = [
        [ 0, -1, 1, 1, -1],
        [ 1,  0,-1, 1, -1],
        [-1,  1, 0, 1, -1],
        [ 1,  1, 1, 0,  0],
        [ -1, -1, -1,0, 0]
    ]
b = [0,0,0,1,-1]
c = [0,0,0,1,-1]

print(Simplex(A,b,c))

A = [
        [2,-1],
        [1,-5]
    ]
b = [2,-4]
c = [2,-1]

print(Simplex(A,b,c))

A = [
        [-1,1,1,1,-1],
        [-1,-1,1,1,-1],
        [-1,-1,-1,1,-1],
        [-1,-1,-1,1,-1],
        [-1,-1,-1,1,-1],
        [1,-1,-1,1,-1],
        [1,1,-1,1,-1],
        [1,1,1,0,0],
        [-1,-1,-1,0,0]
    ]

b = [0,0,0,0,0,0,0,1,-1]
c = [0,0,0,1,-1]

print(Simplex(A,b,c))

















        




















    
