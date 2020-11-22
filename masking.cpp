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

template <class T>
T reverseBits(T num)
{
	unsigned int numBits = sizeof(num) * 8;
	unsigned int reverse = 0, temp;
	for (unsigned i = 0; i < numBits; ++i)
	{
		temp = (num & (1 << i));
		if(temp)
		{
			reverse |= (1 << ((numBits - 1) - i));
		}
	}
	return reverse;
}

// start at dest[0]
template <class T>
void bytesInQuestion(T* dest, const T* src, unsigned offset, unsigned length)
{
  /*** Useful information for accessing info to pull out the fragment ***/
  const unsigned wordSizeBits = sizeof(T)*8;
  unsigned startChunk = offset / wordSizeBits;
  unsigned startBitPos = offset % wordSizeBits;
  unsigned endBitPos = (offset + length) % wordSizeBits;
  unsigned endChunk = (offset + length) / wordSizeBits;


  // Mask needs to be sizeof(T) ~0 but bit shift the current chunk. clear left clear right

  for ( unsigned i = 0; i <= (endChunk - startChunk); ++i )
  {
    dest[i] = src[startChunk + i]; // copying chunks over.
		//std::cout << src[startChunk + i] << " " << getBinary(src[startChunk + i]) << std::endl;
  }
  T firstChunkMask = (~T(0)) << startBitPos; // create beginning mask.
  dest[0] &= firstChunkMask;
  T lastChunkMask = unsigned(~T(0)) >> (wordSizeBits - endBitPos); // create end mask, type issue must be casted.
  dest[endChunk - startChunk] &= lastChunkMask;
  if (startChunk == endChunk) {
    dest[0] >>= startBitPos; // flushes out unwanted bits.
  } else {
		// Handle when endChunk = startChunk + 1 && endChunk > startChunk + 1
		/* endChunk = startChunk + 1 */
		// Must move bits from end chunk to startchunk, then remove them from end chunk.
		dest[0] >>= startBitPos;
		T tempMask = ~(T(0)) << startBitPos;
		tempMask = ~tempMask;
		T firstNBits = dest[1] & tempMask;
		firstNBits = reverseBits(firstNBits);
		dest[0] = (dest[0]) | firstNBits;
		dest[1] >>= startBitPos;
  }
  /*
   in separate routine
   test with multiple unsigned char .. 16 bytes. Binary sequence. Call routine... print out what destination is after routine.

  */
}

int main()
{
	int destination[4] = { 0 };
	int* dest = destination;
	//const int source1[4] = {0xFEA1, 0xABCD, 0x8402, 0x570F};
	int x = 0xABCD;
	const int source1[4] = {0x7FFFFFFF, 0x7ABCD747, 0xFFFF, 0xFFFF};
	const int* src = source1;

  // BASE test where no offset and in the same chunk.
	bytesInQuestion(dest, src, 3, 42);

	//std::cout << "SOURCE 1 VALUES: ";
	for( int i = 0; i < 4; ++i )
	{
  	std::cout << getBinary(src[i]) << " ";
	}
	std::cout << '\n';
	//std::cout << "DESTINATION VALUES: ";
	for ( int i = 0; i < 4; ++i )
	{
		std::cout << getBinary(dest[i]) << " ";
	}
	std::cout << '\n';
	/*
  // Test where offset and in the same chunk.
  bytesInQuestion(dest, src, 2, 6);
  std::cout << "DESTINATION VALUE 2: " << getBinary(*dest) << std::endl;
	std::cout << "DESTINATION VALUE 2: " << *dest << std::endl;*/



	//std::cout << getBinary(0xFEA1) << std::endl;
	//std::cout << getBinary(0xABCD) << std::endl;
	return 0;
}
