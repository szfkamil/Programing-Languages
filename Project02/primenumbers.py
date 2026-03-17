num = int(input("WRITE A NUMBER "))
for i in range(num):
    j=1
    while(i>j):
        if i%(i-j) == 0 and i/(i-j) != i:
            break
        if i/(i-j) == i:
            print(i)
        j+=1
