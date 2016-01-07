# Test program for coveringLSH.py
# (c) Rasmus Pagh 2016
#
# License: This implementation is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; either version 2.1 of the License, or (at your option) any later version. The implementation is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

import code, random, time
from coveringLSH import dist, buildCovering, buildDataStructure, nearestNeighbor

n = 10000
r = 5
d = 25
repetitions = 10000

print "Building data structure with",n,"vectors in",d,"dimensions and maximum radius",r,"..."
buildCovering(d,r)
S = [random.getrandbits(d) for i in xrange(n)] 
D = buildDataStructure(S,r)

def bruteForceNearestNeighbor(S,y):
    best, nn = float("inf"), None
    for x in S:
        if dist(x,y) < best:
            best = dist(x,y)
            nn = x
    return nn

print "Testing correctness..."
for y in xrange(100):
    y = random.getrandbits(d)
    x1 = nearestNeighbor(D,r,y)
    x2 = bruteForceNearestNeighbor(S,y)
    if dist(y,x2) <= r:
        if x1==None: print (bin(y),None,bin(x2))
        elif dist(y,x1)!=dist(y,x2):
            print (bin(y),bin(x1),bin(x2))

print "Testing speed..."
start = time.clock()
for y in xrange(repetitions):
    y = random.getrandbits(d)
    x1 = bruteForceNearestNeighbor(S,y)
print "Brute force:",int(repetitions/(time.clock()-start)),"queries per second"

start = time.clock()
for y in xrange(repetitions):
    y = random.getrandbits(d)
    x1 = nearestNeighbor(D,r,y)
print "CoveringLSH:",int(repetitions/(time.clock()-start)),"queries per second"

code.interact(local=locals())
