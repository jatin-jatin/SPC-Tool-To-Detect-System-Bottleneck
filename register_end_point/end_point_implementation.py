import timeit
import time
def sys_check_fun():
    y=0
    x=timeit.default_timer()
    while timeit.default_timer() - x < 0.01:
        y=y+1
        

x=timeit.default_timer()
sys_check_fun()
y=timeit.default_timer()
print(y-x)
