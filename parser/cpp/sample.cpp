#include "sample.hpp"

namespace testMyOuter {
namespace testMyInner {

Foo::Foo(int yy)
    : id(yy)
{
    xx = id + 1;
}

void
Foo::print(std::string str)
{
    std::cout << "I love " << str << std::endl;
}

Bar::Bar(int zz)
    : Foo(zz)
  , myDad(1)
  , hahah(123)
{
    std::cout << "constructor in Bar" << std::endl;
}

bool
Bar::test()
{
    std::cout << "laoziduojihang" << std::endl;
    return false;

}

void
Bar::test(const Foo ** const shit)
{
    print("zazhengne");
    Bar * b = new Bar(123);
    b->test();
    std::cout << "hahaha" << std::endl;
}


int main(int argc, char *argv[])
{
    Bar bb(123);
    bb.test();
    bb.print("sss");
    return 0;
}

}
}