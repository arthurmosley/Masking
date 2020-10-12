#!/usr/bin/python3
import sys
#from os import *
import os
import string
import inspect
import re
import tempfile 
import filecmp
import pprint
import time
import copy

import random

from MyStuff3 import *
from operator import itemgetter, attrgetter

class DirectedGraph:
  V = []
  W = []
  E = []
  A = []
  def __init__ (s, N):
    """
    """
    s.V = range(0,N)
    s.E = []
    s.A = []
    s.W = []
  
  def addNode(s, N):
    """ N must be a scalar number value
    """
    s.V.append(N)
  def addNodes(s, Nset):
    """ Nset must be a list of scalar number values
    """
    s.V.extend(Nset)
    
  def addEdge(s, src, dst):
    s.E.append([src,dst])

  def add2Edges(s, src,dst):
    s.addEdge(src,dst)
    s.addEdge(dst,src)

  def addEdges(s, src, dstlist):
    for dst in dstlist:
      s.addEdge(src,dst)

  def addDblEdges(s, src, dstlist):
    for dst in dstlist:
      s.add2Edges(src,dst)
      
  def SetUp(s):
    """call after all nodes and edges have been defined
    """
    s.W = [ { 'id':i, 'out':[], 'in':[] } for i in s.V ]
    s.E.sort()
    s.A = [ [0 for i in s.V] for j in s.V ]
    for [r,c] in s.E:
      # do not process repeat edges
      if r < len(s.V) and c < len(s.V):
        if s.A[r][c] == 0:
          s.A[r][c] = 1
          s.W[r]['out'].append(c)
          s.W[c]['in'].append(r)
      else:
        print("error!", r,c,"|V|=",len(s.V),"|E|=",len(s.E))
        
  def Init(s, Nset, Eset):
    s.V = Nset
    s.E = Eset
    s.SetUp()

def Transpose(dg):
  """ return a new dg which is the transpose of the argument """
  Eset = [[b,a] for [a,b] in dg.E]
  rtn = DirectedGraph(len(dg.V))
  rtn.E = Eset
  rtn.SetUp()
  return rtn


def floyd(dg):
  """
  Floyd Warshalll's all pairs shortest path
  """
  A = copy.deepcopy(dg.A)
  for y in dg.V:
    for x in dg.V:
      if A[x][y]:
        for j in dg.V:
          if A[y][j] > 0:
            if (A[x][j]==0 or (A[x][y]+A[y][j]<A[x][j])):
              A[x][j] = A[x][y] + A[y][j]
  return A


def Top(s):
  return s[len(s)-1]

def SetTop(s, v):
  s[len(s)-1] = v

def Node(t):
  return t[0]

def Where(t):
  return t[1]



class dgGen(DirectedGraph):
  """
  Simple statemachine to generate a DG
  """
  V = []
  W = []
  E = []
  A = []

  def __init__(s, v, e):
    """
    Random state st,
    #vertices, #edges
    """
    ## random.seed(st)

    s.Init(list(range(v)), random.sample([[i, j] for i in range(v) for j in range(v)], e))

#**********************************************************************
# Non recursive version of the basic depth first search, via Cormen.
# Has identical output to the recursive version.
class BasicDFS(DebugHelper):
  Color = []
  T = 0
  Time = []
  Parents = []
  White = 0
  Gray = 1
  Black = 2

  TreeEdge = 1
  BackEdge = 2
  ForwEdge = 3
  OtherEdge = 4

  pathT = ST("($a->$b) ")
  a1 = ST("$a -> $b\n")
  Traverse = 0
  AllLoops = []

  def __init__(s,dg):
    InitDbg(s)
    s.dg = dg
    s.BackEdges = []
    s.ForwEdges = []
    s.CrossEdges = []
    s.DiscoverTime = [ 0 for i in dg.V ]
    s.FinishTime = [ 0 for i in dg.V ]
    s.Parents = [ -1 for i in dg.V ]
    # 0 = undiscovered
    s.Color = [ s.White for i in dg.V ]
    s.visitedNodes = [ 0 for i in dg.V ]
    s.visitedEdges = [ [ 0  for i in dg.V ] for j in dg.V ]
    s.AllLoops = []
    s.Traverse = s.DFSTraversal
    s.AllPaths = []

  def AllowVisit(s,n):
    return s.Color[n] == s.White
  def Visit(s,n):
    if s.Color[n] == s.White:
      if s.Debugging():
        print("Coloring",n,"Gray at",s.T)
      s.DiscoverTime[n] = s.T
      s.Color[n] = s.Gray
  def Finish(s,n):
    if s.Color[n] != s.Black:
      if s.Debugging():
        print(STSP("Coloring $n Black at $T",n=n,T=s.T))
      s.FinishTime[n] = s.T
      s.Color[n] = s.Black

  def SrcNode(s,e):
    return e[0]
  def DstNode(s,e):
    return e[1]

  def TraverseEdge(s, a, b):
    ## s.text- = s.text + s.a1.substitute(a=a,b=b)
    s.path.append([a, b])
    if s.Parents[b] == -1:
      s.Parents[b] = a
    if s.Debugging():
      print(STSP("Forw $a->$b len(path)=$l",a=a,b=b,l=len(s.path)))

  def ProcessBackEdge(s, a, b):
    i =  0
    P = []
    s.BackEdges.append([a,b])
    s.path.append([a,b])
    for [x,y] in reversed(s.path):
      #if s.Debugging():
      #  print "considering ",x,"->",y
      P.append([x,y])
      if x == b:
        break
    P.reverse()
    if s.Debugging():
      print( "BackEdge",a,"->",b," (loop) ",P, "len(path)=",len(s.path))
    s.path.pop()
    s.AllLoops.append(P)

  def ProcessOtherEdge(s, a, b):
    if s.DiscoverTime[a] < s.DiscoverTime[b]:
      s.ForwEdges.append([a,b])
      if s.Debugging():
        print("rejecting",a,"->",b," as a forward edge")
      pass
    else:
      s.CrossEdges.append([a,b])
      if s.Debugging():
        print("rejecting",a,"->",b," as a cross edge")
      pass 


  def fVisitedEdges(s):
    pass
  def fVisitedNodes(s):
    if s.Debugging():
      print("Discovered Total of",len(s.AllLoops),"Unique Loops")
      for p in s.AllLoops:
        pTxt = "["
        for [x,y] in p:
          pTxt = pTxt + TSP(s.pathT, a=x,b=y)
        print ("Loop Found with",len(p),"hops",pTxt,"]")

      print("Discover Time/Finish Time")
      for i in s.dg.V:
        print(i,":",s.DiscoverTime[i],"/",s.FinishTime[i])

  def prt(s, *args, **kv):
    l = 2
    if "l" in kv:
      l = kv["l"]
    SPC = " "*l;
    print(STSP(SPC + "{ $arg", arg=args));
    for v in s.dg.V:
      print(STSP(SPC + "  $v  p:$p $d/$fin", v=v, p=s.Parents[v],
                 d=s.DiscoverTime[v],
                fin=s.FinishTime[v]))
    print(SPC + "}");

  def DFSTraversal(s, stack):
    """Basic DFS
    """
    s.path = []
    while len(stack) > 0:
      top = Top(stack)
      node = Node(top)
      c = 0
      ## print "stack:", stack
      ## first time visiting this node
      s.Visit(node)
      s.T = s.T + 1
      lastVisit = Where(top)
      for e in range(lastVisit, len(s.dg.W[node]['out'])):
        dst = s.dg.W[node]['out'][e]
        top[1] = top[1] + 1
        if s.AllowVisit(dst):
          c = c + 1
          s.TraverseEdge(node, dst)
          stack.append([ dst, 0 ])
          break
        elif s.Color[dst] == s.Gray:
          s.ProcessBackEdge(node, dst)
        elif s.Color[dst] == s.Black:
          s.ProcessOtherEdge(node, dst)
      if c == 0:
        s.Finish(node)
        stack.pop()
        # s.path.pop()
        if s.Debugging():
          print("Path is now",s.path)
    s.AllPaths.append(s.path)

class SCC(DebugHelper):
  def __init__(s, dg):
    InitDbg(s)
    s.G = dg
    s.dfs1 = BasicDFS(dg)
    for v in s.G.V:
      s.dfs1.DFSTraversal([[v, 0]])
    s.GT = Transpose(s.G)
    s.dfs2 = BasicDFS(s.GT)
    ByFT = [ [v, s.dfs1.FinishTime[v]] for v in s.G.V ]
    Sorted = sorted(ByFT, key=itemgetter(1), reverse=True)
    for v, ft in Sorted:
      s.dfs2.DFSTraversal([[v, 0]])

    P = [ s.dfs2.Parents[v] for v in dg.V ]
    for v in dg.V:
      if P[v] == -1:
        P[v] = v

    Changed = True
    IT = 0

    R = [ set() for v in dg.V ]

    for u, v in dg.E:
      R[P[u]] = R[P[u]] | set([v])

    while Changed == True:
      Changed = False
      IT = IT + 1
      for u, v in dg.E:
        L = len(R[P[u]])
        R[P[u]] = R[P[u]] | R[P[v]]
        if len(R[P[u]]) != L:
          Changed = True

    CM = [ [ 0 for v in dg.V ] for u in dg.V ]
    for u in dg.V:
      for v in R[P[u]]:
        CM[u][v] = 1

    s.Info = [ ( v, P[v], (s.dfs2.DiscoverTime[v], s.dfs2.FinishTime[v]), R[v]) for v in dg.V ]
    s.CM = CM
    s.R = R
    s.P = P
    s.IT = IT

    if s.Debugging():
      print("{", IT);
      print("  ", s.G.E); prt(s.G.A, h='Orig');
      prt(s.CM, 'CM')
      print("}");



class DGConnected(DebugHelper):
  def ID(s, v):
    return s.Info[v][0]
  def setID(s, v, k):
    s.Info[v][0] = k
  def R(s, v):
    return s.Info[v][1]
  def F(s, v):
    return s.Info[v][2]
  def mergeR(s, v, k):
    if isinstance(k, set):
      s.Info[v][1] = s.Info[v][1] | k
    elif isinstance(k, list):
      s.Info[v][1] = s.Info[v][1] | set(k)
    elif isinstance(k, int):
      s.Info[v][1] = s.Info[v][1] | set([k])

  def __init__(s, dg):
    InitDbg(s)
    s.Info = [ [len(dg.V)+1, set(), False] for v in dg.V ]
    for (u, v) in dg.E:
      # s.setID(u, min(s.ID(u),u))
      # print(STSP("$u -> $v ID(u)=$uid ID(v)=$vid",
      #            u=u,v=v,uid =s.ID(u), vid=s.ID(v)))
      s.mergeR(u, set([v]))
    Changed = True;
    s.IT = 0;
    while Changed:
      Changed = False
      s.IT = s.IT + 1
      for u in dg.V:
        LL = len(s.R(u))
        for v in s.R(u):
          s.mergeR(u, s.R(v))
        if LL != len(s.R(u)):
          Changed=True
    s.CM = [ [ 0 for v in dg.V ] for u in dg.V ]
    for u in dg.V:
      for v in s.Info[u][1]:
        s.CM[u][v] = 1
    if s.Debugging():
      fg = floyd(dg)
      print("{");
      prt(dg.A, h="Orig")
      prt(s.CM, h='Connection')
      prt(fg, h='floyd')
      print("}");

  def isConnected(s, u, v):
    return v in s.R(u)



def TestGraph(N, E, C):
  for x in range(C):
    dg = dgGen(N, E)
    fg = floyd(dg)
    scc = SCC(dg)
    CC = DGConnected(dg)
    Break = False;
    Rtn = []
    if CC.IT != scc.IT:
      Rtn.append(copy.deepcopy(dg))
    if IsDebugging(TestGraph):
      print(STSP(' Graph of |$V|,|$E| took $IT $IT2', 
                 V=len(dg.V), E=len(dg.E), IT=CC.IT, IT2=scc.IT), end=' ')
      if CC.IT < scc.IT:
        print()
        prt(dg.A, h='Orig');
        prt(scc.R, h='SCC R')
        prt(CC.Info, h='DGC R')
      elif CC.IT > scc.IT:
        print('****')
      else:
        print()

    for u in dg.V:
      for v in dg.V:
        A = fg[u][v] > 0
        B = CC.isConnected(u, v)
        C = scc.CM[u][v] > 0
        if A != B and A != C:
          print(STSP("  $u -> $v ? $A vs $B", u=u,v=v, A=A,B=B));
          ## print("  edges", dg.E)
          prt(dg.A, h='Orig');
          prt(fg, h='FG');
          prt(CC.CM, h='CM')
          prt(CC.Info, h='CCInfo')
          prt(scc.CM, h='SCC CM')
          Break = True;
          break;
      if Break:
        break
  return Rtn



def TestGraph2(N, E, C):
  for x in range(C):
    dg = dgGen(N, E)
    fg = floyd(dg)
    scc = SCC(dg)
    Break = False;
    Rtn = []
    Appended = False
    if len(scc.dfs1.AllLoops) != len(scc.dfs2.AllLoops):
      Rtn.append(dg)
      Appended = True
    for u in dg.V:
      for v in dg.V:
        A = fg[u][v] > 0
        B = scc.CM[u][v] > 0
        if A != B:
          # Break = True;
          if not Appended:
            Rtn.append(dg)
          if IsDebugging(TestGraph2):
            print(STSP("  $u -> $v ? $A vs $B", u=u,v=v, A=A,B=B));
            ## print("  edges", dg.E)
            prt(dg.A, h='Orig');
            prt(fg, h='FG');
            prt(scc.Info, h='SCC Info')
            prt(scc.CM, h='SCC CM')
          break;
      if Break:
        break
  return Rtn

#DebugPush(TestGraph)
N = 12
Cases = []
for E in range(N//2, (N//3)*N):
  Cases += TestGraph2(N, E, 10)

for dg in Cases:
  scc = SCC(dg)
  CC = DGConnected(dg)
  print(STSP('{ Graph of |$V|,|$E| took $IT', 
             V=len(dg.V), E=len(dg.E), IT=scc.IT))
  prt(dg.A, h='Orig');
  prt(scc.Info, h='DGC R')
  prt(scc.dfs1.AllLoops, h='Loops')
  prt(scc.dfs1.AllPaths, h='Paths')
  print('}')
