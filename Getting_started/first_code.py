# basic syntax

from sys import modules


print ( 1 + 1 )

# Declaring and assigning variable

num1 = int (input ("Enter a number1 : "))
num2 = int (input ("Enter a number2 : "))

sum = num1 + num2
diff = num1 - num2
product = num1 * num2
div = num1 / num2
floor_div = num1 // num2
modules = num1 % num2
exponent_result = num1 ** num2

if (num1 > num2):
    print ("Number1 is greater")
elif (num1 == num2):
    print ("Number1 is equal to Number2")
else:
    print ("Number2 is greater")


print ("Sum is : " , sum)
print ("Difference is : " , diff)
print ("Product is : " , product)
print ("Quotient is : " , div)
print ("floor division is : ", floor_div)
print ("modules is : ",modules)
print ("Exponent is : ", exponent_result)

# logical operators 


#  if statement 

age = 20

if age < 13 :
    print ("kid")
elif age >= 18 :
    print ("you're elegible voter")
else :
    print ("uncle")

# nested if else 

year= int (input ("Enter the year: "))

if year%4 == 0:
    if year%100 == 0:
        if year%400 == 0:
            print ("It's a leap year")
        else:
            print (year , "is not a leap year")
    else:
        print (year, "is a leap year")
else:
    print(year, "is not a leap year")

# for loops 

# for i in range (0,5) :
#     print (i)

# generally there are 3 parameters in the loop (start,end,step)
# step is nothing number of step it will jump after each iteration

# for i in range (0,6,3):
#     print (i)

'''
output: 
0
3
'''
for i in range (10,6,-1):
    print (i)

str = "omkar joshi"

for i in str:
    print (i)

# while loop

count = 0

while count < 5 :
    print (count)
    count = count + 1

# the pass statement is the null operation, it does nothing

# sum of n natural number 

num = int(input ("Enter a number : "))
sum = 0
Count = 1

while Count <= num :
    sum = sum+Count
    count +=1

print ("Sum of n n natural number is : ",sum)

