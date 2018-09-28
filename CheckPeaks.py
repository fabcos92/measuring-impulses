# Checking highest impules in the data

'''lst2 = [1,2,3,4,5,6,7,8,9,8,7,6,7,4,3,2,1]
lst = [1,6,3]
res = next(i for i, j in zip(lst, lst[1:]) if j < i)
res2 = [i for i, j in zip(lst, lst[1:]) if j <= i]
res3 = [j for i, j, k in zip(lst, lst[1:], lst[2:]) if i < j and i == k]


lst3 = [1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1]

for i in range(len(lst)):
    if lst3[i-1] < lst3[i] and lst3[i-1] == lst3[i+1]:
        print(lst3[i])

lst4 = [1,2,3,4,5,6,7,8,9,8,7,6,5,6,3,2,1]


for i in range(len(lst4)):
    if lst4[i-1] < lst4[i] and lst4[i-1] == lst4[i+1]:
        print(lst4[i])


# 9'''

lst = [10,20,30,40,30,20,70,10,20,10,20,30,40,50,60,70,80,60]
lst2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]

sup = list(zip(lst,lst2))
res = [j for i, j, k in zip(sup, sup[1:], sup[2:]) if i < j and j > k and j[0] >= 30.0]

print res
