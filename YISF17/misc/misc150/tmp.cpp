#include <iostream>
#include <fstream>

//  base_value
template <typename _ttype, _ttype _tvalue>
struct base_value
{
	typedef typename _ttype type;

	static _ttype const value = _tvalue;
};

//  bool
template <bool _tvalue>
struct bool_value : base_value<bool, _tvalue> {};
using bool_default = bool_value<false>;

//  char
template <char _tvalue>
struct char_value : base_value<char, _tvalue> {};
using char_default = char_value<0>;

//  int
template <int _tvalue>
struct int_value : base_value<int, _tvalue> {};
using int_default = int_value<0>;

//  unsigned char
template <unsigned char _tvalue>
struct unsigned_char_value : base_value<unsigned char, _tvalue> {};
using unsigned_char_default = unsigned_char_value<0>;

//  unsigned int
template <unsigned int _tvalue>
struct unsigned_int_value : base_value<unsigned int, _tvalue> {};
using unsigned_int_default = unsigned_int_value<0>;

///
///
///
template <typename _tvalue_one, typename _tvalue_two>
struct operator_01
{
	static base_value<decltype(_tvalue_one::value + _tvalue_two::value),
		_tvalue_one::value + _tvalue_two::value> const result;
};

///
///
///
template <typename _tvalue_one, typename _tvalue_two>
struct operator_02
{
	static base_value<decltype(_tvalue_one::value - _tvalue_two::value),
		_tvalue_one::value - _tvalue_two::value> const result;
};

///
///
///
template <typename _tvalue_one, typename _tvalue_two>
struct operator_03
{
	static base_value<decltype(_tvalue_one::value * _tvalue_two::value),
		_tvalue_one::value * _tvalue_two::value> const result;
};

///
///
///
template <typename _tvalue_one, typename _tvalue_two>
struct operator_04
{
	static base_value<decltype(_tvalue_one::value ^ _tvalue_two::value),
		_tvalue_one::value ^ _tvalue_two::value> const result;
};

///
///
///
template <typename _tvalue_one, typename _tvalue_two>
struct operator_05
{
	static base_value<decltype(_tvalue_one::value % _tvalue_two::value),
		_tvalue_one::value % _tvalue_two::value> const result;
};

///
///
///
template <typename _tvalue_one, typename _tvalue_two>
struct operator_06
{
	static base_value<bool,
		_tvalue_one::value || _tvalue_two::value> const result;
};

///
///
///
template <typename _tvalue_one, typename _tvalue_two>
struct operator_07
{
	static base_value<bool,
		_tvalue_one::value && _tvalue_two::value> const result;
};

///
///
///
template <typename _tvalue>
struct operator_08
{
	static base_value<bool,
		!_tvalue::value> const result;
};

///
///
///
template <typename _tvalue_one, typename _tvalue_two>
struct operator_09
{
	static base_value<bool,
		_tvalue_one::value == _tvalue_two::value> const result;
};

///
///
///
template <typename _ttype>
struct operator_10
{
	static base_value<bool, false> const result;
};

///
///
///
template <>
struct operator_10<bool_default>
{
	static base_value<bool, true> const result;
};

///
///
///
template <>
struct operator_10<char_default>
{
	static base_value<bool, true> const result;
};

///
///
///
template <>
struct operator_10<int_default>
{
	static base_value<bool, true> const result;
};

///
///
///
template <>
struct operator_10<unsigned_char_default>
{
	static base_value<bool, true> const result;
};

///
///
///
template <>
struct operator_10<unsigned_int_default>
{
	static base_value<bool, true> const result;
};

///
///
///
template <typename _ttype, _ttype _tvalue>
struct operator_11
{
	static typename _ttype const value = _tvalue + operator_11<typename _ttype, _tvalue - 1>::value;
};

///
///
///
template <>
struct operator_11<bool, bool_default::value>
{
	static bool const value = bool_default::value;
};

///
///
///
template <>
struct operator_11<char, char_default::value>
{
	static char const value = char_default::value;
};

///
///
///
template <>
struct operator_11<int, int_default::value>
{
	static int const value = int_default::value;
};

///
///
///
template <>
struct operator_11<unsigned char, unsigned_char_default::value>
{
	static unsigned char const value = unsigned_char_default::value;
};

///
///
///
template <>
struct operator_11<unsigned int, unsigned_int_default::value>
{
	static unsigned int const value = unsigned_int_default::value;
};

///
///
///
template <typename _ttype, _ttype _tvalue>
struct operator_12
{
	static typename _ttype const value = (_tvalue & 0x01) + operator_12<typename _ttype, _tvalue - 1>::value;
};

///
///
///
template <>
struct operator_12<bool, bool_default::value>
{
	static bool const value = bool_default::value;
};

///
///
///
template <>
struct operator_12<char, char_default::value>
{
	static char const value = char_default::value;
};

///
///
///
template <>
struct operator_12<int, int_default::value>
{
	static int const value = int_default::value;
};

///
///
///
template <>
struct operator_12<unsigned char, unsigned_char_default::value>
{
	static unsigned char const value = unsigned_char_default::value;
};

///
///
///
template <>
struct operator_12<unsigned int, unsigned_int_default::value>
{
	static unsigned int const value = unsigned_int_default::value;
};

int main()
{
	unsigned char encoded_flag[20] = { 0 };

	encoded_flag[0] = operator_01<char_value<'Y'>,
		unsigned_char_value<0x10>>::result.value;

	encoded_flag[1] = operator_01<char_value<'I'>,
		unsigned_char_value<0x10>>::result.value;

	encoded_flag[2] = operator_01<char_value<'S'>,
		unsigned_char_value<0x10>>::result.value;

	encoded_flag[3] = operator_01<char_value<'F'>,
		unsigned_char_value<0x10>>::result.value;

	encoded_flag[4] = operator_01<char_value<'{'>,
		unsigned_char_value<0x10>>::result.value;

	encoded_flag[5] = operator_02<char_value<'v'>,
		unsigned_char_value<0x20>>::result.value;

	encoded_flag[6] = operator_02<char_value<'3'>,
		unsigned_char_value<0x20>>::result.value;

	encoded_flag[7] = operator_02<char_value<'r'>,
		unsigned_char_value<0x20>>::result.value;

	encoded_flag[8] = operator_02<char_value<'Y'>,
		unsigned_char_value<0x20>>::result.value;

	encoded_flag[9] = operator_02<char_value<'_'>,
		unsigned_char_value<0x20>>::result.value;

	encoded_flag[10] = operator_03<char_value<'C'>,
		unsigned_char_value<0x02>>::result.value;

	encoded_flag[11] = operator_03<char_value<'o'>,
		unsigned_char_value<0x02>>::result.value;

	encoded_flag[12] = operator_03<char_value<'N'>,
		unsigned_char_value<0x02>>::result.value;

	encoded_flag[13] = operator_03<char_value<'F'>,
		unsigned_char_value<0x02>>::result.value;

	encoded_flag[14] = operator_03<char_value<'u'>,
		unsigned_char_value<0x02>>::result.value;

	encoded_flag[15] = operator_04<char_value<'5'>,
		unsigned_char_value<0xaa>>::result.value;

	encoded_flag[16] = operator_04<char_value<'i'>,
		unsigned_char_value<0xaa>>::result.value;

	encoded_flag[17] = operator_04<char_value<'n'>,
		unsigned_char_value<0xaa>>::result.value;

	encoded_flag[18] = operator_04<char_value<'G'>,
		unsigned_char_value<0xaa>>::result.value;

	encoded_flag[19] = operator_04<char_value<'}'>,
		unsigned_char_value<0xaa>>::result.value;


	unsigned char k = operator_11<unsigned char, 0x08>::value;

	if (operator_09<int_value<0x10>, int_value<operator_02<int_value<0x10>, int_value<0x02>>::result.value>>::result.value)
	{
		k ^= operator_12<unsigned char, 0x10>::value;
	}

	if (operator_10<int_value<operator_05<int_value<0x10>, int_value<0x02>>::result.value>>::result.value)
	{
		k ^= operator_12<unsigned char, 0x20>::value;
	}
	std::cout << k << std::endl;
	for (int loop = 0; loop < sizeof(encoded_flag); ++loop)
	{
		encoded_flag[loop] ^= k;
	}

	std::ofstream output("encoded_flag.txt", std::ios::binary);
	if (output.is_open())
	{
		output.write(reinterpret_cast<const char*>(encoded_flag),
			sizeof(encoded_flag));

		output.close();
	}

	return 0;
}



/*
k = [0x62,0x27,0x66,0x0D,0x0B]
for i in k:
	t = i ^ 0x34
	print chr(t+0x20)
k = [0xB2,0xEA,0xA8,0xB8,0xDE]

for i in k:
	t = i ^ 0x34
	print chr(t/2)

YISF{v3rY_CoNFu5inG}	*/