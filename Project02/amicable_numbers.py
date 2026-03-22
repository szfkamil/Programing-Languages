limit = int(input("select a limit number "))
def suma_dzielnikow(number):
    sum = 0
    for j in range(1,number):
        if number%j == 0:
            sum += j 
    return sum

for i in range (4,limit):
    suma = suma_dzielnikow(i)
    if suma_dzielnikow(suma) == i and suma > i:
        print(f"nasze liczby to {i} oraz {suma}") 