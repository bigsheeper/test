#include <tuple>
#include <iostream>

template<typename ... elements>
void Func1(elements... args) {
  std::cout << "tuple size = " << sizeof...(args) << std::endl;
  int res[sizeof...(args)] = {args...};
  std::cout << res[0] << std::endl;
}

template<typename ... elements>
void Func2(std::tuple<elements...> args) {
//  std::cout << "tuple size = " << std::tuple_size<elements>::value << std::endl;
  std::cout << std::get<0>(args) << std::endl;
}

int main() {
  Func1(1, 2, 3, 4);
  Func2(std::make_tuple(5, 6, 7, 8));
  return 0;
}

