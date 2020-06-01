#include <iostream>

// Alignment requirements
// (typical 32 bit machine)

// char         1 byte
// short int    2 bytes
// int          4 bytes
// double       8 bytes

// structure A
struct structa_tag {
    char c;
    short int s;
} structa_t;

// structure B
typedef struct structb_tag {
    int i;
    short int s;
    char c;
} structb_t;

// structure C
typedef struct structc_tag {
    char c;
    double d;
    int s;
} structc_t;

// structure D
typedef struct structd_tag {
    double d;
    int s;
    char c;
} structd_t;

struct E {
} e;

int main() {
  std::cout << sizeof(structa_t) << std::endl;
  std::cout << sizeof(structb_t) << std::endl;
  std::cout << sizeof(structc_t) << std::endl;
  std::cout << sizeof(structd_t) << std::endl;
//  std::cout << sizeof(e) << std::endl;

  return 0;
}

// 4
// 8
// 24
// 16

// https://www.geeksforgeeks.org/structure-member-alignment-padding-and-data-packing/

// why size of structc_t is 24?
// Because Every structure will also have alignment requirements.
// 假设 struct c1 占用 20 （1 + 7 + 8 + 4） 个字节，那么对于 struct c2，double 成员的起始位置就是 20 + 1 + 7 = 28，
// 不是 8 的整数倍，所以 double 应该进行偏移至 32，导致 size of structc_t 也对应进行偏移，为 24 而不是 20。
