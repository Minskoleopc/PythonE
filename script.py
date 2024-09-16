# conditional statement
# one input and multiple comes
# program 1
numT = 17
if numT > 0 and numT <= 5:
    print("10 % discount")
if numT > 5 and numT <= 10:
    print("20 % discount")
if numT > 10:
    print("30 % discount")
    
# program 2
numT = -17
if numT > 0 and numT <= 5:
    print("10 % discount")
elif numT > 5 and numT <= 10:
    print("20 % discount")
elif numT > 10:
    print("30 % discount")
else:
    print("incorrect input")
    
# program 3
marks = 92
if marks > 90:
    print("Grade A")
if marks >= 75:
    print("Grade B")
if marks >= 65:
    print("Grade C")
    

# program 4

marks = 22
if marks > 90:
    print("Grade A")
elif marks >= 75:
    print("Grade B")
elif marks >= 65:
    print("Grade C")
else:
    print("please try again")
    

# program 5
s = 10
t = 5

if s > t:
    print("s is greater")
else:
    print("t is greater")

# program 6

x1 = 1000
x2 = 500
x3 = 200

if x1 > x2 and x1 > x3:
    print("x1 is greater")
elif x2 > x1 and x2 > x3:
    print("x2 is greater")
else:
    print("x3 is greater")


if x1 > x2:
    if x1 > x3:
        print("x1 is greater")
    else:
        print("x3 is greater")
elif x2 > x3:
    print('x2 is greater')
else:
    print("x3 is greater")
    
    
# ternary operator

q = 9
r = 3

if q > r:
    print("q is greater")
else:
    print("r is greater")
    
# statment1 if condition else statement2
print("q is greater") if q > r else print("r is greater")

age = 18
w = "can drive" if age >= 18 else "cannot drive"
print(w)




























    












    
    
    
    
    