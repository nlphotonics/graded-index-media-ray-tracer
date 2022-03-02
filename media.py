#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def getn(r):
    n0 = 1.564
    A = 0.5
    n = n0*np.sqrt(1-A**2 * (r[0]**2+r[1]**2))
    return n

def getdeln(r,n=getn):
    h = 1e-4
    dx = np.array([h,0,0])
    dy = np.array([0,h,0])
    parx = (n(r+dx)-n(r-dx))/(2*h)
    pary = (n(r+dy)-n(r-dy))/(2*h)
    return np.array([parx,pary,0])


def getT(r,s,n=getn):
    return n(r)*s

def getD(r,n=getn,deln=getdeln):
    return n(r)*deln(r)


if __name__ == '__main__':
    from ray import ray
    r0 = ray()
    r0.r = np.array([0.5,0,0])
    r0.s = np.array([0,0,1])
    r0.eikonal = 0
    rays = []    
    rays.append(r0)

    print(getn(rays[0].r))
    print(getdeln(rays[0].r))
    print(getT(rays[0].r,rays[0].s))
    print(getD(rays[0].r))
    
