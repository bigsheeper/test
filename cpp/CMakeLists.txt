cmake_minimum_required(VERSION 3.16)
project(cpp)

set(CMAKE_CXX_STANDARD 14)

add_executable(rvo RVO.cpp)

add_executable(test_constexpr test_constexpr.cpp)

add_subdirectory(template)

add_executable(test_lambda test_lambda.cpp)

add_executable(test_volatile test_volatile.cpp)

add_executable(test_struct_alignment test_struct_alignment.cpp)