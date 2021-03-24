import re
import sys


def tToken_finder(char):
        if (char == "+"):
            return "SUM"
        elif(char == "-"):
            return "MIN"
        elif(char == "/"):
            return "DIV"
        elif(char == "*"):
            return "MUT"
        elif(char == "("):
            return "OPN"
        elif(char == ")"):
            return "CLS"
        else:
            return "NUM"



class Token:
  def __init__(self, tToken = None, value = None):
    self.type = tToken
    self.value = value

class PrePro():
    @staticmethod
    def filter(code):
        stringWNComents = re.sub(re.compile("/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/",re.DOTALL ) ,"" ,code)
        return stringWNComents

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

            if((self.position < len(self.origin)) and self.actual.type == "NUM"):
                while(tToken_finder(self.origin[self.position]) == "NUM"):
                    self.actual.value += self.origin[self.position]
                    self.position += 1
                    if(self.position == len(self.origin)):
                        break

        return self.actual

        


class Parser():
    def __init__(self):
        self.tokens = Tokenizer

    @staticmethod
    def parseExpression():
        Parser.tokens.selectNext()
        res = Parser.parseTerm()

        while(Parser.tokens.actual.type == "SUM" or Parser.tokens.actual.type == "MIN"):
            if (Parser.tokens.actual.type == "SUM"):
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == "NUM"):
                    res += Parser.parseTerm()
                elif(Parser.tokens.actual.type == "OPN"):
                    res+=Parser.Expression()
                else:
                    if(Parser.tokens.actual.type == "SUM" or Parser.tokens.actual.type == "MIN"):
                        res += Parser.unaryCalc()
                    else:
                        raise Exception('Comando errado1')

            elif (Parser.tokens.actual.type == "MIN"):
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == "NUM"):
                    res -= Parser.parseTerm()
                elif(Parser.tokens.actual.type == "OPN"):
                    res-=Parser.Expression()
                else:
                    if(Parser.tokens.actual.type == "SUM" or Parser.tokens.actual.type == "MIN"):
                        res += Parser.unaryCalc()
                    raise Exception('Comando errado2')

        if (Parser.tokens.actual.type == "END"):
            return res
        else:
            raise Exception('Comando errado3')
    
    @staticmethod
    def parseTerm():
        if(Parser.tokens.actual.type == "NUM" or Parser.tokens.actual.type == "OPN"):
            if(Parser.tokens.actual.type == "NUM"):
                res = float(Parser.tokens.actual.value)
            elif(Parser.tokens.actual.type == "OPN"):
                res = Parser.Expression()
            Parser.tokens.selectNext()
            while(Parser.tokens.actual.type == "DIV" or Parser.tokens.actual.type == "MUT"):
                if (Parser.tokens.actual.type == "DIV"):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == "NUM"):
                        res /= float(Parser.tokens.actual.value)
                    elif(Parser.tokens.actual.type == "OPN"):
                        res/=Parser.Expression()
                    else:
                        raise Exception('Comando errado4')

                elif (Parser.tokens.actual.type == "MUT"):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == "NUM"):
                        res *= float(Parser.tokens.actual.value)
                    elif(Parser.tokens.actual.type == "OPN"):
                        res*=Parser.Expression()
                    else:
                        raise Exception('Comando errado5')

                Parser.tokens.selectNext()
            return res
        elif(Parser.tokens.actual.type == "SUM" or Parser.tokens.actual.type == "MIN"):
            return Parser.unaryCalc()
            
        else:
            raise Exception('Comando errado6')

    @staticmethod
    def Expression():
        open = 1
        Parser.tokens.selectNext()
        dentroDoParenteses = ""
        while(open !=0):
            if(Parser.tokens.actual.type == "END"):
                raise Exception("Did not close parenthesis")
            elif(Parser.tokens.actual.type == "OPN"):
                open +=1
            elif(Parser.tokens.actual.type == "CLS"):
                open -=1
            else:
                dentroDoParenteses += Parser.tokens.actual.value
            Parser.tokens.selectNext()
        dentroDoParenteses = Parser().run(dentroDoParenteses)
        return dentroDoParenteses

    @staticmethod
    def unaryCalc():
        maisOuMenos = 0
        while(Parser.tokens.actual.type == "SUM" or Parser.tokens.actual.type == "MIN"):
            if(Parser.tokens.actual.type == "SUM"):
                maisOuMenos += 1
            else:
                maisOuMenos -= 1
            Parser.tokens.selectNext()
        if(Parser.tokens.actual.type == "NUM"):
            if(maisOuMenos < 0):
                res = float(Parser.tokens.actual.value)* -1
                Parser.tokens.selectNext()
                return res
            res = float(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            return res
        else:
            raise Exception('Unary error')

        
    @staticmethod
    def run(code):
        #tira comentarios
        code = PrePro().filter(code)
        #executa o compilador
        Parser.tokens = Parser().tokens(origin = code) 
        return Parser().parseExpression()
    

        

def main():
    if(len(sys.argv) < 2):
        raise Exception("Comando não passado")
    comando = ""
    for i in range(1,len(sys.argv)):
        # print(sys.argv)
        comando += sys.argv[i]
        comando += " "
    resultado = Parser().run(comando)

    print("{:.0f}".format(round(resultado,2)))


if __name__ == "__main__":
    main()