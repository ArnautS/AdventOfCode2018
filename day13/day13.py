#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import re
from collections import deque
from enum import Enum

class TrackType(Enum):
    HORIZONTAL = '-'
    VERTICAL = '|'
    SLASH = '/'
    BACKSLASH = '\\'
    INTERSECTION = '+'

directions = {'^' : 0, '>' : 1, 'v' : 2, '<' : 3}
cartTracktypes = {'^' : TrackType.VERTICAL, 'v' : TrackType.VERTICAL,
                  '>' : TrackType.HORIZONTAL, '<' : TrackType.HORIZONTAL}
carts = []

class Cart:    
    def __init__(self, direction):
        self.direction = deque(directions)
        self.direction.rotate(-directions[direction])
        self.turns = deque(['left','straight','right'])
        self.moved = False
        
    def __str__(self):
        return self.direction[0]
        
    def turnLeft(self):
        self.direction.rotate(1)
        
    def turnRight(self):
        self.direction.rotate(-1)
        
    def turnAtIntersection(self):
        if self.turns[0] == 'left':
            self.turnLeft()
        elif self.turns[0] == 'right':
            self.turnRight()
        self.turns.rotate(-1)
        
    def turnAtSlash(self): # /
        if self.direction[0] in '<>':
            self.turnLeft()
        elif self.direction[0] in '^v':
            self.turnRight()
            
    def turnAtBackslash(self): # \
        if self.direction[0] in '^v':
            self.turnLeft()
        elif self.direction[0] in '<>':
            self.turnRight()
            
class Track:
    def __init__(self, char):
        if char in [x.value for x in list(TrackType)]:
            self.type = TrackType(char)
            self.cart = None
            self.value = char
        elif char in cartTracktypes:
            self.type = cartTracktypes[char]
            self.cart = Cart(char)
            carts.append(self.cart)
            self.value = self.type.value
        else:
            self.type = None
            self.cart = None
            self.value = char       
            
    def __str__(self):
        if self.cart == None:
            return self.value        
        else:
            return self.cart.direction[0]
        
    def setCart(self, cart):
        self.cart = cart
        
    def removeCart(self):
        self.cart = None
        

def moveCart(track, row, col):
    cart = track.cart
    if cart.direction[0] == '>':
        nextTrack = tracks[row, col+1]
    elif cart.direction[0] == '<':
        nextTrack = tracks[row, col-1]
    elif cart.direction[0] == '^':
        nextTrack = tracks[row-1, col]
    elif cart.direction[0] == 'v':
        nextTrack = tracks[row+1, col]
    
    if nextTrack.cart == None:
        cart.moved = True
        nextTrack.cart = cart
        track.removeCart()
    else:
        return True, nextTrack
    
    if nextTrack.type == TrackType.INTERSECTION:
        cart.turnAtIntersection()
    elif nextTrack.type == TrackType.SLASH:
        cart.turnAtSlash()
    elif nextTrack.type == TrackType.BACKSLASH:
        cart.turnAtBackslash()
    return False, nextTrack
        
def prettyPrinter(data):
    for row in data:
        print(''.join([str(col) for col in row]))


# In[2]:


tracks = np.array([[Track(char) for char in line] 
                 for line in open('input.txt','r').read().splitlines()])
firstCrash = True
while len(carts) > 1:
    for row, trackrow in enumerate(tracks):
        for col, track in enumerate(trackrow):
            if track.cart == None:
                continue            
            elif not track.cart.moved:
                crashed, nextTrack = moveCart(track, row, col)
                if crashed :
                    carts.remove(track.cart)
                    track.removeCart()
                    carts.remove(nextTrack.cart)
                    nextTrack.removeCart()
                    if firstCrash:
                        print(col,row)
                        firstCrash = False
    for cart in carts:
        cart.moved = False
        
for row, trackrow in enumerate(tracks):
    for col, track in enumerate(trackrow):
        if track.cart == None:
            continue
        else:
            print(col,row)
            break



# In[ ]:




