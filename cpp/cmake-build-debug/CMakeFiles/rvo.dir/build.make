# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/sheep/workspace/arctern/sheep/test/arctern/cpp

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/sheep/workspace/arctern/sheep/test/arctern/cpp/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/rvo.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/rvo.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/rvo.dir/flags.make

CMakeFiles/rvo.dir/RVO.cpp.o: CMakeFiles/rvo.dir/flags.make
CMakeFiles/rvo.dir/RVO.cpp.o: ../RVO.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sheep/workspace/arctern/sheep/test/arctern/cpp/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/rvo.dir/RVO.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/rvo.dir/RVO.cpp.o -c /home/sheep/workspace/arctern/sheep/test/arctern/cpp/RVO.cpp

CMakeFiles/rvo.dir/RVO.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/rvo.dir/RVO.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/sheep/workspace/arctern/sheep/test/arctern/cpp/RVO.cpp > CMakeFiles/rvo.dir/RVO.cpp.i

CMakeFiles/rvo.dir/RVO.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/rvo.dir/RVO.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/sheep/workspace/arctern/sheep/test/arctern/cpp/RVO.cpp -o CMakeFiles/rvo.dir/RVO.cpp.s

# Object files for target rvo
rvo_OBJECTS = \
"CMakeFiles/rvo.dir/RVO.cpp.o"

# External object files for target rvo
rvo_EXTERNAL_OBJECTS =

rvo: CMakeFiles/rvo.dir/RVO.cpp.o
rvo: CMakeFiles/rvo.dir/build.make
rvo: CMakeFiles/rvo.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/sheep/workspace/arctern/sheep/test/arctern/cpp/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable rvo"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/rvo.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/rvo.dir/build: rvo

.PHONY : CMakeFiles/rvo.dir/build

CMakeFiles/rvo.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/rvo.dir/cmake_clean.cmake
.PHONY : CMakeFiles/rvo.dir/clean

CMakeFiles/rvo.dir/depend:
	cd /home/sheep/workspace/arctern/sheep/test/arctern/cpp/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sheep/workspace/arctern/sheep/test/arctern/cpp /home/sheep/workspace/arctern/sheep/test/arctern/cpp /home/sheep/workspace/arctern/sheep/test/arctern/cpp/cmake-build-debug /home/sheep/workspace/arctern/sheep/test/arctern/cpp/cmake-build-debug /home/sheep/workspace/arctern/sheep/test/arctern/cpp/cmake-build-debug/CMakeFiles/rvo.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/rvo.dir/depend
