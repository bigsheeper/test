cmake_minimum_required(VERSION 3.16)
project(gdal)

set(CMAKE_CXX_STANDARD 14)

set(CONDA_PREFIX "$ENV{CONDA_PREFIX}")
message(STATUS "conda_prefix = " ${CONDA_PREFIX})
include_directories(${CONDA_PREFIX}/include)
link_directories(${CONDA_PREFIX}/lib)

add_executable(main main.cpp)

target_link_libraries(main gdal)