#include <iostream>
#include <bitset>
#include <string>
#include <stdlib.h>
#include <bits/c++config.h>

template <class T>
std::string getBinary(T num)
{
	std::string binary = std::bitset<64> (num).to_string();
	//std::bitset<64> binaryEquivalent num;
	return binary;
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
template <class T>
T bitMask(int offset, int length)
{
	//All ones.
	unsigned long long mask = ~(0);
	//
	mask = ~((mask) >> length) >> offset;
	return mask;
}


// Convert input to binary --> 00 001111 000011 11 00001111
// 				Want bits OFFSET = 2 LENGTH = 11
//        OFFSET (2) % 8 = 2 (go back 2 bits) ... LENGTH (11) % 8 = 3 + 2
template <class T>
T bytesInQuestion(T fragment, int offset, int length)
{
	unsigned long long mask = ~(0);
	mask = ~((mask) << length) << offset;
	//std::cout << "TEST1: " << getBinary(fragment) << std::endl;
	//std::cout << "TEST2: " << getBinary(mask) << std::endl;
	T bytesInQ = fragment &  mask;

	return bytesInQ;
}

// Function that isolates the fragment wanted.
template <class T>
T cleanFragment(T stream, int offset, int length)
{

	return stream;
}


// running tally of the bit position.
// as printing out each bit, print out shift value in decimal.
// if % 7 and number of bits is 30. ABORT for now.
// write the routine to print out chunks that are more than one variable long.
		// 8 bytes MAX 32 bit architecture.. PRINT OUT BIT POSITIONS.
		// little endian architecture.
int main()
{
	const unsigned int a = 7;
	const unsigned int b = ~(0);
	printBinary(a, b);

	const unsigned int mask1 = 0xF800;
	const unsigned int mask2 = 0x07E0;
	const unsigned int mask3 = 0x001F;
	unsigned int test = 0x7BEF;
	unsigned int out1 = (test & mask1) >> 11;
	unsigned int out2 = (test & mask2) >> 5;
	unsigned int out3 = (test & mask3);
	std::cout << "out1 = " << out1 << std::endl;
	std::cout << "out2 = " << out2 << std::endl;
	std::cout << "out3 = " << out3 << std::endl << std::endl;
	//std::cout << "Binary of hex: " << getBinary(0xFF) << std::endl;

	//Example for bit shifting.
	printBinary(test, mask1);
	printBitManipulation(test, mask1);
	printBinary(test, mask2);
	printBitManipulation(test, mask2);
	printBinary(test, mask3);
	printBitManipulation(test, mask3);

	// Creating a bitmask of 4 bits long.
	unsigned long long allOnes = ~(0);
	allOnes = ~((allOnes) >> 4) >> 10 ;
	std::cout << "BITMASK 4 bits long: " << getBinary(allOnes) << std::endl;

	unsigned long long un = bytesInQuestion(0xFAFA, 2, 4);
	std::cout << "raw number bytes in question: " << un << std::endl;
	std::string uncleanFragment = getBinary(un);
	std::cout << "uncleaned bytes in question: " << uncleanFragment << std::endl;
	// Basic output.
  //printBinary(12, 10);
  //printBitManipulation(12, 10);



	return 0;
}
