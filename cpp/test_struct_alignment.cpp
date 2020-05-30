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
//  std::cout << sizeof(structa_t) << std::endl;
//  std::cout << sizeof(structb_t) << std::endl;
  std::cout << sizeof(structc_t) << std::endl;
//  std::cout << sizeof(structd_t) << std::endl;
//  std::cout << sizeof(e) << std::endl;

  return 0;
}

