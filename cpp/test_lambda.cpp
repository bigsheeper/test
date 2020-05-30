#include <iostream>


class A {
public:
    int operator()(int x, int y) { return x + y; }
};

// [capture](parameters) mutable -> return-type { statement }
// capture 为捕捉列表

int main() {
  int i = 1;
  int j = 2;

  auto fun1 = [](int x, int y) { return x + y; };
  std::cout << fun1(3, 4) << std::endl;

  // 值传递
  auto fun2 = [=] { return i + j; };
  std::cout << fun2() << std::endl;

  // 引用传递
  auto fun3 = [&] { return i + j; };
  std::cout << fun3() << std::endl;

  // 值传递与引用传递的结果不一样。值传递在 lambda 函数被定义时就已经被决定了，而引用传递是运行时动态决定的。
  // 总之，需要捕捉的值成为常量，则使用值传递; 需要捕捉的值成为变量（类似参数），则使用引用传递。
  i++;
  std::cout << fun2() << std::endl;
  std::cout << fun3() << std::endl;

  A a;
  std::cout << a(5, 6) << std::endl;

  return 0;
}

