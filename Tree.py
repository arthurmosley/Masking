
from MyStuff3 import *



class Tree(DebugHelper):
  """
  Always acts like a dictionary of kid names to kids
  """
  def __init__(s, item, kids={}):
    InitDbg(s)
    s.item = item
    s.kids = kids
    # Ordered list of names for kids
    # Internally, the map form is always used, because its a superset.
    # So even if the kids are passed in as a list, they are always
    # transformed into dicts
    s.kid_names = []
    if isinstance(kids, list) or isinstance(kids, tuple):
      if len(kids)>0 and (isinstance(kids[0], list) or isinstance(kids[0], tuple)):
        ## these are dict-capable records.
        ## Use [ [ kn, kid ] ... ] for when your kid names do not
        ## sort in  the default way
        s.kid_names = [ k for k,v in kids ]
        s.kids = dict(kids)
      else:
        s.kid_names = [ i for i,v in enumerate(kids) ]
        s.kids = dict([ [i, k] for i, k in enumerate(kids) ])
    elif isinstance(kids, dict):
      s.kid_names = [ k for k in kids ]

  def __getitem__(s, k):
    return s.kids[k]

  def __setitem__(s, k, v):
    if k not in s.kid_names:
      s.kid_names.append(k)
    s.kids[k] = v

  def __delitem__(s, k):
    s.DBG2(s.__delitem__, "removing k",k, s.kid_names)
    s.kid_names.remove(k)
    del s.kids[k]

  def __contains__(s, k):
    return k in s.kids

  def __len__(s):
    return len(s.kids)

  def __iter__(s):
    """ preserves the ordering of the kids
    """
    return s.kid_names.__iter__()

  def iteritems(s):
    return [(kn,s.kids[kn]) for kn in s.kid_names ]

  def __call__(s, *args, **kwargs):
    return s.item(*args, **kwargs)

  def to_string(s, l=0):
    def SPC(l):
      return "  "*l
    x=''
    if len(s.kids) > 0:
      x = STSP("""${S}[ $item \n""",S=SPC(l), item=str(s.item))
      for kn in s.kid_names:
        x = x + STSP("""${S1}(kid:$kn\n${kid}${S1})${S1}\n""",kn=kn,
                     S1=SPC(l+1),S2=SPC(l+2),kid=s.kids[kn].to_string(l+2))
      x = x + STSP("""$S]\n""",S=SPC(l))
    else:
      x = STSP("""$S0[ $item ]""",S0=SPC(l), item=str(s.item))
    return x

  def __str__(s):
    return s.to_string()


def PostOrder(t, op, l=0):
  rtn = []
  for kn in t:
    P = PostOrder(t[kn], op)
    if P != None:
      rtn.append([kn,P])
  return op(t, dict(rtn))


class NRPost(DebugHelper):

  @staticmethod
  def STK(t):
    return [ t, 0, dict([ [kn, None] for kn in t  ]) ]
  def __init__(s):
    InitDbg(s)
  def __call__(s, t, op):
    s.S = [[ None, 0, [] ], STK(t) ]

def CPTREE2(T, m={}, op=CP):
  if isinstance(T, Tree):
    kids = dict([[kn, CPTREE2(T[kn],m)] for kn in T.kid_names ])
    rtn = Tree(op(T.item),  kids)
    m[T] = rtn
    return rtn

