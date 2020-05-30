#include <iostream>

const int a = 1;
int b = 2;

constexpr int Fibonacci(int n) {
  return n == 1 ? 1 : n == 2 ? 2 : Fibonacci(n - 1) + Fibonacci(n - 2);
}

int SimpleFunc(int n) {
  return n;
}

constexpr int Func1(int &n) {
  // constexpr function can call only other constexpr function not simple function.
  // SimpleFunc(n); // illegal

  return a;
}

constexpr int &Func2(int n) {
  return b;
}

constexpr void Func3(int n) {
  int a = 1;
  ++a;
}

int main() {
  const int x = Fibonacci(5);
  std::cout << x << std::endl;

  Func1(b);

  Func3(2);
  return 0;
}

// reference <https://www.geeksforgeeks.org/understanding-constexper-specifier-in-c/>

