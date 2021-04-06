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
                #se for o ultimo acaba
                if (self.position >= len(self.origin)):
                    self.actual = Token(tToken= "END")
                    return self.actual


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
    def parseFactor():

        Parser.tokens.selectNext()
        res = 0
        if(Parser.tokens.actual.type == "NUM"):
            res = int(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
        elif(Parser.tokens.actual.type == "SUM" or Parser.tokens.actual.type == "MIN"):
            if(Parser.tokens.actual.type == "SUM"):
                res += int(Parser.parseFactor())
                # Parser.tokens.selectNext()
            elif(Parser.tokens.actual.type == "MIN"):
                res -= int(Parser.parseFactor())
                # Parser.tokens.selectNext()
        elif(Parser.tokens.actual.type == "OPN"):
            res = Parser.parseExpression()
            if(Parser.tokens.actual.type != "CLS"):
                raise Exception ("Parenteses não fechados")
            Parser.tokens.selectNext()

        else:
            raise Exception ("Factor error")    
        return res


    @staticmethod
    def parseExpression():
        res = Parser.parseTerm()

        while(Parser.tokens.actual.type == "SUM" or Parser.tokens.actual.type == "MIN"):
            if (Parser.tokens.actual.type == "SUM"):
                res += int(Parser.parseTerm())

            elif (Parser.tokens.actual.type == "MIN"):
                res -= int(Parser.parseTerm())

        return res

    @staticmethod
    def parseTerm():
        res = int(Parser.parseFactor())
        while(Parser.tokens.actual.type == "MUT" or Parser.tokens.actual.type == "DIV"):
            if(Parser.tokens.actual.type == "MUT"):
                res *= int(Parser.parseFactor())

            elif(Parser.tokens.actual.type == "DIV"):
                res /= int(Parser.parseFactor())

        return res



        
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