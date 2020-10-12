#!/usr/bin/python3

import os
from os import path
import sys
import re
import copy
import string
from functools import reduce
import stat

def NameOf(A):
  return A.__name__

###
def LOG2(x):
  from math import ceil,log
  return int(ceil(log(x)/log(2)))


def CP(a):
  return copy.deepcopy(a)



def RXC(*args, **kwargs):
  return re.compile(*args, **kwargs)

def RXS(rx, *args, **kwargs):
  return re.search(rx, *args, **kwargs)


def RXM(rx, *args, **kwargs):
  return re.match(rx, *args, **kwargs)


def ST(f):
  return string.Template(f)
def TSP(f, *args, **kwargs):
  return f.substitute(*args, **kwargs)

def STSP(f, *args, **kwargs):
  return TSP(ST(f), *args, **kwargs)



def prt(*args, **kwargs):
  def SPC(c):
    return "  "*c
  L = 1
  if "l" in kwargs:
    L = kwargs["l"]
  if L > 1:
    print()
  H = ''
  if "h" in kwargs:
    H = kwargs['h']
  for arg in args:
    if isinstance(arg, list):
      print(SPC(L),"[ ", H)
      for i,v in enumerate(arg):
        print(SPC(L+1), i, ":", v, ", ")
      print(SPC(L),"]")
    elif isinstance(arg, tuple):
      print(SPC(L),"( ", H)
      for i,v in enumerate(arg):
        print(v, ", ", end=' ')
      print(")")
    elif isinstance(arg,set):
      print(SPC(L), "set( ", H)
      for i,v in enumerate(arg):
        print(SPC(L+1),v, ", ")
      print(SPC(L), ")")      
    elif isinstance(arg, dict):
      print(SPC(L), "{ ", H)
      for k, v in arg.items():
        print(SPC(L+1), k, ": ", end=' ')
        prt(v, l=L+2), ", "
      print(SPC(L), "}")
    else:
      print(SPC(L), arg)

def InitDbg(s):
  DebugHelper.__init__(s)


def OR(a, b):
  return a | b


def AND(a, b):
  return a & b


def DebugFlags(*args):
  rtn = set([])
  for arg in args:
    if isinstance(arg,set):
      rtn = rtn | arg
    elif isinstance(arg, list) or isinstance(arg, tuple):
      rtn = rtn | reduce(OR, [ DebugFlags(arg1) for arg1 in arg ])
    elif isinstance(arg, int) or isinstance(arg, str) or isinstance(arg, type):
      rtn = rtn | set([arg])
    else:
      rtn = rtn | set([arg])      
  return rtn


class DebugHelper(object):
  """ flag to set debugging flags """
  __debug_on__ = [set([])]

  def __init__(s):
    s.__debug_class__ = set([s.__class__])

  def Debugging(s, *f):
    flags = DebugFlags(*f) | s.__debug_class__
    return (DebugHelper.__debug_on__[-1] & flags)==flags
      
  def DBG2(s, f, *args, **kwargs):
    if s.Debugging(f):
      print(NameOf(s.__class__), "::", end=' ') 
      for k in args:
        print(k, end=' ')
      print()
  def DBG(s, *args, **kwargs):
    if s.Debugging():
      print(NameOf(s.__class__), "::", end=' ') 
      for k in args:
        print(k, end=' ')
      print()

def IsDebugging(*f):
  flags = DebugFlags(*f) 
  return (DebugHelper.__debug_on__[-1] & flags)==flags


def CurrDebugFlags(id=-1):
  return DebugHelper.__debug_on__[id]

def DebugNow(*args, **kwargs):
  f = DebugFlags(*args, **kwargs)
  if DebugHelper in CurrDebugFlags():
    print("setting debug flags to", f)
  DebugHelper.__debug_on__[-1] = f

def GlobalDebug(f, *args):
  if IsDebugging(f):
    print(NameOf(f.__class__), "::", end=' ')
    for k in args:
      print(k, end= ' ')
    print()

## push a debuggings state
def DebugPush(*args):
  f = DebugFlags(*args)
  if DebugHelper in CurrDebugFlags():
    print("setting debug flags to", f)
  DebugHelper.__debug_on__.append(f)

def DebugPop():
  if len(DebugHelper.__debug_on__) > 1:
    rtn = DebugHelper.__debug_on__[-1]
    DebugHelper.__debug_on__ = DebugHelper.__debug_on__[:-1]
    return rtn
  return DebugHelper.__debug_on__[-1]
