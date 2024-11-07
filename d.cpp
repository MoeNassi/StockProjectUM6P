#include <iostream>
#include <queue>
#include <stack>

int main() {
    std::queue < int > Qu;
    std::stack < int > St;

    Qu.push(5);
    Qu.push(51);
    Qu.push(3);
    Qu.push(125);
    Qu.push(34);    

    St.push(5);
    St.push(51);
    St.push(3);
    St.push(125);
    St.push(34);

    Qu.pop();
    St.pop();

    std::cout << Qu.back() << std::endl;
    std::cout << St.top() << std::endl;
}