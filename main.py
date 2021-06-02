import re
import sys


class Assembly:

    commands = []

    @staticmethod
    def AddCommand(command):
        Assembly.commands.append(command)

    @staticmethod
    def WriteASM(ASMname):
        commands_list = Assembly.commands
        final_string = "\n".join(commands_list)

        ASM_code = f'''
; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

segment .bss  ; variaveis
  res RESB 1

section .text
  global _start

print:  ; subrotina print

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
  XOR ESI, ESI

print_dec: ; empilha todos os digitos
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI ; contador de digitos
  CMP EAX, 0
  JZ print_next ; quando acabar pula
  JMP print_dec

print_next:
  CMP ESI, 0
  JZ print_exit ; quando acabar de imprimir
  DEC ESI

  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT

  POP ECX
  MOV [res], ECX
  MOV ECX, res

  MOV EDX, 1
  INT 0x80
  JMP print_next

print_exit:
  POP EBP
  RET

; subrotinas if/while
binop_je:
  JE binop_true
  JMP binop_false

binop_jg:
  JG binop_true
  JMP binop_false

binop_jl:
  JL binop_true
  JMP binop_false

binop_false:
  MOV EBX, False
  JMP binop_exit
binop_true:
  MOV EBX, True
binop_exit:
  RET

_start:

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  ; codigo gerado pelo compilador
{final_string}

  ; interrupcao de saida
  POP EBP
  MOV EAX, 1
  INT 0x80'''

        f = open(ASMname, "w+")

        f.write(ASM_code)



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
    elif(char == "if"):
        return "IF"
    elif(char == "else"):
        return "ELSE"                
    elif(char == "while"):
        return "WHILE"
    elif(char == "bool" or char == "int"):
        return "TYPE"
    elif(char == "true" or char == "false"):
        return "BOOL"





class SymbolTable:

    def __init__(self):
        self.sym = {}
        self.varNum = 0
        self.loopNum=0

    def setter(self, name, value, type ,number):
        if(value != None):
            if(type == "bool"):
                value = bool(value)
            elif(type == "int"):
                value = int(value)
        self.sym[name] = (value,type,number)

    def getter(self, name):
        try:
            return self.sym[name]
        except:
            return "error"

    def get_varNum(self):
        self.varNum+=1
        return self.varNum     
           
    def get_loopNum(self):    
        self.loopNum +=1
        return self.loopNum * 4    


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
        command = " MOV EBX, {0} ;".format(self.value)
        Assembly.AddCommand(command)
        return (int(self.value),"int")

class BoolVal(Node):
    def Evaluate(self,ST):
        if(self.value == "true"):
            command = " MOV EBX, {0} ;".format(True)
            Assembly.AddCommand(command)
            return (True,"bool")
        else:
            command = " MOV EBX, {0} ;".format(False)
            Assembly.AddCommand(command)
            return (False,"bool")



class UnOp(Node):
    def Evaluate(self,ST):
        value = self.children[0].Evaluate(ST)[0]
        if self.value == '+':
            command = " MOV EBX, {0} ;".format(value)
            Assembly.AddCommand(command)
            return (value,"int")
        else:
            command = " MOV EBX, {0} ;".format(-value)
            Assembly.AddCommand(command)
            return (-value,"int")

class BinOP(Node):
    def Evaluate(self,ST):
        if (self.value=="+"):
            command =" POP EAX ;\n ADD EAX, EBX ;\n MOV EBX, EAX ;"
            Assembly.AddCommand(command)
            return (int(self.children[0].Evaluate(ST)[0]) + int(self.children[1].Evaluate(ST)[0]),"int")
        if (self.value=="-"):
            command =" POP EAX ;\n SUB EAX, EBX ;\n MOV EBX, EAX ;"
            Assembly.AddCommand(command)
            return (int(self.children[0].Evaluate(ST)[0]) - int(self.children[1].Evaluate(ST)[0]),"int")
        if (self.value=="*"):
            command =" POP EAX ;\n IMUL EAX, EBX ;\n MOV EBX, EAX ;"
            Assembly.AddCommand(command)
            return (int(self.children[0].Evaluate(ST)[0]) * int(self.children[1].Evaluate(ST)[0]),"int")
        if (self.value=="/"):
            command =" POP EAX ;\n DIV EAX, EBX ;\n MOV EBX, EAX ;"
            Assembly.AddCommand(command)
            return (int(self.children[0].Evaluate(ST)[0]) // int(self.children[1].Evaluate(ST)[0]),"int")

class FirstAssign(Node):
    def Evaluate(self, ST):
        type = self.children[0]
        name = self.children[1]
        number =ST.get_varNum()
        if(ST.getter(name) != "error"):
            raise Exception ("Variable " + name + " aready declared")
        command = " PUSH DWORD 0 ;\n MOV [EBP-{0}], EBX ".format(number)
        Assembly.AddCommand(command)
        ST.setter(name, None ,type,number)

class Assign(Node):
    def Evaluate(self, ST):
        name = self.children[0].value
        expression = self.children[1].Evaluate(ST)
        type = ST.getter(name)[1]
        number = ST.getter(name)[2]
        if(type == "error"):
            raise Exception ("Symbol "+ name + " not declared")
        if(expression[1] != type):
            if((expression[1] == "bool" and type == "int") or (expression[1] == "int" and type == "bool")):
                pass
            else:
                raise Exception("Can't cast the "+ name +" variable")
        command = " MOV [EBP-{0}], EBX;".format(number)
        Assembly.AddCommand(command)
        ST.setter(name, expression[0],type,number)

class Identifier(Node):
    def Evaluate(self, ST):
        val = ST.getter(self.value)
        command = ' MOV EBX, [EBP-{0}] ;'.format(val[2])
        Assembly.AddCommand(command)
        return val

class Println(Node):
    def Evaluate(self, ST):
        print_value = self.children[0].Evaluate(ST)
        if(print_value == "error"):
            raise Exception ("Symbol "+self.children[0].value+" not declared")
        else:
            command = " PUSH EBX ;\n CALL print ;\n POP EBX ;"
            Assembly.AddCommand(command)
            print(print_value[0])


class LogOp(Node):
    def Evaluate(self, ST): 
        if self.value == "<":
            command = " POP EAX \n CMP EAX, EBX\n CALL binop_jl"
            Assembly.AddCommand(command)
            return (self.children[0].Evaluate(ST)[0] < self.children[1].Evaluate(ST)[0],"bool")
        elif self.value == ">":
            command = " POP EAX \n CMP EAX, EBX\n CALL binop_jg"
            Assembly.AddCommand(command)
            return (self.children[0].Evaluate(ST)[0] > self.children[1].Evaluate(ST)[0],"bool")
        elif self.value == "==":
            command = " POP EAX \n CMP EAX, EBX\n CALL binop_je"
            Assembly.AddCommand(command)
            return (self.children[0].Evaluate(ST)[0] == self.children[1].Evaluate(ST)[0],"bool")
        elif self.value == "&&":
            command = " POP EAX \n AND EAX, EBX\n CALL binop_jl"
            Assembly.AddCommand(command)
            if(bool(self.children[0].Evaluate(ST)[0] & self.children[1].Evaluate(ST)[0])):
                return(True,"bool")
            else:
                return (False,"bool")
        elif self.value == "||":
            command = " POP EAX \n OR EAX, EBX\n CALL binop_jl"
            Assembly.AddCommand(command)
            if(self.children[0].Evaluate(ST)[0] | self.children[1].Evaluate(ST)[0]):
                return (True,"bool")
            else:
                return(False,"bool")
        elif self.value == "!":
            return (not self.children[0].Evaluate(ST)[0],"bool") 


class WhileOp(Node):

    def Evaluate(self, ST):
        loopNum = ST.get_loopNum()
        command = " LOOP_{0}\n CMP EBX, False ;\n JE EXIT_{0};\n JMP LOOP_{0} ;\n EXIT_{0}:".format(loopNum)
        Assembly.AddCommand(command)
        while (self.children[0].Evaluate(ST)[0]):
            self.children[1].Evaluate(ST)
        
    
class IfOp(Node):
    def Evaluate(self, ST):
        loopNum = ST.get_loopNum()
        command = " CMP EBX, False ;\n"
        if len(self.children) > 2:
            command += " JE ELSE_{0} ;\n".format(loopNum)
        else:
            command += " JE EXIT_{0} ;\n".format(loopNum)
        command += " JMP EXIT_{0} ;\n".format(loopNum)
        if(len(self.children) > 2):
            command += ' ELSE_{0} ;\n'.format(loopNum)
        command += ' EXIT_{0} ;'.format(loopNum)
        Assembly.AddCommand(command)
        if (self.children[0].Evaluate(ST)[0]):
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
            while(self.origin[self.position] == " " or self.origin[self.position] == "\t"):
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
        elif(Parser.tokens.actual.type == "BOOL"):
            res = Parser.tokens.actual.value
            node = BoolVal(res)
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
        
        elif Parser.tokens.actual.type == "TYPE":
            firstAssign = FirstAssign("=", [])
            firstAssign.children.append(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "IDENT"):
                firstAssign.children.append(Parser.tokens.actual.value)
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type != "ENDCOM":
                    raise Exception("; NOT FOUND")
                Parser.tokens.selectNext()
            else:
                raise Exception("FIRST ASSIGN ERROR")
            return firstAssign


        

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
    Assembly.WriteASM("program.asm")

if __name__ == "__main__":
    main()