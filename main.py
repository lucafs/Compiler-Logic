import sys

def calculadora(sys):
    comando = sys.argv[1]
    #Tira espaços da conta
    comando = comando.replace(' ', '')    
    numbers = ["0"]
    operacao = []
    cont_num = 0
    for i in comando:
        if (i == "+"):
            operacao.append(0)
            numbers.append("0")
            cont_num += 1
        elif(i == "-"):
            operacao.append(1)
            numbers.append("0")
            cont_num += 1
        else:
            numbers[cont_num] += i
    resultado = int(numbers[0])
    for i in range(len(operacao)):
        if operacao[i] == 0:
            resultado += int(numbers[i+1])
        elif operacao[i] == 1:
            resultado -= int(numbers[i+1])
    print("O resultado dessa operação é {0}".format(resultado))


calculadora(sys)