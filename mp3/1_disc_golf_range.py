"""Hard coded variables are on lines 27-29. Just run with Python3 1_disc_golf_range.py"""
from threading import Semaphore, Thread
from time import sleep
import random
"""
UNSYNC CODE
# frolfer
while True:
    stash -= N                # call for bucket
    for i in range(0,N):      # for each disc in bucket,
        discs_on_field += 1   # throw (maybe simulate with a random sleep)

# cart
while True:
    stash += discs_on_field   # collect discs and deposit in stash
"""

rand = random.Random()
#rand_num = rand.seed(100)

MAX_CART_RUNS = 10 #change this to number of times cart can fetch discs currently IS [IS NOT] in use.

class frolf_game:
	def __init__(self):
		#self.discs = 0 not needed
#***************************************#
		self.frolfers = 3 #frolfers playing	
		self.stash = 20   #20 discs in the stash
		self.bucket= 5    #5 discs per bucket
#***************************************#
		self.thrown = 0   #discs thrown
		self.cart_cycles=0 ##times cart has fetched discs 
	
game=frolf_game()
mutex = Semaphore(1)  									#for changing frolf_game attributes
cart = Semaphore(0)
stash_empty = Semaphore(0) 
throwing = Semaphore(1)									#protect multiple player threads from throwing and modifying thrown disc shared data

def player_thread(player):
	global game
	rand.seed(100)                      				#rand number seed
	rand_num=rand.random()             
   # while(game.cart_cycles<MAX_CART_RUNS):   			#change condition to true for infinite looping
	while(1):
		mutex.acquire()                     			# block from other threads changing frolf_game vars
		print('Frolfer',player,'calls for the bucket.')
		if game.stash >= game.bucket:                   #first frolfer calls for the bucket
			game.stash = game.stash-game.bucket   		#fix stash after bucket filled
			print('Frolfer',player,'got',game.bucket,'discs; ','Stash = ',game.stash)
		else:
			stash_empty.release()                 		#stash empty, permit cart to refill. Block throwing.
			cart.acquire()                      
            #print("debug")
			game.stash = game.stash-game.bucket			#fix stash after bucket filled
			print('Frolfer',player,'got',game.bucket,'discs;','Stash = ',game.stash)
		mutex.release()                      			#permit modification of frolf_game variables
		for i in range(game.bucket):        
			throwing.acquire()             	   			#block to avoid thrown disc contention between frolfers
			print('Frolfer',player,'threw disc:',i)
			game.thrown +=1								#cs
			throwing.release()             				#unblock for other throwers. Can be preempted in loop for concurrent throwing.
			sleep (rand_num)

def cart_thread():                            		    #blocks throwers from throwing while reclaiming thrown discs.
	global game
	#while(game.cart_cycles<MAX_CART_RUNS): 
          												#^can be replaced with 1 to continue forever.
	while(1):
		stash_empty.acquire()
		print('################################################################################')
		print('Stash = ', game.stash,'disc[s];',' Cart entering the field!')
		game.stash += game.thrown
		print('Cart done, gathered ',game.thrown,' discs; ','Stash =',game.stash, 'discs.')
		game.thrown = 0
		print('################################################################################')
		game.cart_cycles+=1								#debug
		cart.release()                     				#only cart

if __name__ == '__main__':
	c = Thread(target= cart_thread)
	c.start() 
	for i in range (game.frolfers):						#thread for each player
		p = Thread(target=player_thread,args=[i]) 
		p.start()
