"""Hard coded variables are on lines 9-11. Just run with Python3 2_dance_mixer.py"""
from threading import Semaphore,Thread
import time
from time import sleep
import random
from itertools import cycle
from collections import deque
#***************************************#
num_leaders = 3
num_followers = 5
song_length = 5
#***************************************#
pair = [None]*2
rand = random.Random()
rand.seed(100)

class ballroom:
    def __init__(self):
        self.song_time = song_length
        self.music_list = ['Dubstep','Taylor Swift','Michael Jackson','Livin La Vida Loca']
        self.dancing = Semaphore(0)
        self.waiting = Semaphore(0)
        self.leaderSem = Semaphore(0)
        self.followerSem = Semaphore(0)
        self.mutex = Semaphore(1)
        self.dancers = 0
        self.closed = True
        self.music_on = True
br = ballroom()

def open_floor():
    br.dancing.release()
def close_floor():
    br.dancing.acquire()
    br.waiting.acquire()
def enter():
    br.dancing.acquire()
    br.mutex.acquire()
    br.dancers += 1
    br.mutex.release()
    br.dancing.release()
def line_up():
    br.mutex.acquire()
    br.dancers -= 1
    if br.dancers == 0 and  br.closed:
        br.waiting.release()
    br.mutex.release()

class dance_queue:
    global br
    leader_queue = deque()
    follower_queue = deque()
    leaders = Semaphore(0)
    followers = Semaphore(0)
    def append(type, waitingSem):
        if type == "Leader":
            dance_queue.leader_queue.appendleft(waitingSem)
            dance_queue.leaders.release()
        else:
            dance_queue.follower_queue.appendleft(waitingSem)
            dance_queue.followers.release()
    def pop():
        dance_queue.leaders.acquire()
        dance_queue.followers.acquire()
        popped_leader = dance_queue.leader_queue.pop()
        popped_leader.release()
        popped_follower = dance_queue.follower_queue.pop()
        popped_follower.release()

class Dancer:
    def __init__(self, num, type):
        global br
        self.type = type
        self.num = num
        self.waitingSem = Semaphore(0)
        self.partner = None
        if type == "Leader": #leader wait
            self.arrivedSem = br.leaderSem
            self.partnerSem = br.followerSem
        else:               #follower wait
            self.arrivedSem = br.followerSem
            self.partnerSem = br.leaderSem
    #def set_partner(dancer):
        #self.partner=dancer

    def __repr__(self):  #prints out the dancer and the number associated with them
        return self.type+" "+str(self.num)
    
    def dance(self):
        global br
        dancing_time = rand.random()
        while(1):
            dance_queue.append(self.type, self.waitingSem)
            self.waitingSem.acquire()
            enter()
            if br.music_on == False: #see if dancing can begin
                break
            print(self.type+" "+ str(self.num) + " entering floor")

            if self.type == "Leader":
                self.partnerSem.acquire()
                pair[0]=self
                self.arrivedSem.release()
                if pair[0] and pair[1]:
                    print("Leader "+ str(pair[0].num) + " and Follower " + str(pair[1].num) + " are dancing.")
                    #print(pair[0]+ " and  " + pair[1] + " are dancing.")
                dance_queue.pop()
            else: 
                pair[1]=self
                self.arrivedSem.release()
                self.partnerSem.acquire()
            sleep(dancing_time)
            line_up()#line back up 
            print(self.type+" "+ str(self.num)+ " is getting back in line.")

def start_music(dance):
    print("\n** Band Leader started playing " + dance + " **")
    open_floor()
def end_music(dance):
    close_floor()
    print("** Band Leader stopped playing " + dance + " **\n")

#dj changes music and opens/closes the dance floor
def dj_thread():
        dance_queue.pop() #get first pair released for dance
        for dance in cycle(br.music_list):
            start_music(dance)
            sleep(br.song_time)
            end_music(dance)
#d = dj()

if __name__ == '__main__':
    
    # dj
    dj = Thread(target= dj_thread)
    leaders_array =[]
    followers_array = []
    dancing_time = rand.random()
    dancer_array = []

    for i in range(num_leaders):
        l = Dancer(i,"Leader")
        dancer_array.append(l)
        leaders_array.append(Thread(target = l.dance))
        #leaders_array.append(Thread(target = l.dance, args=(l,)))
        leaders_array[i].start()

    for i in range(num_followers):
        f = Dancer(i,"Follower")
        dancer_array.append(f)
        followers_array.append(Thread(target = f.dance))
        #followers_array.append(Thread(target = f.dance, args=(f,)))
        followers_array[i].start()

    dj.start()
    dj.join()
    #sleep(dancing_time)
    br.music_on = False
    open_floor()
    for dancer in dancer_array:
        dancer.waitingSem.release()
    for i in range(0, num_leaders):
        leaders_array[i].join()
    for i in range(0, num_followers):
        followers_array[i].join()
