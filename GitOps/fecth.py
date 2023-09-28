
import operator as op


bl = ['backup']

ls = '2015_7BACKUP'


for i in bl:
    res=op.contains(ls, i)
    print(res)


dct = {'a':['abc','bcd']}

print(dct['a'])