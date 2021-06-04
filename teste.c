/*Error: tipo de retorno*/

int soma(int x, int y)
{
    int res;
    res = x + y;
    return "somei";    
}

int main()
{
    string x;
    x = soma(3,2);
    println(x);
    
}
