from token import *
from tokenizer import *
from prePro import *
from node import *

class Parser:
    
    def parseProgram():
        children=[]
        while Parser.tokens.actual.type!='EOF':
            if Parser.tokens.actual.type=='ROTINA':
                res=Parser.parseSubDec()
                children.append(res)
            if Parser.tokens.actual.type=='FUNCAO':
                res=Parser.parseFuncDec()
                children.append(res)
            while Parser.tokens.actual.type=='BREAK':
                t=Parser.tokens.selectNext()
        children.append(Call("MAIN",[]))
        return StatementsNode("root",children)

    def parseSubDec():
        if Parser.tokens.actual.type=='ROTINA':
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type=='IDENTIFIER':
                name= Parser.tokens.actual.value
                t=Parser.tokens.selectNext()
                if Parser.tokens.actual.type=='OPEN_PAR':
                    t=Parser.tokens.selectNext()
                    children=[]
                    while Parser.tokens.actual.type=='COMMA' or Parser.tokens.actual.type!='CLOSE_PAR':
                        if Parser.tokens.actual.type=='COMMA':
                            t=Parser.tokens.selectNext()
                            if Parser.tokens.actual.type=='IDENTIFIER':
                                variavel=IdentifierNode(Parser.tokens.actual.value,[])
                                t=Parser.tokens.selectNext()
                                if Parser.tokens.actual.type=='COMO':
                                    t=Parser.tokens.selectNext()
                                    tipo=Parser.parseType()
                        else:
                            if Parser.tokens.actual.type=='IDENTIFIER':
                                variavel=IdentifierNode(Parser.tokens.actual.value,[])
                                t=Parser.tokens.selectNext()
                                if Parser.tokens.actual.type=='COMO':
                                    t=Parser.tokens.selectNext()
                                    tipo=Parser.parseType()
                        children.append(VarDec("vardec", [variavel, tipo]))
                    if Parser.tokens.actual.type=='CLOSE_PAR':
                        t=Parser.tokens.selectNext()
                        if Parser.tokens.actual.type=='BREAK':
                            t=Parser.tokens.selectNext()
                            list_of_children=[]
                            while Parser.tokens.actual.type!='FIM':
                                list_of_children.append(Parser.parseStatement())
                                if Parser.tokens.actual.type=='BREAK':
                                    t=Parser.tokens.selectNext()
                            t=Parser.tokens.selectNext()
                            if Parser.tokens.actual.type=='ROTINA':
                                t=Parser.tokens.selectNext()
                                stmnts = StatementsNode("STATEMENTS",list_of_children)
                                children.append(stmnts)
                                return SubDec(name,children)

                            else:
                                raise Exception("Must insert a ROTINA at the end.")
                        else:
                            raise Exception("Must break line.")
                    else:
                        raise Exception("Must close parenthesis.")
                else:
                    raise Exception("Must open parenthesis.")
            else:
                raise Exception("Must insert IDENTIFIER in the begin.")
        else:
            raise Exception("Must insert ROTINA in the begin.")


    def parseFuncDec():
        if Parser.tokens.actual.type=='FUNCAO':
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type=='IDENTIFIER':
                name= Parser.tokens.actual.value
                t=Parser.tokens.selectNext()
                if Parser.tokens.actual.type=='OPEN_PAR':
                    t=Parser.tokens.selectNext()
                    children=[]
                    while Parser.tokens.actual.type=='COMMA' or Parser.tokens.actual.type!='CLOSE_PAR':
                        if Parser.tokens.actual.type=='COMMA':
                            t=Parser.tokens.selectNext()
                            if Parser.tokens.actual.type=='IDENTIFIER':
                                variavel=IdentifierNode(Parser.tokens.actual.value,[])
                                t=Parser.tokens.selectNext()
                                if Parser.tokens.actual.type=='COMO':
                                    t=Parser.tokens.selectNext()
                                    tipo=Parser.parseType()
                                else:
                                    raise Exception("Must declare type")
                        else:
                            if Parser.tokens.actual.type=='IDENTIFIER':
                                variavel=IdentifierNode(Parser.tokens.actual.value,[])
                                t=Parser.tokens.selectNext()
                                if Parser.tokens.actual.type=='COMO':
                                    t=Parser.tokens.selectNext()
                                    tipo=Parser.parseType()
                                else:
                                    raise Exception("Must declare type")
                        children.append(VarDec("vardec", [variavel, tipo]))
                    if Parser.tokens.actual.type=='CLOSE_PAR':
                        t=Parser.tokens.selectNext()
                        if Parser.tokens.actual.type=='COMO':
                            t=Parser.tokens.selectNext()
                            tipo=Parser.parseType()
                            children.insert(0, tipo)
                            if Parser.tokens.actual.type=='BREAK':
                                t=Parser.tokens.selectNext()
                                list_of_children=[]
                                while Parser.tokens.actual.type!='FIM':
                                    list_of_children.append(Parser.parseStatement())
                                    if Parser.tokens.actual.type=='BREAK':
                                        t=Parser.tokens.selectNext()
                                t=Parser.tokens.selectNext()
                                if Parser.tokens.actual.type=='FUNCAO':
                                    t=Parser.tokens.selectNext()
                                    stmnts = StatementsNode("STATEMENTS",list_of_children)
                                    children.append(stmnts)
                                    return FuncDec(name,children)

                                else:
                                    raise Exception("Must insert a ROTINA at the end.")
                            else:
                                raise Exception("Must break line.")
                    else:
                        raise Exception("Must close parenthesis.")
                else:
                    raise Exception("Must open parenthesis.")
            else:
                raise Exception("Must insert IDENTIFIER in the begin.")
        else:
            raise Exception("Must insert FUNCTIONTION in the begin.")


    def parseStatement():
        if Parser.tokens.actual.type=='IDENTIFIER':
            variavel=IdentifierNode(Parser.tokens.actual.value,[])
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type=='EQUAL':
                t=Parser.tokens.selectNext()
                return AssigmentOp("=",[variavel,Parser.parseRelExpression()])
            else:
                raise Exception("Must define a value for the variable.")


        if Parser.tokens.actual.type=='IMPRIMI':
            t=Parser.tokens.selectNext()
            return PrintNode("IMPRIMI",[Parser.parseRelExpression()])


        if Parser.tokens.actual.type=='SE':
            children=[]
            t=Parser.tokens.selectNext()
            condicao=Parser.parseRelExpression()
            children.append(condicao)
            if Parser.tokens.actual.type=='ENTAO':
                t=Parser.tokens.selectNext()
                if Parser.tokens.actual.type=='BREAK':
                    t=Parser.tokens.selectNext()
                    verdade=[]
                    while Parser.tokens.actual.type!='FIM' and Parser.tokens.actual.type!='SENAO':
                        verdade.append(Parser.parseStatement())
                        if Parser.tokens.actual.type=='BREAK':
                            t=Parser.tokens.selectNext()
                    verdades=StatementsNode("STATEMENTS",verdade)
                    children.append(verdades)
                    if Parser.tokens.actual.type=='SENAO':
                        t=Parser.tokens.selectNext()
                        if Parser.tokens.actual.type=='BREAK':
                            t=Parser.tokens.selectNext()
                            mentira=[]
                            while Parser.tokens.actual.type!='FIM':
                                mentira.append(Parser.parseStatement())
                                if Parser.tokens.actual.type=='BREAK':
                                    t=Parser.tokens.selectNext()
                            mentiras=StatementsNode("STATEMENTS",mentira)
                            children.append(mentiras)                                
                    if Parser.tokens.actual.type=='FIM':
                        t=Parser.tokens.selectNext()
                        if Parser.tokens.actual.type=='SE':
                            t=Parser.tokens.selectNext()
                            return IfNode("IF",children)


        if Parser.tokens.actual.type=='ENQUANTO':
            t=Parser.tokens.selectNext()
            condicao=Parser.parseRelExpression()
            if Parser.tokens.actual.type=='BREAK':
                t=Parser.tokens.selectNext()
                verdade=[]
                while Parser.tokens.actual.type!='FIM_ENQUANTO':
                    verdade.append(Parser.parseStatement())
                    if Parser.tokens.actual.type=='BREAK':
                        t=Parser.tokens.selectNext()
                verdades=StatementsNode("STATEMENTS",verdade)
                if Parser.tokens.actual.type=='FIM_ENQUANTO':
                    t=Parser.tokens.selectNext()
                    return WhileNode("WHILE",[condicao,verdades])
        

        if Parser.tokens.actual.type=='DECLARAR':
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type=='IDENTIFIER':
                variavel=IdentifierNode(Parser.tokens.actual.value,[])
                t=Parser.tokens.selectNext()
                if Parser.tokens.actual.type=='COMO':
                    t=Parser.tokens.selectNext()
                    tipo=Parser.parseType()
                    return VarDec("vardec", [variavel, tipo])


        if Parser.tokens.actual.type == 'FACA':
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'IDENTIFIER':
                variavel = Parser.tokens.actual.value
                t=Parser.tokens.selectNext()
                if Parser.tokens.actual.type == 'OPEN_PAR':
                    t=Parser.tokens.selectNext()
                    children = []
                    while Parser.tokens.actual.type != 'CLOSE_PAR':
                        if Parser.tokens.actual.type == 'COMMA':
                            t=Parser.tokens.selectNext()
                            children.append(Parser.parseRelExpression())
                        else:
                            children.append(Parser.parseRelExpression())
                    if Parser.tokens.actual.type == 'CLOSE_PAR':
                        Parser.tokens.selectNext()
                        return Call(variavel, children)
        else:
            return NoOp(None,None)
        

    def parseRelExpression():
        res=Parser.parseExpression()
        if Parser.tokens.actual.type=='EQUAL':
            t=Parser.tokens.selectNext()
            res = BinOp("=",[res,Parser.parseExpression()])
        elif Parser.tokens.actual.type=='BIGGER':
            t=Parser.tokens.selectNext()
            res = BinOp(">",[res,Parser.parseExpression()])
        elif Parser.tokens.actual.type=='SMALLER':
            t=Parser.tokens.selectNext()
            res = BinOp("<",[res,Parser.parseExpression()])
        return res

    def parseExpression():
        res=Parser.parseTerm()
        while Parser.tokens.actual.type=='PLUS' or Parser.tokens.actual.type=='MINUS' or Parser.tokens.actual.type=='OU':
            if Parser.tokens.actual.type=='PLUS':
                t=Parser.tokens.selectNext()
                res = BinOp("+",[res,Parser.parseTerm()])
            elif Parser.tokens.actual.type=='MINUS':
                t=Parser.tokens.selectNext()
                res = BinOp("-",[res,Parser.parseTerm()])
            elif Parser.tokens.actual.type=='OU':
                t=Parser.tokens.selectNext()
                res = BinOp("OU",[res,Parser.parseTerm()])
        return res

    def parseTerm():
        res=Parser.parseFactor()
        while Parser.tokens.actual.type=='MULT' or Parser.tokens.actual.type=='DIV' or Parser.tokens.actual.type=='E':    
            if Parser.tokens.actual.type=='DIV':
                t=Parser.tokens.selectNext()
                res = BinOp("/",[res,Parser.parseFactor()])
            elif Parser.tokens.actual.type=='MULT':
                t=Parser.tokens.selectNext()
                res = BinOp("*",[res,Parser.parseFactor()])
            elif Parser.tokens.actual.type=='E':
                t=Parser.tokens.selectNext()
                res = BinOp("E",[res,Parser.parseFactor()])
        return res

    def parseFactor():
        if Parser.tokens.actual.type=='INT':
            res=IntVal(Parser.tokens.actual.value,[])
            t=Parser.tokens.selectNext()
            return res
        elif Parser.tokens.actual.type == 'VERDADEIRO' or Parser.tokens.actual.type == 'FALSO':
            res = BooleanVal(Parser.tokens.actual.value, [])
            t = Parser.tokens.selectNext()
            return res
        elif Parser.tokens.actual.type=='INPUT':
            res = InputNode(Parser.tokens.actual.value, [])
            t=Parser.tokens.selectNext()
            return res
        elif Parser.tokens.actual.type=='IDENTIFIER':
            variavel = Parser.tokens.actual.value
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type=="OPEN_PAR":
                t=Parser.tokens.selectNext()
                children=[]
                while Parser.tokens.actual.type != 'CLOSE_PAR':
                    if Parser.tokens.actual.type == 'COMMA':
                        t=Parser.tokens.selectNext()
                        children.append(Parser.parseRelExpression())
                    else:
                        children.append(Parser.parseRelExpression())
                if Parser.tokens.actual.type == 'CLOSE_PAR':
                    Parser.tokens.selectNext()
                    return Call(variavel, children)
            res=IdentifierNode(variavel,[])
            return res
        elif Parser.tokens.actual.type=='PLUS':
            t=Parser.tokens.selectNext()
            res=UnOp("+",[Parser.parseFactor()])
            return res
        elif Parser.tokens.actual.type=='MINUS':
            t=Parser.tokens.selectNext()
            res=UnOp("-",[Parser.parseFactor()])
            return res
        elif Parser.tokens.actual.type=='PLUS':
            t=Parser.tokens.selectNext()
            res=UnOp("+",[Parser.parseFactor()])
            return res
        elif Parser.tokens.actual.type=='OPEN_PAR':
            t=Parser.tokens.selectNext()
            res=Parser.parseRelExpression()
            if Parser.tokens.actual.type=='CLOSE_PAR':
                t=Parser.tokens.selectNext()
                return res
            else:
                raise Exception("Didn't close parenthesis. ")
        elif Parser.tokens.actual.type=='NEGA':
            t = Parser.tokens.selectNext()
            return UnOp("NEGA", [Parser.parseFactor()])
        else:
            raise Exception("Unexpected token.")


    def parseType():
        if Parser.tokens.actual.type=="INTEIRO":
            t=Parser.tokens.selectNext()
            return TypeNode('INTEIRO', [])
        if Parser.tokens.actual.type=="CONDICAO":
            t=Parser.tokens.selectNext()
            return TypeNode('CONDICAO', [])


    def run(code):
        code=PrePro.filter(code)
        Parser.tokens=Tokenizer(code)
        t=Parser.tokens.selectNext()
        res=Parser.parseProgram()

        while Parser.tokens.actual.type == "BREAK":
            Parser.tokens.selectNext()

        if Parser.tokens.actual.type == 'EOF':
            return res
        else:
            raise Exception("Unexpected token.")