
from symbolTable import SymbolTable

class Node:
        def Evaluate(self,table):
            pass
class BinOp(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        x=self.children[0].Evaluate(table)
        y=self.children[1].Evaluate(table)
        if x[1]==y[1]=="INTEIRO":
            if self.value=="+":
                return [(x[0]+y[0]),"INTEIRO"]
            if self.value=="-":
                return [(x[0]-y[0]),"INTEIRO"]
            if self.value=="*":
                return [(x[0]*y[0]),"INTEIRO"]
            if self.value=="/":
                return [(x[0]//y[0]),"INTEIRO"]
            if self.value=="<":
                if ((x[0]<y[0])):
                    return [True,"CONDICAO"]
                else:
                    return [False,"CONDICAO"]
            if self.value==">":
                if ((x[0]>y[0])):
                    return [True,"CONDICAO"]
                else:
                    return [False,"CONDICAO"]
            if self.value=="=":
                if ((x[0]==y[0])):
                    return [True,"CONDICAO"]
                else:
                    return [False,"CONDICAO"]

        if x[1]==y[1]=="CONDICAO":
            if self.value == 'E':
                return [x[0] and y[0], "CONDICAO"]
            if self.value == 'OU':
                return [x[0] or y[0], "CONDICAO"]
            if self.value=="=":
                if ((x[0]==y[0])):
                    return [True,"CONDICAO"]
                else:
                    return [False,"CONDICAO"]

        raise Exception("Can't operate with two different types")

class UnOp(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        if self.children[0].Evaluate(table)[1] == "INTEIRO":
            if self.value=="+":
                return [(+self.children[0].Evaluate(table)[0]),"INTEIRO"]
            if self.value=="-":
                return [(-self.children[0].Evaluate(table)[0]),"INTEIRO"]

        if self.children[0].Evaluate(table)[1] == "CONDICAO":
            if self.value == 'NEGA':
                return [not (self.children[0].Evaluate(table)[0]), "CONDICAO"]
        raise Exception("Type is not correct")

class IntVal(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        return [self.value, "INTEIRO"]

class NoOp(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children

class IdentifierNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children

    def Evaluate(self,table):
        return (table.get_value(self.value))

class AssigmentOp(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        if self.children[0].value not in table.table:
            raise Exception("The variable is not declared")
        x=self.children[0].value
        y=self.children[1].Evaluate(table)
        if table.table[x][1]==y[1]:
            table.set_value(x, y[0])
        else:
            raise Exception("The type of the value is not the type of the variable")

class TypeNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        return self.value

class PrintNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        print(self.children[0].Evaluate(table)[0])

class StatementsNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        for i in self.children:
            i.Evaluate(table)

class WhileNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        if self.children[0].Evaluate(table)[1]!="CONDICAO":
            raise Exception("Type must be CONDICAO")
        while self.children[0].Evaluate(table)[0]:
            self.children[1].Evaluate(table)

class IfNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        if self.children[0].Evaluate(table)[1]!="CONDICAO":
            raise Exception("Type must be CONDICAO")
        if self.children[0].Evaluate(table)[0]:
            self.children[1].Evaluate(table)
        else:
            if len(self.children) == 3:
                self.children[2].Evaluate(table)

class InputNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        return [int(input()), "INTEIRO"]

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):
        table.set_type(self.children[0].value, self.children[1].value)

class BooleanVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):
        return [self.value, "CONDICAO"]

class SubDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):
        if self.value in table.table:
            raise Exception("The variable is already declared")
        table.set_type(self.value,"ROTINA")
        table.set_value(self.value,self)
        

class FuncDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        if self.value in table.table:
            raise Exception("The variable is already declared")
        table.set_type(self.value,"FUNCAO")
        table.set_value(self.value,self)

class Call(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        #recupera no do ST, get symbol
        #evaluate de todos filhos
        #da o setter nos argumentos
        #evaluate no ultimo filho
        #retorna via o nome
        dec=table.get_value2(self.value)[0] #no func ou sub
        tipo=table.get_value2(self.value)[1] #tipo do no, func ou sub
        new_table=SymbolTable(table)
        init=0
        if tipo=="FUNCAO":
            new_table.table[self.value] =  [None, dec.children[0].Evaluate(table)]
            init=1
        j=0
        for i in range(init, len(dec.children)-1):
            dec.children[i].Evaluate(new_table)
            argument=self.children[j].Evaluate(table)
            argument_value=argument[0]
            argument_type=argument[1]
            parameter_type=dec.children[i].children[1].Evaluate(table)  #new_table.get_value(argument_type)
            if argument_type!=parameter_type:
                raise Exception("tipos errados")
            j+=1
            new_table.set_value(dec.children[i].children[0].value,argument_value)
        if (j) != len(self.children):
            raise Exception("quantidade de argumentos distintos")
        dec.children[-1].Evaluate(new_table)
        if tipo=="FUNCAO":
            return new_table.get_value(self.value)