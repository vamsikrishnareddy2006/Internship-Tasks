# Even Odd Sorter

numbers = []

n = int(input("How many numbers do you want to enter? "))

for i in range(n):
    num = int(input(f"Enter number {i + 1}: "))
    numbers.append(num)

even_numbers = []
odd_numbers = []

for num in numbers:
    if num % 2 == 0:
        even_numbers.append(num)
    else:
        odd_numbers.append(num)

print("\n===== Result =====")
print("Even Numbers:", even_numbers)
print("Odd Numbers :", odd_numbers)