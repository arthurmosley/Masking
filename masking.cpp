#include <iostream>
#include <bitset>
#include <string>
#include <stdlib.h>

template <class T>
std::string getBinary(T num)
{
	std::string binary = std::bitset<32> (num).to_string();
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
	unsigned int allOnes = ~(0);
	allOnes = ~((allOnes) << 4);
	std::cout << "BITMASK 4 bits long: " << getBinary(allOnes) << std::endl; 
	

	// Basic output.
  //printBinary(12, 10);
  //printBitManipulation(12, 10);



	return 0;
}