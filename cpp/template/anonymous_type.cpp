template <typename T>
class X {};

template <typename T>
void F(T t) {}

struct A {
} a;

// b is a anonymous type variable.
struct {
    int i;
} b;

// B is a anonymous type.
typedef struct {int i;} B;

using G = B;

void Fun() {
  struct C {} c;

  typedef struct {int i;} D;

  X<A> x1;
  X<B> x2;
  X<C> x3;
  X<D> x4;

  F<A>(a);
//  F<B>(b); // Illegal
  F<C>(c);
  D d{1};
  F<D>(d);
}
