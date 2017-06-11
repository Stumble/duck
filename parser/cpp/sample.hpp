#include <iostream>
#include <algorithm>
#include <string>

namespace testMyOuter {
namespace testMyInner {

class xx;

class Base
{
    int x;
};

class Foo
{
public:
    explicit
    Foo(int);

    void
    print(std::string);

private:
    int id;
    int xx;
};

class Bar : public Foo, public Base
{
public:
    explicit
    Bar(int zz);

    bool
    test();

    void
    test(const Foo ** const shit);

    const Foo*
    returnTypeFunc();

public:
    Foo myDad;
    Foo* myDzz;
    const Foo hahah;
};


}
}