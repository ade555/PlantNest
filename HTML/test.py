num = [i for i in range(5)]
new = [0,1,2,3,4,4,3,2,1,2,3,4,2,1,2,3,4]

for n, n2 in zip(num, new):
    print(" num is ", n)
    print(" new is ", n2)

