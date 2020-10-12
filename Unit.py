from Tree import *
from FragmentInfo import *
print(__name__, sys.argv)
if __name__ == "__main__":
  x = Tree(1, [ Tree(2, [ Tree(3), Tree(4) ] ),
                Tree(5, [ Tree(6), Tree(7) ] ) ])

  # the tree above looks like this:
  #
  #            1
  #      +-----+------+
  #      |            |
  #      2            5  
  #      +            +
  #  +---+--+      +--+-----+
  #  |      |      |        |
  #  3      4      6        7 
  

  m = {}
  y = CPTREE2(x, m)
  print("now we print the post order traversal of the tree")
  PostOrder(x, lambda a, r: prt(a.item))
  print("now we print the default string representation of the tree")
  print(str(y))
  print("----------------")
  print(" now we delete the SECOND child of t")
  ## Debug output specifically the __delitem__ operator ONLY
  #X DebugPush(Tree, x.__delitem__)
  ## uncomment the line marked #X to see Tree:__delitem__ work
  del x[1]

  PostOrder(x, lambda a, r: prt(a.item))


  # the different ways to create FragmentInfos
  fl=  [ FragmentInfo(0, 10), FragmentInfo(10, 20, FragmentInfo.DefaultStreamKind),
         FragmentInfo(32, 48, kind='MSBStream'),
  ]
  for f in fl:
    print(STSP("fragment $ff has byteRange $a and bitRange $b",
               ff=f, a=f.byteRange, b=f.bitRange))

  fLH = [ FragmentInfo(8, 7) ]
  fRH = [ FragmentInfo(1,3), FragmentInfo(6, 2), FragmentInfo(6, 4), FragmentInfo(6,10),
          FragmentInfo(8,7), FragmentInfo(8, 12), FragmentInfo(15,3), FragmentInfo(16,4) ]


  for A in fLH:
    for B in fRH:
      try:
        C = A & B
        print(STSP('$A & $B = $C', A=A, B=B, C=C))
      except EmptyFragmentError as E:
        print(STSP('$A & $B broke.. $E ', A=A, B=B, E=E))
      try:
        C = A | B
        print(STSP('$A | $B = $C', A=A, B=B, C=C))
      except EmptyFragmentError as E:
        print(STSP('$A & $B broke.. $e', A=A, B=B, E=E))
      try:
        C = FragmentInfo.subtract1(A, B)
        print(STSP('subtract1($A, $B) = $C', A=A, B=B, C=C))
      except FragmentError as E:
        print(STSP('subtract1($A - $B) broke.. $E', A=A, B=B, E=E))
      try:
        D = FragmentInfo.subtract2(A, B)
        print(STSP('subtract2($A, $B) = $D', A=A, B=B, D=D))
      except FragmentError as E:
        print(STSP('subtract2($A - $B) broke.. $E', A=A, B=B, E=E))
