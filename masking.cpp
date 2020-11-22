#include <iostream>
#include <bitset>
#include <string>
#include <stdlib.h>
#include <bits/c++config.h>

template <class T>
std::string getBinary(T num)
{
	const int nBits = sizeof(T)*8;
	unsigned char s[nBits + 1];
	for (unsigned int i = 0; i < nBits; ++i)
	{
		s[i] = '0' + ((num >> i) & 1);
	}
	s[nBits] = 0;
	return std::string((const char*) s);
}

int getNumeric(std::string binary)
{
  int convert = std::stoi(binary, nullptr, 2);
  return convert;
}

std::string fillBinary(std::string bin, int size)
{
	if(bin.length() >= size) return bin;
	int numFill = size-bin.length();
	std::string filledBinary = "";
	while(bin.length() < numFill)
	{
		filledBinary += "0";
	}
	filledBinary += bin;
	return filledBinary;
}

template <class T>
void printBinary(T num1, T num2)
{
	std::cout << "a =" << num1 << std::endl;
	std::cout << "b =" << num2 << std::endl;
	std::cout << "---------------------------------------" << std::endl;
	std::cout << "Binary output of a" << " is: " << getBinary(num1) << std::endl;
	std::cout << "Binary output of b" << " is: " << getBinary(num2) << std::endl;
	std::cout << "---------------------------------------" << std::endl;
}

template <class T>
void printBitManipulation(T num1, T num2)
{
	std::cout << "a | b                : " << getBinary(num1 | num2) << ":   " << (num1 | num2)  << std::endl;
	std::cout << "a & b                : " << getBinary(num1 & num2) << ":   " << (num1 & num2)  << std::endl;
	std::cout << "a ^ b                : " << getBinary(num1 ^ num2) << ":   " << (num1 ^ num2)  << std::endl;
	std::cout << "~(a | b)             : " << getBinary(~(num1 | num2)) << ":   " << ~(num1 | num2)  << std::endl;
	std::cout << "~(a & b)             : " << getBinary(~(num1 & num2)) << ":   " << ~(num1 & num2)  << std::endl;
	std::cout << "~(a ^ b)             : " << getBinary(~(num1 ^ num2)) << ":   " << ~(num1 ^ num2)  << std::endl;
	std::cout << "---------------------------------------" << std::endl;
}

// Creating a bit mask for a specific offset and length.
unsigned long long bitMask(unsigned int offset, unsigned int length)
{
	//All ones.
	unsigned long long mask = ~(0);
	//
	mask = ~((mask) >> length) >> offset;
	return mask;
}

// start at dest[0]
template <class T>
void bytesInQuestion(T* dest, const T* src, unsigned offset, unsigned length)
{
  /*** Useful information for accessing info to pull out the fragment ***/
  const unsigned wordSizeBits = sizeof(T)*8;
  //std::cout << "WORD SIZE " << wordSizeBits << std::endl;
  unsigned startChunk = offset / wordSizeBits;
  unsigned startBitPos = offset % wordSizeBits;
  unsigned endBitPos = (offset + length) % wordSizeBits;
  unsigned endChunk = (offset + length) / wordSizeBits;
  //std::cout << "END CHUNK " << endChunk << std::endl;

  // Mask needs to be sizeof(T) ~0 but bit shift the current chunk. clear left clear right

  for ( unsigned i = 0; i <= (endChunk - startChunk); ++i )
  {
    dest[i] = src[startChunk + i];
  }
	// getting a mask for whatever starting bits aren't necessary. Followed by executing the mask.
  T firstChunkMask = (~T(0)) << startBitPos;
  dest[0] &= firstChunkMask;
	// getting a mask for whatever ending bits aren't necessary. Followed by executing the mask.
  T lastChunkMask = (~T(0)) >> (wordSizeBits - endBitPos);
  dest[endChunk - startChunk] &= lastChunkMask;
  if (startChunk == endChunk) {
    dest[0] >>= startBitPos;
  } else {
	
  }
  /*
   in separate routine
   test with multiple unsigned char .. 16 bytes. Binary sequence. Call routine... print out what destination is after routine.
  */
}

int main()
{
	//unsigned long long un = bytesInQuestion(0xFAFA, 2, 4);
	//std::cout << "raw number bytes in question: " << un << std::endl;
	//std::string uncleanFragment = getBinary(un);
	//std::cout << "uncleaned bytes in question: " << uncleanFragment << std::endl;
	// Basic output.
  //printBinary(12, 10);
  //printBitManipulation(12, 10);
	int dest = 0;
	int* destination = &dest;
	const int source1 = 0xF1EA;
	const int* src = &source1;
  std::cout << "SOURCE 1 VALUE: " << getBinary(*src) << std::endl;
  // BASE test where no offset and in the same chunk.
	bytesInQuestion(src, destination, 0, 6);
  std::cout << "DESTINATION VALUE 1: " << getBinary(*destination) << std::endl;
  std::cout << "DESTINATION VALUE 1: " << *destination << std::endl;
  // Test where offset and in the same chunk.
  bytesInQuestion(src, destination, 2, 6);
  std::cout << "DESTINATION VALUE 2: " << getBinary(*destination) << std::endl;
	std::cout << "DESTINATION VALUE 2: " << *destination << std::endl;
	return 0;
}
