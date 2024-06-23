from django.test import TestCase
import time
# Create your tests here.
time_local = time.localtime(1486720211)
print(time.localtime(1486720211))
dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
print(dt)
str_time = int(time.time())
time_local2 = time.localtime(str_time)
dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local2)
print(str_time)
print(dt)
