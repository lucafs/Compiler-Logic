import re
import sys
from abc import ABC, abstractmethod

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


class Node():
    def __init__(self,value = None , children = []):
        self.value = value
        self.children = []
    def evaluate(self):
        pass

class NoOp(Node):
    def Evaluate(self):
        pass

class IntVal(Node):
    def Evaluate(self):
        return int(self.value)
class UnOp(Node):
    def Evaluate(self):
        if self.value == '+':
            return self.children[0].Evaluate()
        else:
            return -self.children[0].Evaluate()

class BinOP(Node):
    def Evaluate(self):
        if (self.value=="+"):
            return int(self.children[0].Evaluate()) + int(self.children[1].Evaluate())
        if (self.value=="-"):
            return int(self.children[0].Evaluate()) - int(self.children[1].Evaluate())
        if (self.value=="*"):
            return int(self.children[0].Evaluate()) * int(self.children[1].Evaluate())
        if (self.value=="/"):
            return int(self.children[0].Evaluate()) // int(self.children[1].Evaluate())



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
            res = Parser.tokens.actual.value
            node = IntVal(res)
            Parser.tokens.selectNext()
            return node

        elif(Parser.tokens.actual.type == "SUM" or Parser.tokens.actual.type == "MIN"):
            if(Parser.tokens.actual.type == "SUM"):
                node = UnOp("+", [])
                node.children.append(Parser.parseFactor())    
                return node            
            elif(Parser.tokens.actual.type == "MIN"):
                node = UnOp("-", [])
                node.children.append(Parser.parseFactor())   
                return node
        elif(Parser.tokens.actual.type == "OPN"):
            res = Parser.parseExpression()
            if(Parser.tokens.actual.type != "CLS"):
                raise Exception ("Parenteses não fechados")
            Parser.tokens.selectNext()
            return res


        else:
            raise Exception ("Factor error")    


    @staticmethod
    def parseExpression():
        res = Parser.parseTerm()

        while(Parser.tokens.actual.type == "SUM" or Parser.tokens.actual.type == "MIN"):
            if (Parser.tokens.actual.type == "SUM"):
                node = BinOP("+",[])
                node.children.append(res)
                node.children.append(Parser.parseTerm())

            elif (Parser.tokens.actual.type == "MIN"):
                node = BinOP("-",[])
                node.children.append(res)
                node.children.append(Parser.parseTerm())
            res = node
        return res

    @staticmethod
    def parseTerm():
        res = Parser.parseFactor()
        while(Parser.tokens.actual.type == "MUT" or Parser.tokens.actual.type == "DIV"):
            if(Parser.tokens.actual.type == "MUT"):
                node = BinOP("*",[])
                node.children.append(res)
                node.children.append(Parser.parseFactor())

            elif(Parser.tokens.actual.type == "DIV"):
                node = BinOP("/",[])
                node.children.append(res)
                node.children.append(Parser.parseFactor())
            res = node

        return res



        
    @staticmethod
    def run(code):
        #tira comentarios
        code = PrePro().filter(code)
        #executa o compilador
        Parser.tokens = Parser().tokens(origin = code) 
        res =  Parser().parseExpression()
        if(Parser.tokens.actual.type != "END"):
            raise Exception ("ERROR")
        return res
    

        
def main():
    if(len(sys.argv) < 2):
        raise Exception("Comando não passado")
    file = ""
    for i in range(1,len(sys.argv)):
        file += sys.argv[i]
    f = open(file,'r')
    comando = f.read()
    resultado = Parser().run(comando)
    resultado = resultado.Evaluate()

    print(resultado)

if __name__ == "__main__":
    main()