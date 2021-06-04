/*Ok*/

int soma(int x, int y)
{
    int res;
    res = x + y;
    return res;    
}

int main()
{
    bool res;
    int x;
    x = 3;
    
    res = soma(x,2) == 8;
    
    println(res);
}
