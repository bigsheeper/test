#include "extern_template_instance.h"

extern template void Func1<int>(int t);
void test1() { Func1(1); }
