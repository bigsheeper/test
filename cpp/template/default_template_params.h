#pragma once

#include <iostream>

template<typename T = int>
class A {
public:
    explicit A(T t) : t_(t) {}

    void Func1() {
      std::cout << t_ << std::endl;
    }

private:
    T t_;
};