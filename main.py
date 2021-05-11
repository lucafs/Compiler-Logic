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
        elif(char == "&"):
            return "AND"
        elif(char == "│"):
            return "OR"   
        elif(char.isalpha() or char == "-" or char == "_"):
            return "IDENT"
        elif(char.isdigit()):
            return "NUM"
        else:
            return "?"

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
    def Evaluate(self, st):
        return int(input())

class LogOp(Node):

    def Evaluate(self, st):
        if self.value == "<":
            return self.children[0].Evaluate(st) < self.children[1].Evaluate(st)
        elif self.value == ">":
            return self.children[0].Evaluate(st) > self.children[1].Evaluate(st)
        elif self.value == "==":
            return self.children[0].Evaluate(st) == self.children[1].Evaluate(st)
        elif self.value == "&&":
            return self.children[0].Evaluate(st) or self.children[1].Evaluate(st)
        elif self.value == "││":
            return self.children[0].Evaluate(st) and self.children[1].Evaluate(st)


class WhileOp(Node):

    def Evaluate(self, st):  
        while (self.children[0].Evaluate(st)):
            self.children[1].Evaluate(st)
        
    
class IfOp(Node):
    def Evaluate(self, st):
        if (self.children[0].Evaluate(st)):
            self.children[1].Evaluate(st) 
        else:
            if len(self.children) > 2:
                self.children[2].Evaluate(st)



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
                    if(self.position == len(self.origin)):
                        break

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



            if(self.actual.value == "println"):
                self.actual.type = "PRINT"
            elif(self.actual.value == "readln"):
                self.actual.type = "READ"
            elif(self.actual.value == "if"):
                self.actual.type = "IF"
            elif(self.actual.value == "else"):
                self.actual.type = "ELSE"                
            elif(self.actual.value == "while"):
                self.actual.type = "WHILE"
        return self.actual

        


class Parser():
    def __init__(self):
        self.tokens = Tokenizer

    @staticmethod
    def parseOrexPR():
        res = Parser.parseAndexPR()
        while(Parser.tokens.actual.type == "OR"):
            node = LogOp("││",[])
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
        Parser.tokens.selectNext()
        if Parser.tokens.actual.type == "OPN_COM":
            commands = Comandos()
            Parser.tokens.selectNext()
            while(Parser.tokens.actual.type != "CLS_COM"):
                commands.children.append(Parser.parseCommand())
                if(Parser.tokens.actual.type != "ENDCOM"):
                    print(Parser.tokens.actual.type)
                    raise Exception("; not found")
                Parser.tokens.selectNext()
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
            else:
                print(Parser.tokens.actual.value)
                raise Exception("COMMAND ERROR")
            
            return assign
        

        elif Parser.tokens.actual.type == "PRINT":
            print_node = Println("PRINT", [])
            print_value = Parser.parseOrexPR()
            print_node.children.append(print_value)
            if Parser.tokens.actual.type != "ENDCOM":
                raise Exception("; NOT FOUND")
            return print_node
        
        elif Parser.tokens.actual.type == "WHILE":
            while_node = WhileOp('while', [])
            Parser.tokens.selectNext()
          
            if Parser.tokens.actual.type == 'OPN':
                while_node.children.append(Parser.parseOrexPR())
                if Parser.tokens.actual.type == 'CLS':
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == 'ENDCOM':
                        while_node = NoOp()
                    else:
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
                    if Parser.tokens.actual.type == 'ENDCOM':
                        if_node.children.append(NoOp())
                    else:
                        if_node.children.append(Parser.parseCommand())
                    if Parser.tokens.actual.type == "ELSE":
                        print("salve")    
                else:
                    raise Exception("IF ERROR")
            else:
                raise Exception("IF ERROR")
            
        else:
            pass

        
    @staticmethod
    def run(code):
        #tira comentarios
        code = PrePro().filter(code)
        #executa o compilador
        Parser.tokens = Parser().tokens(origin = code) 
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