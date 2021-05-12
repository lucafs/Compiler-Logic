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
        elif(char == "{"):
            return "OPN_COM"
        elif(char == "}"):
            return "CLS_COM"                    
        elif(char == "="):
            return "EQL"
        elif(char == ";"):
            return "ENDCOM"
        elif(char == ">"):
            return "GREATER"
        elif(char == "<"):
            return "LESS"
        elif(char == "!"):
            return "NEG"
        elif(char == "&"):
            return "AND"
        elif(char == "|"):
            return "OR"   
        elif(char.isalpha() or char == "-" or char == "_"):
            return "IDENT"
        elif(char.isdigit()):
            return "NUM"
        else:
            return "?"


def IdentType(char):
    if(char == "println"):
        return "PRINT"
    elif(char == "readln"):
        return "READ"
    elif(char == "if"):
        return "IF"
    elif(char == "else"):
        return "ELSE"                
    elif(char == "while"):
        return "WHILE"


class SymbolTable:

    def __init__(self):
        self.sym = {}

    def setter(self, name, value):
        self.sym[name] = value

    def getter(self, name):
        return self.sym[name]


class Node():
    def __init__(self,value = None , children = []):
        self.value = value
        self.children = []
    def Evaluate(self,ST):
        pass

class NoOp(Node):
    def Evaluate(self,ST):
        pass


class IntVal(Node):
    def Evaluate(self,ST):
        return int(self.value)
class UnOp(Node):
    def Evaluate(self,ST):
        if self.value == '+':
            return self.children[0].Evaluate(ST)
        else:
            return -self.children[0].Evaluate(ST)

class BinOP(Node):
    def Evaluate(self,ST):
        if (self.value=="+"):
            return int(self.children[0].Evaluate(ST)) + int(self.children[1].Evaluate(ST))
        if (self.value=="-"):
            return int(self.children[0].Evaluate(ST)) - int(self.children[1].Evaluate(ST))
        if (self.value=="*"):
            return int(self.children[0].Evaluate(ST)) * int(self.children[1].Evaluate(ST))
        if (self.value=="/"):
            return int(self.children[0].Evaluate(ST)) // int(self.children[1].Evaluate(ST))

class Assign(Node):
    def Evaluate(self, ST):
        expression = self.children[1].Evaluate(ST)
        name = self.children[0].value
        ST.setter(name, expression)

class Identifier(Node):
    def Evaluate(self, ST):
        return ST.getter(self.value)

class Println(Node):
    def Evaluate(self, ST):
        print_value = self.children[0].Evaluate(ST)
        print(print_value)

class ReadLn(Node):
    def Evaluate(self, ST):
        return int(input())

class LogOp(Node):

    def Evaluate(self, ST):
        if self.value == "<":
            return self.children[0].Evaluate(ST) < self.children[1].Evaluate(ST)
        elif self.value == ">":
            return self.children[0].Evaluate(ST) > self.children[1].Evaluate(ST)
        elif self.value == "==":
            return self.children[0].Evaluate(ST) == self.children[1].Evaluate(ST)
        elif self.value == "&&":
            return self.children[0].Evaluate(ST) and self.children[1].Evaluate(ST)
        elif self.value == "!":
            return not self.children[0].Evaluate(ST)
        elif self.value == "||":
            return self.children[0].Evaluate(ST) or self.children[1].Evaluate(ST)


class WhileOp(Node):

    def Evaluate(self, ST):  
        while (self.children[0].Evaluate(ST)):
            self.children[1].Evaluate(ST)
        
    
class IfOp(Node):
    def Evaluate(self, ST):
        if (self.children[0].Evaluate(ST)):
            self.children[1].Evaluate(ST) 
        else:
            if len(self.children) > 2:
                self.children[2].Evaluate(ST)



class Comandos(Node):
    def Evaluate(self, ST):
        for x in self.children:
            x.Evaluate(ST)









class Token:
  def __init__(self, tToken = None, value = None):
    self.type = tToken
    self.value = value

class PrePro():
    @staticmethod
    def filter(code):
        stringWNComents = re.sub(re.compile("/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/",re.DOTALL ) ,"" ,code)
        stringWNComents = stringWNComents.replace('\n','')
        return stringWNComents

class Tokenizer:
  def __init__(self, origin = None, position = 0 ,actual = None):
    self.origin = origin #string
    self.position = position #posicao atual
    self.actual = actual #token

  def selectNext(self):
        #se for o ultimo acaba
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
            if((self.position < len(self.origin)) and self.actual.type == "IDENT"):
                while(tToken_finder(self.origin[self.position]) == "IDENT" or tToken_finder(self.origin[self.position]) == "NUM"):
                    self.actual.value += self.origin[self.position]
                    self.position += 1
                    if(self.actual.value == "else"):
                        break
                    if(self.position == len(self.origin)):
                        break
                identT = IdentType(self.actual.value)
                if(identT != None):
                    self.actual.type = identT


            if((self.position < len(self.origin)) and self.actual.type == "ENDCOM"):
                while(tToken_finder(self.origin[self.position]) == "ENDCOM"):
                    self.actual.value += self.origin[self.position]
                    self.position += 1
                    if(self.position == len(self.origin)):
                        break
            if((self.position < len(self.origin)) and self.actual.type == "EQL"):
                if(tToken_finder(self.origin[self.position]) == "EQL"):
                    self.actual.value += self.origin[self.position]
                    self.actual.type = "DUALEQL"
                    self.position +=1

            if(self.actual.type == "OR"):
                if(tToken_finder(self.origin[self.position]) != "OR"):
                    raise Exception("OR INCOMPLETE")
                self.position +=1
                self.actual.value += self.origin[self.position]

            if(self.actual.type == "AND"):
                if(tToken_finder(self.origin[self.position]) != "AND"):
                    raise Exception("AND INCOMPLETE")
                self.position +=1
                self.actual.value += self.origin[self.position]

        return self.actual

        


class Parser():
    def __init__(self):
        self.tokens = Tokenizer

    @staticmethod
    def parseOrexPR():
        res = Parser.parseAndexPR()
        while(Parser.tokens.actual.type == "OR"):
            node = LogOp("||",[])
            node.children.append(res)
            node.children.append(Parser.parseAndexPR())
            res = node

        return res

    @staticmethod
    def parseAndexPR():
        res = Parser.parseEqePR()
        while(Parser.tokens.actual.type == "AND"):
            node = LogOp("&&",[])
            node.children.append(res)
            node.children.append(Parser.parseEqePR())
            res = node

        return res

    @staticmethod
    def parseEqePR():
        res = Parser.parseRelexPR()
        while(Parser.tokens.actual.type == "DUALEQL"):
            node = LogOp("==",[])
            node.children.append(res)
            node.children.append(Parser.parseRelexPR())
            res = node

        return res


    @staticmethod
    def parseRelexPR():
        res = Parser.parseExpression()
        while(Parser.tokens.actual.type == "GREATER" or Parser.tokens.actual.type == "LESS"):
            if(Parser.tokens.actual.type == "GREATER"):
                node = LogOp(">",[])
                node.children.append(res)
                node.children.append(Parser.parseExpression())
            elif(Parser.tokens.actual.type == "LESS"):
                node = LogOp("<",[])
                node.children.append(res)
                node.children.append(Parser.parseExpression())
            res = node

        return res

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
    def parseFactor():
        Parser.tokens.selectNext()
        res = 0
        if(Parser.tokens.actual.type == "NUM"):
            res = Parser.tokens.actual.value
            node = IntVal(res)
            Parser.tokens.selectNext()
            return node
        elif(Parser.tokens.actual.type== "IDENT"):
            node = Identifier()
            node.value= Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return node
        elif(Parser.tokens.actual.type == "SUM" or Parser.tokens.actual.type == "MIN" or Parser.tokens.actual.type == "NEG"):
            if(Parser.tokens.actual.type == "SUM"):
                node = UnOp("+", [])
                node.children.append(Parser.parseFactor())    
                return node            
            elif(Parser.tokens.actual.type == "MIN"):
                node = UnOp("-", [])
                node.children.append(Parser.parseFactor())   
                return node
            elif(Parser.tokens.actual.type == "NEG"):
                node = LogOp("!", [])
                node.children.append(Parser.parseFactor())   
                return node
        elif(Parser.tokens.actual.type == "OPN"):
            res = Parser.parseOrexPR()
            if(Parser.tokens.actual.type != "CLS"):
                raise Exception ("Parenteses não fechados")
            Parser.tokens.selectNext()
            return res
        elif(Parser.tokens.actual.type == "READ"):
            node = ReadLn("READ", [])
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "OPN"):
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == "CLS"):
                    Parser.tokens.selectNext()
                else:
                    raise Exception("Read error")
            else:
                raise Exception("Read error")
            return node 
        else:
            raise Exception ("Factor error")    


    @staticmethod
    def parseBlock():
        if Parser.tokens.actual.type == "OPN_COM":
            commands = Comandos()
            Parser.tokens.selectNext()
            while(Parser.tokens.actual.type != "CLS_COM"):
                commands.children.append(Parser.parseCommand())
            if(Parser.tokens.actual.type == "CLS_COM"):
                Parser.tokens.selectNext()
            else:
                raise Exception("} not found")
            return commands
        else:

            raise Exception("{ not found")

    @staticmethod
    def parseCommand():
        if Parser.tokens.actual.type == "IDENT":
            var_name = Parser.tokens.actual.value
            var_node = Identifier(var_name, [])

            Parser.tokens.selectNext()

            if Parser.tokens.actual.type == "EQL":
                assign = Assign("=", [])
                assign.children.append(var_node)
                value = Parser.parseOrexPR()
                assign.children.append(value)
                if Parser.tokens.actual.type != "ENDCOM":
                    raise Exception("; NOT FOUND")
                Parser.tokens.selectNext()
            else:
                raise Exception("COMMAND ERROR")
            
            return assign
        

        elif Parser.tokens.actual.type == "PRINT":
            print_node = Println("PRINT", [])
            print_value = Parser.parseOrexPR()
            print_node.children.append(print_value)
            if Parser.tokens.actual.type != "ENDCOM":
                raise Exception("; NOT FOUND")
            Parser.tokens.selectNext()
            return print_node
        
        elif Parser.tokens.actual.type == "WHILE":
            while_node = WhileOp('while', [])
            Parser.tokens.selectNext()
          
            if Parser.tokens.actual.type == 'OPN':
                while_node.children.append(Parser.parseOrexPR())
                if Parser.tokens.actual.type == 'CLS':
                    Parser.tokens.selectNext()
                    while_node.children.append(Parser.parseCommand())
                else:
                    raise Exception("WHILE ERROR")
            else:
                raise Exception("WHILE ERROR")
            return while_node
        
        elif Parser.tokens.actual.type == "IF":
            if_node = IfOp("if",[])
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'OPN':
                if_node.children.append(Parser.parseOrexPR())
                if Parser.tokens.actual.type == 'CLS':
                    Parser.tokens.selectNext()
                    if_node.children.append(Parser.parseCommand())
                    if Parser.tokens.actual.type == "ELSE":
                        Parser.tokens.selectNext()
                        if_node.children.append(Parser.parseCommand())
                else:
                    raise Exception("IF ERROR")
            else:
                raise Exception("IF ERROR")
            return if_node  
        elif Parser.tokens.actual.type == "ENDCOM":
            return NoOp()
        else:
            return Parser.parseBlock()

        
    @staticmethod
    def run(code):
        #tira comentarios
        code = PrePro().filter(code)
        #executa o compilador
        Parser.tokens = Parser().tokens(origin = code) 
        Parser.tokens.selectNext()
        res =  Parser().parseBlock()
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
    ST = SymbolTable()
    resultado.Evaluate(ST)

if __name__ == "__main__":
    main()