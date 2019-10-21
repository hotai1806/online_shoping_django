# from django.test import TestCase
import math
# type(c[i]) == int and c == False:
# Create your tests here.
c = True
a = input()
first = 0
second = 0

kq = 0
for i in range(len(a)):
    if a[i] == "+":
        kq += first+second
        c = False
    elif a[i] =="-":
        kq -= first-second
        c = False
    elif a[i] == "/":
        kq += first/second
        c = False
    elif (isinstance(a[i], int) == int) and (c is True):
        first = int(a[i])

    else:
        second = int(a[i])

        c = True
print(kq)
