# # from django.test import TestCase
# import math
# # type(c[i]) == int and c == False:
# # Create your tests here.
# c = True
# a = input()
# first = 0
# second = 0
#
# kq = 0
# for i in range(len(a)):
#     if a[i] == "+":
#         kq += first+second
#         c = False
#     elif a[i] =="-":
#         kq -= first-second
#         c = False
#     elif a[i] == "/":
#         kq += first/second
#         c = False
#     elif (isinstance(a[i], int) == int) and (c is True):
#         first = int(a[i])
#
#     else:
#         second = int(a[i])
#
#         c = True
# print(kq)
#
# # N = int(input())
# # count = int()
# # arr = [[None]*N,[None]*N]
# # print(arr)
# # for a in range(N):
# #   for b in range(1):
# #     arr[a][b] = int(input())
# #
# # for a in range(N):
# #     if(arr[a][0] > arr[a][1]):
# #         for i in range(1):
# #             if (arr[a][0] + arr[i][0]) == arr[a][1]:
# #                 count +=1
# #                 arr[i].pop(0)
# n = int(input())
# a = [None][None] * n
#
# for i range(len(a)-1):
#
myfamily = {
    'Birds' : {
        'BlueOnes': ["detailsAboutBlueBird"],
        'RedOnes' : ["detailsAboutRedBirds"]
    }
}

print(type(myfamily))
print(myfamily['Birds'[1]])
