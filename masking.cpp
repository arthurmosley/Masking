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

template <class T>
void bytesInQuestion(const T* src, T* dest, unsigned int offset, unsigned int length)
{
  /*** Useful information for accessing info to pull out the fragment ***/
  const unsigned wordSizeBits = sizeof(T)*8;
  //std::cout << "WORD SIZE " << wordSizeBits << std::endl;
  unsigned int startChunk = offset / wordSizeBits;
  unsigned int startBitPos = offset % wordSizeBits;
  unsigned int endBitPos = (offset + length) % wordSizeBits;
  unsigned int endChunk = (offset + length) / wordSizeBits;
  //std::cout << "END CHUNK " << endChunk << std::endl;

  /***

  Okay... these are the bits presented (0101 0111 1000 1111 0000 0000 0000 0000)
  Wanna get base case of BytesInQestion(, , 0, 6)... EXPECTED output = (0101 01) IN dest

  ***/
  const unsigned int baseEx = 0xF1EA;
  std::string baseBin = getBinary(baseEx);
//  std::cout << "src INTEGER: " << baseEx << "\nsrc BINARY: " << baseBin << std::endl;

  // Mask needs to be sizeof(T) ~0 but bit shift the current chunk. clear left clear right

  /*** FIRST CHUNK ***/
  unsigned long long firstChunkMask = ~(0);
  firstChunkMask = ~((firstChunkMask) << wordSizeBits);
  //std::cout << "FIRST MASK " << getBinary(firstChunkMask) << std::endl;
  T temp = (*src >> startBitPos) & firstChunkMask ;
  std::string base = getBinary(temp);
  //std::cout << "src1 INTEGER: " << temp << "\nsrc BINARY: " << base << std::endl;
  *dest += temp;

  if (startChunk != endChunk)
  {
    // Grabbing the first chunk from source. -- All this does is remove 'n' LSB's (n can be 0)
    int currentChunk = startChunk;
    while(currentChunk < endChunk) // Not sure if <= or < yet
    {
      // Need to fill up "new" first chunk and continue to fill in subsequent chunks until the end.
      if (startBitPos != 0)
      {
         // Then grab "startBitPos" bits from the next chunk.
      }
      currentChunk++;
    }
  }
  else
  {
    // Start and end are in the same chunk.
    unsigned int endChunkMask = ~(0);
    std::cout << "END BIT: " << endBitPos << " OFFSET: " << offset <<  std::endl;
    endChunkMask = (endChunkMask) >> (wordSizeBits - length); // (wordsizeBits - endBitPos)
    //std::cout << "END CHUNK MASK " << getBinary(endChunkMask) << std::endl;
    temp &= endChunkMask;
    //std::cout << "binary temp " << getBinary(temp) << std::endl;
    *dest = temp; // How does "adding" to destination work.
  }
}

// running tally of the bit position.
// as printing out each bit, print out shift value in decimal.
// if % 7 and number of bits is 30. ABORT for now.
// write the routine to print out chunks that are more than one variable long.
		// 8 bytes MAX 32 bit architecture.. PRINT OUT BIT POSITIONS.
		// little endian architecture.
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
	bytesInQuestion(src, destination, 0, 45);
  std::cout << "DESTINATION VALUE 1: " << getBinary(*destination) << std::endl;
  std::cout << "DESTINATION VALUE 1: " << *destination << std::endl;
  // Test where offset and in the same chunk.
  bytesInQuestion(src, destination, 2, 6);
  std::cout << "DESTINATION VALUE 2: " << getBinary(*destination) << std::endl;
	std::cout << "DESTINATION VALUE 2: " << *destination << std::endl;
	return 0;
}
