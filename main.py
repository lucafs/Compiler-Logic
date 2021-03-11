import re
import sys


def tToken_finder(char):
        if (char == "+"):
            return "SUM"
        elif(char == "-"):
            return "MIN"
        else:
            return "NUM"


class Token:
  def __init__(self, tToken = None, value = None):
    self.type = tToken
    self.value = value



class Tokenizer:
  def __init__(self, origin = None, position = 0 ,actual = None):
    self.origin = origin #string
    self.position = position #posicao atual
    self.actual = actual #token

  def selectNext(self):
        #se for o ultimo acaba
        teveEspaco = 0
        if (self.position >= len(self.origin)):
            self.actual = Token(tToken= "END")
            return self.actual
        if(self.position < len(self.origin)):
            #passa enquanto for espaço
            while(self.origin[self.position] == " "):
                self.position += 1
                teveEspaco = 1
                #se for o ultimo acaba
                if (self.position >= len(self.origin)):
                    self.actual = Token(tToken= "END")
                    return self.actual

            #checa se teve espaço entre numeros
            if(teveEspaco == 1 and self.actual.type == "NUM" and tToken_finder(self.origin[self.position]) == "NUM"):
                raise Exception ("Error espaço entre numeros")


            #Aqui achou o proximo token valido.
            self.actual = Token(tToken= tToken_finder(self.origin[self.position]),value = self.origin[self.position])
            self.position += 1
                
        return self.actual

        


class Parser():
    def __init__(self):
        self.tokens = Tokenizer

    @staticmethod
    def parseExpression():
        Parser.tokens.selectNext()
        op = 0
        while(Parser.tokens.actual.type != "END"):
            numAtual = ""
            if(Parser.tokens.actual.type == "NUM"):
                while(Parser.tokens.actual.type == "NUM"):
                    numAtual += Parser.tokens.actual.value
                    Parser.tokens.selectNext()
                if op == 0:
                    resultado  = int(numAtual)
                elif op == 1:
                    resultado -= int(numAtual)
                    op = 0
                elif op == 2:
                    resultado += int(numAtual)
                    op = 0
                
                if (Parser.tokens.actual.type == "MIN"):
                    op = 1
                    Parser.tokens.selectNext()
                elif(Parser.tokens.actual.type == "SUM"):
                    op = 2
                    Parser.tokens.selectNext()

            else:
                raise Exception ("Comando errado")
        #checa se não acaba com um operando.
        if(op != 0):
            raise Exception ("Comando errado")
        return resultado


        
    @staticmethod
    def run(code):
        Parser.tokens = Parser().tokens(origin = code) 
        return Parser().parseExpression()
    

        

def main():
    if(len(sys.argv) < 2):
        raise Exception("Comando não passado")
    comando = ""
    for i in range(1,len(sys.argv)):
        comando += sys.argv[i]
        comando += " "

    print(Parser().run(comando))


if __name__ == "__main__":
    main()