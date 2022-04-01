
class SyntaxError(Exception):
    def __init__(self, message, status):
        super().__init__(message, status)
        self.message = message
        self.status = status

class TreeNode:
    def __init__(self):
        self.child = []
        self.sibling = None
        self.lineno = None
        self.nodekind = None
        self.kind = None
        self.kind.dec = None
        self.kind.stmt = None
        self.kind.exp = None
        self.idnum = None
        self.name = []
        self.table = []
        self.type_name = []
        self.attr = self.attr()

    class attr:
        def __init__(self):
            self.ArrayAttr = None
            self.ArrayAttr.low = None
            self.ArrayAttr.up = None
            self.ArrayAttr.childType = None
            self.procAttr = None
            self.procAttr.paramt = None
            self.ExpAttr = None
            self.ExpAttr.op = None
            self.ExpAttr.val = None
            self.ExpAttr.varkind = None
            self.ExpAttr.type = None

class Parser:
    def __init__(self, tokenlist):
        self.tokenlist = tokenlist
        self.idx = 0
        self.temp_name = None

    def match(self, terminator):
        if self.tokenlist[self.idx][2] != terminator:
            # raise SyntaxError("Syntax Error detected at line {}".format(self.tokenlist[self.idx][0]), -1)
            self.syntaxError()
        self.idx += 1
        return

    def syntaxError(self, message=None):
        if message:
            raise SyntaxError(message, -1)
        else:
            raise SyntaxError(
                'Syntax Error detected at line {}, near "{}"'.format(
                    self.tokenlist[self.idx][0], self.tokenlist[self.idx][2]), -1)

    def parse(self) -> TreeNode:
        root = self.Program()
        self.match("EOF")
        return root

    def Program(self) -> TreeNode:
        if 'PROGRAM' == self.tokenlist[self.idx][2]:
            root = TreeNode()
            root.child[0] = self.ProgramHead()
            root.child[1] = self.DeclarePart()
            root.child[2] = self.ProgramBody()
            self.match(".")
            return root
        else:
            self.syntaxError()

    def ProgramHead(self) -> TreeNode:
        if 'PROGRAM' == self.tokenlist[self.idx][2]:
            t = TreeNode()
            self.match("PROGRAM")
            if 'ID' == self.tokenlist[self.idx][1]:
                t.name.append(self.tokenlist[self.idx][2])
                self.idx += 1
                return t
        self.syntaxError()

    def DeclarePart(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['PROCEDURE', 'TYPE', 'VAR', 'BEGIN']:
            pp = None
            typeP = TreeNode()
            typeP.child[0] = self.TypeDec()
            varP = TreeNode()
            varP.child[0] = self.VarDec()
            s = self.ProcDec()
            if not varP.child[0]:
                varP = s
            if not typeP.child[0]:
                pp = typeP = varP
            if typeP != varP:
                typeP.sibling = varP
            if varP != s:
                varP.sibling = s
            return pp
        else:
            self.syntaxError()

    def TypeDec(self):
        if self.tokenlist[self.idx][2] in ['TYPE']:
            return self.TypeDeclaration()
        elif self.tokenlist[self.idx][2] in ['PROCEDURE', 'VAR', 'BEGIN']:
            return None
        else:
            self.syntaxError()

    def TypeDeclaration(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['TYPE']:
            self.match("TYPE")
            return self.TypeDecList()
        else:
            self.syntaxError()

    def TypeDecList(self) -> TreeNode:
        if self.tokenlist[self.idx][1] == 'ID':
            t = TreeNode()
            self.TypeId(t)
            self.match("=")
            self.TypeName(t)
            self.match(";")
            p = self.TypeDecMore()
            if p:
                t.sibling = p
            return t
        else:
            self.syntaxError()

    def TypeDecMore(self):
        if self.tokenlist[self.idx][1] == 'ID':
            return self.TypeDecList()
        elif self.tokenlist[self.idx][2] in ['PROCEDURE', 'VAR', 'BEGIN']:
            return None
        else:
            self.syntaxError()

    def TypeId(self, TreeNode):
        if self.tokenlist[self.idx][1] == 'ID':
            TreeNode.name.append(self.tokenlist[self.idx][2])
            self.idx += 1
        else:
            self.syntaxError()

    def TypeName(self, TreeNode):
        if self.tokenlist[self.idx][2] in ['INTEGER', 'CHAR']:
            self.BaseType(TreeNode)
        elif self.tokenlist[self.idx][2] in ['ARRAY', 'RECORD']:
            self.StructureType(TreeNode)
        elif self.tokenlist[self.idx][1] == 'ID':
            TreeNode.kind.dec = "IdK"
            TreeNode.type_name[0] = self.tokenlist[self.idx][2]
            self.idx += 1
        else:
            self.syntaxError()

    def BaseType(self, TreeNode):
        if self.tokenlist[self.idx][2] in ['INTEGER']:
            self.match("INTEGER")
            TreeNode.kind.dec = "IntegerK"
        elif self.tokenlist[self.idx][2] in ['CHAR']:
            self.match("CHAR")
            TreeNode.kind.dec = "CharK"
        else:
            self.syntaxError()

    def StructureType(self, TreeNode):
        if self.tokenlist[self.idx][2] in ['ARRAY']:
            self.ArrayType(TreeNode)
        elif self.tokenlist[self.idx][2] in ['RECORD']:
            TreeNode.kind.dec = "RecordK"
            self.RecordType(TreeNode)
        else:
            self.syntaxError()

    def ArrayType(self, TreeNode):
        if self.tokenlist[self.idx][2] in ['ARRAY']:
            self.match("ARRAY")
            self.match("[")
            if self.tokenlist[self.idx][1] in ['INTC']:
                TreeNode.attr.ArrayAttr.low = int(self.tokenlist[self.idx][2])
                self.idx += 1
                self.match("..")
                if self.tokenlist[self.idx][1] in ['INTC']:
                    TreeNode.attr.ArrayAttr.up = int(self.tokenlist[self.idx][2])
                    self.idx += 1
                    self.match("]")
                    self.match("OF")
                    self.BaseType(TreeNode)
                    TreeNode.attr.ArrayAttr.childType = TreeNode.kind.dec
                    TreeNode.kind.dec = "ArrayK"
                    return
        self.syntaxError()

    def RecordType(self, TreeNode):
        if self.tokenlist[self.idx][2] in ['RECORD']:
            self.match("RECORD")
            p = self.FieldDecList()
            TreeNode.child[0] = p
            self.match("END")
        else:
            self.syntaxError()

    def FieldDecList(self) -> TreeNode:
        t = TreeNode()
        if self.tokenlist[self.idx][2] in ['INTEGER', 'CHAR']:
            self.BaseType(t)
        elif self.tokenlist[self.idx][2] in ['ARRAY']:
            self.ArrayType(t)
        else:
            self.syntaxError()
        self.IdList(t)
        self.match(";")
        p = self.FieldDecMore()
        t.sibling = p
        return t

    def FieldDecMore(self):
        if self.tokenlist[self.idx][2] in ['END']:
            return None
        elif self.tokenlist[self.idx][2] in ['ARRAY', 'INTEGER', 'CHAR']:
            return self.FieldDecList()
        else:
            self.syntaxError()

    def IdList(self, TreeNode):
        if self.tokenlist[self.idx][1] == 'ID':
            TreeNode.name.append(self.tokenlist[self.idx][2])
            self.idx += 1
            self.IdMore(TreeNode)
        else:
            self.syntaxError()

    def IdMore(self, TreeNode):
        if self.tokenlist[self.idx][2] in [';']:
            return
        elif self.tokenlist[self.idx][2] in [',']:
            self.match(",")
            self.IdList(TreeNode)
        else:
            self.syntaxError()

    def VarDec(self):
        if self.tokenlist[self.idx][2] in ['PROCEDURE', 'BEGIN']:
            return None
        elif self.tokenlist[self.idx][2] in ['VAR']:
            return self.VarDeclaration()
        else:
            self.syntaxError()

    def VarDeclaration(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['VAR']:
            self.match("VAR")
            return self.VarDecList()
        else:
            self.syntaxError()

    def VarDecList(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['ARRAY', 'INTEGER', 'RECORD', 'ID', 'CHAR']:
            t = TreeNode()
            self.TypeName(t)
            self.VarIdList(t)
            self.match(";")
            t.sibling = self.VarDecMore()
            return t
        else:
            self.syntaxError()

    def VarDecMore(self):
        if self.tokenlist[self.idx][2] in ['PROCEDURE', 'BEGIN']:
            return None
        elif self.tokenlist[self.idx][2] in ['ARRAY', 'INTEGER', 'RECORD', 'ID', 'CHAR']:
            return self.VarDecList()
        else:
            self.syntaxError()

    def VarIdList(self, TreeNode):
        if self.tokenlist[self.idx][1] == 'ID':
            TreeNode.name.append(self.tokenlist[self.idx][2])
            self.idx += 1
            self.VarIdMore(TreeNode)
        else:
            self.syntaxError()

    def VarIdMore(self, TreeNode):
        if self.tokenlist[self.idx][2] in [';']:
            return
        elif self.tokenlist[self.idx][2] in [',']:
            self.match(",")
            self.VarIdList(TreeNode)
        else:
            self.syntaxError()

    def ProcDec(self):
        if self.tokenlist[self.idx][2] in ['BEGIN']:
            return
        elif self.tokenlist[self.idx][2] in ['PROCEDURE']:
            return self.ProcDeclaration()
        else:
            self.syntaxError()

    def ProcDeclaration(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['PROCEDURE']:
            self.match("PROCEDURE")
            if self.tokenlist[self.idx][1] == 'ID':
                t = TreeNode()
                t.name.append(self.tokenlist[self.idx][2])
                self.idx += 1
                self.match("(")
                self.ParamList(t)
                self.match(")")
                self.match(";")
                t.child[1] = self.ProcDecPart()
                t.child[2] = self.ProcBody()
                t.sibling = self.ProcDecMore()
                return t
        self.syntaxError()

    def ProcDecMore(self):
        if self.tokenlist[self.idx][2] in ['BEGIN']:
            return None
        elif self.tokenlist[self.idx][2] in ['PROCEDURE']:
            return self.ProcDeclaration()
        else:
            self.syntaxError()

    def ParamList(self, TreeNode):
        if self.tokenlist[self.idx][2] in [')']:
            return
        elif self.tokenlist[self.idx][2] in ['CHAR', 'INTEGER', 'RECORD', 'ID', 'VAR', 'ARRAY']:
            TreeNode.child[0] = self.ParamDecList()
        else:
            self.syntaxError()

    def ParamDecList(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['CHAR', 'INTEGER', 'RECORD', 'ID', 'VAR', 'ARRAY']:
            t = self.Param()
            p = self.ParamMore()
            t.sibling = p
            return t
        else:
            self.syntaxError()

    def ParamMore(self):
        if self.tokenlist[self.idx][2] in [')']:
            return None
        elif self.tokenlist[self.idx][2] in [';']:
            self.match(";")
            return self.ParamDecList()
        else:
            self.syntaxError()

    def Param(self) -> TreeNode:
        t = TreeNode()
        if self.tokenlist[self.idx][2] in ['CHAR', 'INTEGER', 'RECORD', 'ID', 'ARRAY']:
            t.attr.ArrayAttr.paramt = "valparamType"
        elif self.tokenlist[self.idx][2] in ['VAR']:
            self.match("VAR")
            t.attr.ArrayAttr.paramt = "varparamType"
        else:
            self.syntaxError()
        self.TypeName(t)
        self.FormList(t)
        return t

    def FormList(self, TreeNode):
        if self.tokenlist[self.idx][1] == 'ID':
            TreeNode.name.append(self.tokenlist[self.idx][2])
            self.idx += 1
            self.FidMore(TreeNode)
        else:
            self.syntaxError()

    def FidMore(self, TreeNode):
        if self.tokenlist[self.idx][2] in [')', ';']:
            return
        elif self.tokenlist[self.idx][2] in [',']:
            self.match(",")
            self.FormList(TreeNode)
        else:
            self.syntaxError()

    def ProcDecPart(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['TYPE', 'BEGIN', 'PROCEDURE', 'VAR']:
            return self.DeclarePart()
        else:
            self.syntaxError()

    def ProcBody(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['BEGIN']:
            return self.ProgramBody()
        else:
            self.syntaxError()

    def ProgramBody(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['BEGIN']:
            self.match("BEGIN")
            t = TreeNode()
            t.child[0] = self.StmList()
            self.match("END")
            return t
        else:
            self.syntaxError()

    def StmList(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['WHILE', 'RETURN', 'IF', 'ID', 'READ', 'WRITE']:
            t = self.Stm()
            p = self.StmMore()
            t.sibling = p
            return t
        else:
            self.syntaxError()

    def StmMore(self):
        if self.tokenlist[self.idx][2] in ['ENDWH', 'ELSE', 'FI', 'END']:
            return None
        elif self.tokenlist[self.idx][2] in [';']:
            self.match(";")
            return self.StmList()
        else:
            self.syntaxError()

    def Stm(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['IF']:
            return self.ConditionalStm()
        elif self.tokenlist[self.idx][2] in ['WHILE']:
            return self.LoopStm()
        elif self.tokenlist[self.idx][2] in ['RETURN']:
            return self.ReturnStm()
        elif self.tokenlist[self.idx][2] in ['READ']:
            return self.InputStm()
        elif self.tokenlist[self.idx][2] in ['WRITE']:
            return self.OutputStm()
        elif self.tokenlist[self.idx][1] == ['ID']:
            self.temp_name = self.tokenlist[self.idx][2]
            self.idx += 1
            return self.AssCall()
        else:
            self.syntaxError()

    def AssCall(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['.', ':=', '[']:
            return self.AssignmentRest()
        elif self.tokenlist[self.idx][2] in ['(']:
            return self.CallStmRest()
        else:
            self.syntaxError()

    def AssignmentRest(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['.', ':=', '[']:
            t = TreeNode()
            self.VariMore(t)
            self.match(":=")
            t.child[0] = self.Exp()
            t.name.append(self.temp_name)
            return t
        else:
            self.syntaxError()

    def InputStm(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['READ']:
            self.match("READ")
            self.match("(")
            if self.tokenlist[self.idx][1] == 'ID':
                t = TreeNode()
                t.name.append(self.tokenlist[self.idx][2])
                self.idx += 1
                self.match(")")
                return t
        self.syntaxError()

    def OutputStm(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['WRITE']:
            self.match("WRITE")
            self.match("(")
            t = TreeNode()
            t.child[0] = self.Exp()
            self.match(")")
            return t
        else:
            self.syntaxError()

    def ReturnStm(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['RETURN']:
            self.match("RETURN")
            self.match("(")
            t = TreeNode()
            t.child[0] = self.Exp()
            self.match(")")
            return t
        else:
            self.syntaxError()

    def CallStmRest(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['(']:
            self.match("(")
            t = TreeNode()
            t.child[0] = self.ActParamList()
            t.name.append(self.temp_name)
            self.match(")")
            return t
        else:
            self.syntaxError()

    def ActParamList(self):
        if self.tokenlist[self.idx][2] in [')']:
            return None
        elif self.tokenlist[self.idx][2] in ['INTC', 'ID', '(']:
            t = self.Exp()
            t.sibling = self.ActParamMore()
            return t
        else:
            self.syntaxError()

    def ActParamMore(self):
        if self.tokenlist[self.idx][2] in [')']:
            return None
        elif self.tokenlist[self.idx][2] in [',']:
            self.match(",")
            return self.ActParamList()
        else:
            self.syntaxError()

    def Factor(self) -> TreeNode:
        if self.tokenlist[self.idx][1] in ['INTC']:
            t = TreeNode()
            t.attr.ArrayAttr.val = int(self.tokenlist[self.idx][2])
            return t
        elif self.tokenlist[self.idx][1] in ['ID']:
            return self.Variable()
        elif self.tokenlist[self.idx][2] in ['(']:
            self.match("(")
            t = self.Exp()
            self.match(")")
            return t
        else:
            self.syntaxError()

    def Variable(self) -> TreeNode:
        if self.tokenlist[self.idx][1] == ['ID']:
            t = TreeNode()
            t.name.append(self.tokenlist[self.idx][2])
            t.lineno = self.tokenlist[self.idx][0]
            self.idx += 1
            self.VariMore(t)
            return t
        else:
            self.syntaxError()

    def VariMore(self, TreeNode):
        if self.tokenlist[self.idx][2] in [':=', 'THEN', ')', '<', '*', ',', ']', 'ELSE', '/', '=', ';', 'FI', 'END', 'ENDWH', '+', '-', 'DO']:
            return
        elif self.tokenlist[self.idx][2] in ['[']:
            self.match("[")
            TreeNode.child[0] = self.Exp()
            TreeNode.attr.ExpAttr.varkind = "ArrayMembV"
            TreeNode.child[0].attr.ExpAttr.varkind = "IdV"
            self.match("]")
        elif self.tokenlist[self.idx][2] in ['.']:
            self.match(".")
            TreeNode.child[0] = self.FieldVar()
            TreeNode.attr.ExpAttr.varkind = "FieldMembV"
            TreeNode.child[0].attr.ExpAttr.varkind = "IdV"
        else:
            self.syntaxError()

    def FieldVar(self) -> TreeNode:
        if self.tokenlist[self.idx][1] == ['ID']:
            t =TreeNode()
            t.name.append(self.tokenlist[self.idx][2])
            t.lineno = self.tokenlist[self.idx][0]
            self.idx += 1
            self.FieldVarMore(t)
            return t
        else:
            self.syntaxError()

    def FieldVarMore(self, TreeNode):
        if self.tokenlist[self.idx][2] in [':=', 'THEN', ')', '<', '*', ',', ']', 'ELSE', '/', '=', ';', 'FI', 'END', 'ENDWH', '+', '-', 'DO']:
            return
        elif self.tokenlist[self.idx][2] in ['[']:
            self.match("[")
            TreeNode.child[0] = self.Exp()
            TreeNode.child[0].attr.ExpAttr.varkind = "ArrayMembV"
            self.match("]")
        else:
            self.syntaxError()

    '''改动较大'''
    def ConditionalStm(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['IF']:
            self.match("IF")
            t = TreeNode()
            t.child[0] = self.RelExp()
            self.match("THEN")
            t.child[1] = self.StmList()
            self.match("ELSE")
            t.child[2] = self.StmList()
            self.match("FI")
            return t
        else:
            self.syntaxError()

    def LoopStm(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['WHILE']:
            self.match("WHILE")
            t = TreeNode()
            t.child[0] = self.RelExp()
            self.match("DO")
            t.child[1] = self.StmList()
            self.match("ENDWH")
            return t
        else:
            self.syntaxError()

    def RelExp(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['INTC', 'ID', '(']:
            t = TreeNode()
            t.child[0] = self.Exp()
            self.OtherRelE(t)
            return t
        else:
            self.syntaxError()

    def OtherRelE(self, TreeNode):
        if self.tokenlist[self.idx][2] in ['=', '<']:
            self.CmpOp(TreeNode)
            TreeNode.child[1] = self.Exp()
        else:
            self.syntaxError()

    def CmpOp(self, TreeNode):
        if self.tokenlist[self.idx][2] in ['<']:
            TreeNode.attr.ExpAttr.op = self.tokenlist[self.idx][2]
            self.match("<")
        elif self.tokenlist[self.idx][2] in ['=']:
            TreeNode.attr.ExpAttr.op = self.tokenlist[self.idx][2]
            self.match("=")
        else:
            self.syntaxError()

    def Exp(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['INTC', 'ID', '(']:
            t = TreeNode()
            t.child[0] = self.Term()
            t = self.OtherTerm(t)
            return t
        else:
            self.syntaxError()

    def OtherTerm(self, TreeNode) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['THEN', ')', '<', 'FI', ']', ',', 'END', 'ENDWH', 'ELSE', 'DO', '=', ';']:
            return TreeNode.child[0]
        elif self.tokenlist[self.idx][2] in ['+', '-']:
            self.AddOp(TreeNode)
            TreeNode.child[1] = self.Exp()
            return TreeNode
        else:
            self.syntaxError()

    def AddOp(self, TreeNode):
        if self.tokenlist[self.idx][2] in ['+']:
            TreeNode.attr.ExpAttr.op = self.tokenlist[self.idx][2]
            self.match("+")
        elif self.tokenlist[self.idx][2] in ['-']:
            TreeNode.attr.ExpAttr.op = self.tokenlist[self.idx][2]
            self.match("-")
        else:
            self.syntaxError()

    def Term(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['INTC', 'ID', '(']:
            t = TreeNode()
            t.child[0] = self.Factor()
            t = self.OtherFactor(t)
            return t
        else:
            self.syntaxError()

    def OtherFactor(self, TreeNode) -> TreeNode:
        if self.tokenlist[self.idx][2] in \
                ['THEN', ')', '<', 'FI', ']', ',', 'END', 'ENDWH', 'ELSE', 'DO', '=', ';', '+', '-']:
            return TreeNode.child[0]
        elif self.tokenlist[self.idx][2] in ['/', '*']:
            self.MultOp(TreeNode)
            TreeNode.child[1] = self.Term()
            return TreeNode
        else:
            self.syntaxError()

    def MultOp(self, TreeNode):
        if self.tokenlist[self.idx][2] in ['*']:
            TreeNode.attr.ExpAttr.op = self.tokenlist[self.idx][2]
            self.match("*")
        elif self.tokenlist[self.idx][2] in ['/']:
            TreeNode.attr.ExpAttr.op = self.tokenlist[self.idx][2]
            self.match("/")
        else:
            self.syntaxError()


if __name__ == '__main__':
    tokenlist = None
    parser = Parser(tokenlist)
    root = parser.parse()
