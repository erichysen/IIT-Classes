"""Hard coded variables are on lines 11-12. Just run with Python3 3_philosophers.py"""
from threading import Semaphore, Thread
import time
from time import sleep
import timeit
import random

rand = random.Random()
rand.seed(100)
#***************************************#
num_philosophers = 5
meals = 5
#***************************************#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""each philosopher shares his left and right fork with neighbor.  get fork and put fork
both use the sharing concept to modify individual fork mutexes even though there is only 1 per
philosopher to prevent multiple users from using a fork at the same time."""
class Philosopher:
    def __init__(self, num):
        self.mutex = Semaphore(1)
        self.lfork = num
        self.rfork = (num-1) % num_philosophers
        self.state = "THINKING"
    def __repr__(self): # debug print
        return self.lfork

def get_forks(p):  #right first
    philosophers[int(philosophers[p].rfork)].mutex.acquire()
    philosophers[int(philosophers[p].lfork)].mutex.acquire()

def put_forks(p):
    philosophers[int(philosophers[p].rfork)].mutex.release()
    philosophers[int(philosophers[p].lfork)].mutex.release()
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""
Footman

The "footman" solution: where a single semaphore (a multiplex) limits the number of 
philosophers that can simultaneously "try" to dine.
"""
foot = Semaphore((num_philosophers-1)%num_philosophers)  #limit number of philosophers that can try to dine
def get_left_forks(p) : #left first (same as previous get_forks except acquires l.fork first)
    philosophers[int(philosophers[p].lfork)].mutex.acquire()
    philosophers[int(philosophers[p].rfork)].mutex.acquire()
    
def footman_thread(p):
    rand_num = rand.random()
    num_meals=0     
    while num_meals!=meals:
        foot.acquire()
        get_forks(p)
        num_meals +=1
        sleep (rand_num)
        put_forks(p)
        foot.release()

def Footman() :
    footman_array=[]       
    start = timeit.default_timer()
    for i in range(num_philosophers):
        f_thread = Thread(target=footman_thread, args=[i])
        f_thread.start()
        footman_array.append(f_thread)
    for thread in footman_array:
        thread.join()
    stop = timeit.default_timer()
    print ('1.Footman solution, time elapsed:',str(stop - start)+'s')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""
Left-handed

The "left-handed philosopher" solution: where one of the philosophers attempts to 
pick up his left fork first (whilst all other philosophers start with their right).
"""
def left_handed_thread(p):
    rand_num = rand.random()
    num_meals=0
    while num_meals!=meals:
        if p==0 :
            get_left_forks(p)
            sleep (rand_num)
        else :                  
            get_forks(p)
            sleep (rand_num)
        num_meals +=1               
        put_forks(p)
      
def Left_handed() :
    lefthand_array=[]
    start = timeit.default_timer()
    for i in range(num_philosophers):
        lh_thread = Thread(target=left_handed_thread, args=[i])
        lh_thread.start()
        lefthand_array.append(lh_thread)
    for thread in lefthand_array:
        thread.join()
    stop = timeit.default_timer()
    print ('2.Left-handed solution, time elapsed:',str(stop - start)+'s')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""
Tanenbaum

The Tanenbaum solution: which has philosophers re-checking forks for neighboring, 
hungry philosophers.
"""
mutex = Semaphore(1)

def get_fork_t(p):  #similar to get_fork except tests for adjacent philosophers for their forks
    mutex.acquire()
    philosophers[p].state = 'HUNGRY'
    test(p)
    mutex.release()
    
def put_fork_t(p): #similar to put_fork except starts test to see if neighbors are able to eat after p is done
    mutex.acquire()
    philosophers[p].state = 'THINKING'
    test((p+num_philosophers-1)%num_philosophers)
    test((p-num_philosophers-1)%num_philosophers)
    mutex.release()
    
# test to see if the neighbours are eating
def test(p):
    if philosophers[p].state=='HUNGRY' and  philosophers[(p+num_philosophers-1)%num_philosophers].state!='EATING' \
            and philosophers[(p+1)%num_philosophers].state!='EATING':
        philosophers[p].state='EATING'
        
def tanenbaum_thread(p):
    rand_num = rand.random()
    num_meals = 0
    while num_meals != meals:
        get_fork_t(p)
        sleep(rand_num)
        num_meals+=1
        put_fork_t(p)

def Tanenbaum() :
    tannenbaum_array=[]
    start = timeit.default_timer()
    for i in range(num_philosophers):
        t_thread = Thread(target=tanenbaum_thread, args=[i]) 
        t_thread.start()
        tannenbaum_array.append(t_thread)
    for thread in tannenbaum_array:
        thread.join()
    stop = timeit.default_timer()
    print ('3.Tanenbaum\'s solution, time elapsed:',str(stop - start)+'s')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# main function
if __name__ == '__main__':
    philosophers = []
    for i in range (num_philosophers):
        philosophers.append(Philosopher(i))
    print("Running dining philosophers simulation:", num_philosophers,"philosophers,",meals, "meals each.")
    Footman()
    Left_handed()
    Tanenbaum()