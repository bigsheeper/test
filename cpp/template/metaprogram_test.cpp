#include <type_traits>
#include <iostream>

template<class T>
typename std::enable_if<std::is_arithmetic<T>::value, int>::type foo1(T t) {
  std::cout << t << std::endl;
  return 0;
}

template<class T>
typename std::enable_if<!std::is_arithmetic<T>::value, int>::type foo1(T t) {
  std::cout << t << std::endl;
  return 1;
}

int main() {
  foo1(1);
  foo1("abc");
  return 0;
}

