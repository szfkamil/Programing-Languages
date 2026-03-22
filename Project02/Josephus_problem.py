numbers = []
k = 1
n = int(input("Enter a number for Josephus problem: "))
for i in range(n):
    numbers.append(i+1)
while len(numbers) > 1:
    numbers.pop(k)
    if len(numbers) > 0:
        k = (k + 1) % len(numbers)
print("The survior is number",numbers[0])