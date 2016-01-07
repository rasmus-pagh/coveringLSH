# Reference implementation of CoveringLSH
# (c) Rasmus Pagh 2016
# Version 1.0
#
# Description: Encodes a collection of binary vectors as integers, creates a data structure to perform nearest neighbor queries under Hamming distance up to a maximum radius r. The procedure buildCovering must be called before buildDataStructure. For details see "Locality-sensitive Hashing without False Negatives" by Rasmus Pagh, Proceedings of SODA 2016.
#
# License: This implementation is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; either version 2.1 of the License, or (at your option) any later version. The implementation is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

from random import randint
from math import floor, log
from sets import Set 

A, infinity = {}, float("inf")
def popcnt(x): return bin(x).count('1')
def dist(x,y): return popcnt(x ^ y)

def buildCovering(d,r):
    for v in xrange(1,2**(r+1)): A[v] = 0
    for i in xrange(d):
        m = randint(1, 2**(r+1)-1)
        for v in xrange(1,2**(r+1)):
            A[v] = A[v] + (1<<i) * (popcnt(m & v) % 2)

def buildDataStructure(S,r):
    D = {}
    for x in S:
        for v in xrange(1,2**(r+1)):
            if not (x & A[v]) in D: D[x & A[v]] = Set()
            D[x & A[v]].add(x)
    return D

def nearestNeighbor(D,r,y):
    best, nn = infinity, None
    for v in xrange(1,2**(r+1)):
        if (y & A[v]) in D:
            for x in D[y & A[v]]:
                if dist(x,y) < best:
                    best, nn = dist(x,y), x
        if best <= floor(log(v+1,2)): return nn
    return None
