from threading import Thread
import threading
from queue import Queue
import schedule
import time
import random
import math

# generate random number pair (x,y) every 0.01 seconds
# save a random number pair in Queue
# process queue & calculate 
# Python Standard Queue is basically Thread-safe

"""
    !!! In python, only one Thread can execute at the same time.
    !!! Python GIL(Global Interpreter Lock) permit only one thread
"""

data_size = 0
incircle_size = 0
probability = 0.0

# Get GIL
lock = threading.Lock()

def gen_num(q):
    x = random.random()
    y = random.random()
    q.put((x,y))

# get distance from (0,0)
def get_distance(x,y):
    return math.sqrt(x**2 + y**2)
    
def reduce(q):

    # get GIL
    lock.acquire()

    global data_size
    global incircle_size
    global probability

    data_size = data_size + q.qsize()

    while q.qsize():
        coord_x, coord_y = q.get()
        if get_distance(coord_x,coord_y) < 1:
            incircle_size = incircle_size + 1

    if data_size:
        probability = incircle_size / data_size

    # Release GIL
    lock.release()

    print(probability * 4)

if __name__ == '__main__':

    inputq = Queue()

    # execute all tasks in schedule
    schedule.every(0.01).seconds.do(gen_num,inputq)

    while True:
        schedule.run_pending()

        if inputq.qsize() > 10:
            t = Thread(target=reduce,kwargs={'q':inputq})
            t.start()

        time.sleep(0.001)
        