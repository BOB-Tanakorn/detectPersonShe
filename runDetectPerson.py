import time
import pyodbc

for i in range(1, 13):
    print('2 x {} ='.format(i), int(i*2))
    time.sleep(1)