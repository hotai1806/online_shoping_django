from django.test import TestCase
import math
# Create your tests here.

a = float(5)
b = float(6)
c = float(10)
kq1 = math.sqrt((a*c) - math.pow(b,2))
kq2 = math.sqrt(math.pow(a,2)+ math.pow(b,2))
kq = kq1/kq2
print(kq)
