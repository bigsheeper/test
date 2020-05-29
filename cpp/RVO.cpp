#include <iostream>

struct C {
    C() = default;
    C(const C&) { std::cout << "A copy was made.\n"; }
};

C f() {
  return C();
}

int main() {
  std::cout << "Hello World!\n";
  C obj = f();
}

//g++ -std=c++11 RVO.cpp && ./a.out
//Hello World!
//
//g++ -std=c++11 -fno-elide-constructors RVO.cpp && ./a.out
//Hello World!
//A copy was made.
//A copy was made.
