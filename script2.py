# loop
# while loop (until the condition is met),for loop(definite number of times)
# range(startIndex,Endindex,Stepsize)
# range(startIndex,Endindex) // stepSize by default 1
# range(EndIndex(not included))// startIndex - 0 stepsize -1 

# print 0 to 9
# program 1
for x in range(10):
    print(x)

# print 1 to 9
# program 2
for x in range(1,10):
    print(x)

# print 1 to 10
#program 3
# 1     2     3     4     5     6      7     8    9   10
for x in range(1,11,2):
    print(x)

# table of 2
# program 4
for x in range(2,21,2):
    print(x)

# table of 5
# program 5
for x in range(5,51,5):
    print(x)

# program 6
# print in reverse table to 2
for x in range(20,1,-2):
    print(x)

# program 7
# print table of 5 in reverse
for x in range(50,4,-5):
    print(x)

# program 8
for x in range(3):
    print('hello world !')

# program 9
# break statement with for loop

for x in range(1,6): # x-2 # x - 3
    if x == 3:
        break
    print(x) # 1 # 2


for x in range(1,6):  # 2 # 3
    print(x) # 1 # 2 #3
    if x == 3:
        break
  
for x in range(5,0,-1): #4 # 3
    if x == 3:
        break
    print(x) # 5 # 4



















