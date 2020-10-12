from MyStuff3 import *

class FragmentError(Exception):
  def __init__(s, *args, **kwargs):
    s.msg = [  str(mm) for mm in args ] +  [ (str(k), ":", str(v) )   for k, v in kwargs.items() ]

  def __str__(s):
    return " ".join(s.msg)

class EmptyFragmentError(FragmentError):
  def __init__(s, *args, **kwargs):
    super().__init__('EmptyFragment', *args, **kwargs)

class IllegalFragmentError(FragmentError):
  def __init__(s, *args, **kwargs):
    super().__init__('IllegalFragment', *args, **kwargs)


class FragmentInfo(DebugHelper):
  LegalKind = set(['BASIC', 'LSBStream', 'MSBStream'])
  DefaultKind = 'BASIC'
  DefaultStreamKind = 'LSBStream'

  def __init__(s, *args, **kwargs):
    s.kind = FragmentInfo.DefaultKind
    s.offset = 0
    s.length = 0

    if len(args) == 2:
      s.offset = args[0]
      s.length = args[1]
    elif len(args) == 3:
      s.offset = args[0]
      s.length = args[1]
      s.kind =  args[2]

    if 'kind' in kwargs:
      s.kind = kwargs['kind']
    if 'offset' in kwargs:
      s.offset = kwargs['offset']
    if 'length' in kwargs:
      s.length = kwargs['length']
    ##### PAY ATTENTION!
    s.payload = None
    # payload should be the raw byte sequence that starts at offset for length 'units'
    # You should shift the payload so that unwanted bits are not around!
    ####
    if s.kind not in FragmentInfo.LegalKind:
      raise FragmentError('illegal FragmentInfo kind')
    if (not isinstance(s.offset, int)) or (not isinstance(s.length, int)):
      raise FragmentError('offset and field must be integers')
    if s.offset < 0 or s.length < 0:
      raise FragmentError('offset and field must be >= 0')

  def __str__(s):
    return STSP('($offset,$length,$kind)',
                kind=s.kind, offset=s.offset, length=s.length)
  @property
  def byteStart(s):
    if s.kind == 'BASIC':
      return s.offset
    else:
      return s.offset>>3

  @property
  def byteLength(s):
    if s.kind == 'BASIC':
      return s.length
    else:
      return (s.length+7)>>3

  @property
  def byteEnd(s):
    if s.kind == 'BASIC':
      return s.offset + s.length
    else:
      return (s.offset>>3) + ((s.length+7)>>3)

  @property
  def bitStart(s):
    if s.kind == 'BASIC':
      return s.offset<<3
    else:
      return s.offset
  @property
  def bitLength(s):
    if s.kind == 'BASIC':
      return s.length<<3
    else:
      return s.length
  @property
  def bitEnd(s):
    if s.kind == 'BASIC':
      return (s.offset<<3) + (s.length<<3)
    else:
      return (s.offset + s.length)
  @property
  def byteRange(s):
    return (s.byteStart, s.byteEnd)
  @property
  def bitRange(s):
    return (s.bitStart, s.bitEnd)


  @staticmethod
  def comparableRange(A, B):
    if A.kind == 'BASIC' and B.kind == 'BASIC':
      return (A.byteRange, B.byteRange, 'BASIC')
    else:
      return (A.bitRange, B.bitRange, FragmentInfo.DefaultStreamKind)

  def equals(s, rh):
    ((AStart,AEnd), (BStart,BEnd), k) = FragmentInfo.comparableRange(s, RH)
    return AStart == BStart and AEnd == BEnd

  def __and__(lh, rh):
    ((AStart,AEnd), (BStart,BEnd), k) = FragmentInfo.comparableRange(lh, rh)
    x = max(AStart, BStart)
    y = min(AEnd, BEnd)
    if x < y:
      return FragmentInfo(x, y, k)
    raise EmptyFragmentError((AStart,AEnd), (BStart,BEnd), k)

  def __or__(lh, rh):
    ((AStart,AEnd), (BStart,BEnd), k) = FragmentInfo.comparableRange(lh, rh)
    x = min(AStart, BStart)
    y = max(AEnd, BEnd)
    if x < y:
      return FragmentInfo(x, y-x, k)
    raise EmptyFragmentError((AStart,AEnd), (BStart,BEnd), k)

  # unfortunately, A - B and A ^ B 
  # can result in multiple fragments, so we can't
  # use operator overloading.
  @staticmethod
  def subtract1(lh, rh):
    """
        // 0--8  3---12 --> 0--3    x:0 y:3  w:8
        // 0--8  10--12 --> 10--12  x:0 y:10 w:8 (illegal)
        // 0--12 0--4  --> 0--0     x:0 y:0  w:4 (illegal)
    """
    ((AStart,AEnd), (BStart,BEnd), k) = FragmentInfo.comparableRange(lh, rh)
    x = min(AStart, BStart)
    y = max(AStart, BStart)
    w = min(AEnd, BEnd)
    if y < w and x < y:
      return FragmentInfo(x, y-x, k)
    raise IllegalFragmentError((AStart,AEnd), (BStart,BEnd), k)
  @staticmethod
  def subtract2(lh, rh):
    """
        // 0--8  3---12 --> 8--12  x:8  y:12  
        // 0--8  10--12 --> 10--12 x:10 y:12  (illegal)
        // 0--12 0--4  -->  4--12  x:4  y:12 
    """
    ((AStart,AEnd), (BStart,BEnd), k) = FragmentInfo.comparableRange(lh, rh)
    x = min(AEnd, BEnd)
    y = max(AEnd, BEnd)
    if x < y:
      return FragmentInfo(x, y-x, k)
    raise IllegalFragmentError((AStart,AEnd), (BStart,BEnd), k)

  def intToBinary(num):
    #print("Original number: ", num, "\nBinary number: ", '{0:08b}'.format(num))
    return ('{0:08b}'.format(num))

  def easilyReadBinary(num, chunk_size):
    sn = str(num)
    chunks = []
    bits = []
    for byte in range(0, len(sn), chunk_size):
      print(sn[byte:byte+chunk_size])
      chunks.append(sn[byte:byte+chunk_size])
    #create a dict where key is chunk val is digits
    #for i in chunks:
      #val = [int(d) for d in chunks[i]]
    return chunks


  def bitExtraction(num_bits, bit_offset, chunk_size, bits):
    #base case -- start from the first bit and stay within that chunk *ALWAYS STAY IN CHUNK FOR NOW*
    # --> end_index, j
    # --> bit_offset, i

    #need a bytearray starting from offset and going until end_bit
    #ending index of bit to extract
    end_bit = num_bits + bit_offset
    #mask = bytearray('1'*(num_bits), 'utf-8').decode()

    #bin(int(bits)) << bit_offset


    


  if __name__ == "__main__":
    ex1 = intToBinary(2**(63)-12345)
    ex2 = intToBinary(2**(40)-12345)
    ex3 = intToBinary(2**8-2)
    
    easilyReadBinary(ex3, 8)
    #print("BIT EXTRACTION BASIC")
    bitExtraction(3, 3, 8, ex3)

    #printing binary values 1 - 256
    #for i in range(0, 256):
      #print("Base 2:", i, int('{0:08b}'.format(i)))

    x=bytearray('1'*5, 'utf-8').decode()
    #print("BYTE", x)
    #print(type(x))
    a = intToBinary(0xdeadbeefcafe)
    print(a, len(a))
    





