Number = int(input("Enter a number: "))
sum_of_even_numbers = 0

for i in range (1 , Number +1):
    if i % 2 == 0:
        sum_of_even_numbers += 1
print("Sum of even numbers from 0 to", Number, "is:", sum_of_even_numbers)