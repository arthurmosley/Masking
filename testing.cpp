// Convert input to binary --> 00 001111 000011 11 00001111
// 				Want bits OFFSET = 2 LENGTH = 11
//        OFFSET (2) % 8 = 2 (go back 2 bits) ... LENGTH (11) % 8 = 3 + 2
template <class T>
void bytesInQuestion(const T* src, T* dest, unsigned int offset, unsigned int length)
{
	unsigned long long mask = ~(0);
	mask = ~((mask) << length) << offset;
	//std::cout << "TEST1: " << getBinary(fragment) << std::endl;
	//std::cout << "TEST2: " << getBinary(mask) << std::endl;
	//T bytesInQ = src &  mask;

	//First part of the fragment (1st byte)
	int whichByte = int(offset / 8);
	// startPos information valuable for cleaning the first byte in the buffer.
	int startPos = offset % 8;
	/*** SOURCED FROM geeksforgeeks.org ***/
	const T sourceValue = *src;
	std::cout << "BINARY for SRC: " << getBinary(sourceValue) << std::endl;
	// QUESTION 1: is this okay to do? -- need to check if length is less than number of bits in T.
	// Need to modulo and divide by the number of bits in T.
	// Reevaluate how I did this.
	T firstFrag = (((1 << length) - 1) & (sourceValue >> (offset - 1)));
	std::string t1 = getBinary(firstFrag);
	std::cout << "testing " << "int val:" << firstFrag << " " << t1 << std::endl;
	// adding the first byte of the input given offset and length...
	// QUESTION 2: Should I create a dynamic array where I append each bit in order to save the entire fragment desired?
	// How do I "append" values to the destination?
	std::string entireFragment = "";
	std::string tempChunk = getBinary(firstFrag);
	//adding the current chunk to the fragment to then be held by dest.
	entireFragment += tempChunk;
  std::cout << "entire fragment binary " << entireFragment << std::endl;
  //std::cout << "entire fragment integer " << currentFrag << std::endl;
  int counter = 8 - startPos;
  // How do you find out where the last bit is.
  //  go until the length + offset - how many bits are in the last chunk.
  int endByte = int((offset + length) / 8);
  int endPos = (length) % 8;
  //Goes until hitting the last bit.
  int goUntil = length - endPos;
  T middleFrag = (((1 << goUntil) - 1) & (sourceValue >> (offset + counter - 1)));
  tempChunk = getBinary(middleFrag);
  entireFragment += tempChunk;

	*dest = firstFrag;
}
