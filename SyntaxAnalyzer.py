"""
Top-down parsing
"""
from graphviz import Digraph
from utils import FormatTransformer


class SyntaxError(Exception):
    """
    自定义语法错误异常
    """
    def __init__(self, message, status):
        """
        语法错误信息
            message:错误具体信息
            status：状态，默认-1
        """
        super().__init__(message, status)
        self.message = message
        self.status = status


class TreeNode:
    """
    定义语法树节点
    """
    def __init__(self):
        """
        语法树节点结构
            child：list[] 语法树子节点，上下层关系
            sibling：TreeNode 语法树兄弟节点，平级关系
            lineno：int 行号
            nodekind：str 节点名
            kind：class 类型信息
            name：list[str] 变量标识符表
            type_name：list[] 类型标识符表
            attr：class 属性信息
        """
        self.child = [None] * 3
        self.sibling = None
        self.lineno = None
        self.nodekind = ""
        self.kind = self.kind()
        self.name = []
        self.type_name = [None]
        self.attr = self.attr()

    class kind:
        """
        类型信息
        """
        def __init__(self):
            """
            dec：声明类型
            stmt：语句类型
            exp：表达式类型
            """
            self.dec = None
            self.stmt = None
            self.exp = None

    class attr:
        """
        属性信息
        """
        def __init__(self):
            """
            ArrayAttr：数组属性
            ProcAttr：过程体属性
            ExpAttr：表达式属性
            """
            self.ArrayAttr = self.ArrayAttr()
            self.ProcAttr = self.ProcAttr()
            self.ExpAttr = self.ExpAttr()

        class ArrayAttr:
            def __init__(self):
                """
                low：下标
                low：上标
                childType：数组成员类型
                """
                self.low = None
                self.low = None
                self.childType = None

        class ProcAttr:
            def __init__(self):
                """
                paramt：参数属性（值参，变参）
                """
                self.paramt = None

        class ExpAttr:
            def __init__(self):
                """
                op：运算操作符
                val：常数值
                varkind：变量类别
                """
                self.op = None
                self.val = None
                self.varkind = None


class Parser:
    def __init__(self, tokenlist, idx=0):
        self.tokenlist = tokenlist
        self.idx = idx
        self.temp_name = None

    def match(self, terminator):
        """
        匹配终极符
        """
        if self.tokenlist[self.idx][2] != terminator:
            self.syntaxError()
        self.idx += 1
        return

    def syntaxError(self, message=None):
        """
        显示错误信息
        """
        # if message:
        #     raise SyntaxError(message, -1)
        # else:
        #     raise SyntaxError(
        #         'Syntax Error detected at line {}, "{}"'.format(
        #             self.tokenlist[self.idx][0], self.tokenlist[self.idx][2]), -1)
        message = 'Syntax Error detected at line {}, "{}"'.format(
            self.tokenlist[self.idx][0], self.tokenlist[self.idx][2])
        print('\033[1;31;40m')
        print('\033[7;31m{}\033[1;31;40m'.format(message))
        print('\033[0m')
        exit(0)

    def parse(self) -> TreeNode:
        """
        解析入口
            return：TreeNode 合法语法树根节点
        """
        root = self.Program()
        self.match("EOF")
        return root

    def Program(self) -> TreeNode:
        if 'PROGRAM' == self.tokenlist[self.idx][2]:
            root = TreeNode()
            root.nodekind = "ProK"
            root.child[0] = self.ProgramHead()
            root.child[1] = self.DeclarePart()
            root.child[2] = self.ProgramBody()
            self.match(".")
            return root
        else:
            self.syntaxError()

    '''递归下降程序对生成式进行了一点修改'''
    def ProgramHead(self) -> TreeNode:
        if 'PROGRAM' == self.tokenlist[self.idx][2]:
            t = TreeNode()
            t.nodekind = "PheadK"
            self.match("PROGRAM")
            if 'ID' == self.tokenlist[self.idx][1]:
                t.name.append(self.tokenlist[self.idx][2])
                self.idx += 1
                return t
        self.syntaxError()

    def DeclarePart(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['PROCEDURE', 'TYPE', 'VAR', 'BEGIN']:
            typeP = TreeNode()
            typeP.nodekind = "TypeK"
            typeP.child[0] = self.TypeDec()
            varP = TreeNode()
            varP.nodekind = "VarK"
            varP.child[0] = self.VarDec()
            s = TreeNode()
            s.nodekind = "ProcDecK"
            s.child[0] = self.ProcDec()
            if not s.child[0]:
                s = None
            if not varP.child[0]:
                varP = s
            if not typeP.child[0]:
                typeP = varP
            if typeP != varP:
                typeP.sibling = varP
            if varP != s:
                varP.sibling = s
            return typeP
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
            t.nodekind = "DecK"
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
            if self.tokenlist[self.idx][1] in ['CONST']:
                TreeNode.attr.ArrayAttr.low = int(self.tokenlist[self.idx][2])
                self.idx += 1
                self.match("..")
                if self.tokenlist[self.idx][1] in ['CONST']:
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
        t.nodekind = "DecK"
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
        if self.tokenlist[self.idx][2] in ['ARRAY', 'INTEGER', 'RECORD', 'CHAR'] \
                or self.tokenlist[self.idx][1] == 'ID':
            t = TreeNode()
            t.nodekind = "DecK"
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
        elif self.tokenlist[self.idx][2] in ['ARRAY', 'INTEGER', 'RECORD', 'CHAR'] \
                or self.tokenlist[self.idx][1] == 'ID':
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
            return None
        elif self.tokenlist[self.idx][2] in ['PROCEDURE']:
            return self.ProcDeclaration()
        else:
            self.syntaxError()

    def ProcDeclaration(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['PROCEDURE']:
            self.match("PROCEDURE")
            if self.tokenlist[self.idx][1] == 'ID':
                t = TreeNode()
                t.nodekind = "DecK"
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
        elif self.tokenlist[self.idx][2] in ['CHAR', 'INTEGER', 'RECORD', 'VAR', 'ARRAY'] \
                or self.tokenlist[self.idx][1] == 'ID':
            TreeNode.child[0] = self.ParamDecList()
        else:
            self.syntaxError()

    def ParamDecList(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['CHAR', 'INTEGER', 'RECORD', 'VAR', 'ARRAY'] \
                or self.tokenlist[self.idx][1] == 'ID':
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
        t.nodekind = "DecK"
        if self.tokenlist[self.idx][2] in ['CHAR', 'INTEGER', 'RECORD', 'ARRAY'] \
                or self.tokenlist[self.idx][1] == 'ID':
            t.attr.ProcAttr.paramt = "valparamType"
        elif self.tokenlist[self.idx][2] in ['VAR']:
            self.match("VAR")
            t.attr.ProcAttr.paramt = "varparamType"
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
            t.nodekind = "StmLK"
            t.child[0] = self.StmList()
            self.match("END")
            return t
        else:
            self.syntaxError()

    def StmList(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['WHILE', 'RETURN', 'IF', 'READ', 'WRITE'] \
                or self.tokenlist[self.idx][1] == 'ID':
            t = self.Stm()
            t.nodekind = "StmtK"
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
        elif self.tokenlist[self.idx][1] == 'ID':
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
            t.kind.stmt = "AssignK"
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
                t.kind.stmt = "ReadK"
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
            t.kind.stmt = "WriteK"
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
            t.kind.stmt = "ReturnStm"
            t.child[0] = self.Exp()
            self.match(")")
            return t
        else:
            self.syntaxError()

    def CallStmRest(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['(']:
            self.match("(")
            t = TreeNode()
            t.nodekind = "CallK"
            t.child[0] = self.ActParamList()
            t.name.append(self.temp_name)
            self.match(")")
            return t
        else:
            self.syntaxError()

    def ActParamList(self):
        if self.tokenlist[self.idx][2] in [')']:
            return None
        elif self.tokenlist[self.idx][2] in ['('] \
                or self.tokenlist[self.idx][1] in ['ID', 'CONST']:
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
        if self.tokenlist[self.idx][1] == 'CONST':
            t = TreeNode()
            t.nodekind = "ExpK"
            t.kind.exp = "ConstK"
            t.attr.ExpAttr.val = int(self.tokenlist[self.idx][2])
            self.idx += 1
            return t
        elif self.tokenlist[self.idx][1] == 'ID':
            return self.Variable()
        elif self.tokenlist[self.idx][2] in ['(']:
            self.match("(")
            t = self.Exp()
            self.match(")")
            return t
        else:
            self.syntaxError()

    def Variable(self) -> TreeNode:
        if self.tokenlist[self.idx][1] == 'ID':
            t = TreeNode()
            t.nodekind = "ExpK"
            t.kind.exp = "IdK"
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
        if self.tokenlist[self.idx][1] == 'ID':
            t = TreeNode()
            t.nodekind = "ExpK"
            t.kind.exp = "IdK"
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
            t.kind.stmt = "IfK"
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
            t.kind.stmt = "WhileK"
            t.child[0] = self.RelExp()
            self.match("DO")
            t.child[1] = self.StmList()
            self.match("ENDWH")
            return t
        else:
            self.syntaxError()

    def RelExp(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['('] \
                or self.tokenlist[self.idx][1] in ['ID', 'CONST']:
            t = TreeNode()
            t.nodekind = "ExpK"
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
            TreeNode.kind.exp = "OpK"
            self.match("<")
        elif self.tokenlist[self.idx][2] in ['=']:
            TreeNode.attr.ExpAttr.op = self.tokenlist[self.idx][2]
            TreeNode.kind.exp = "OpK"
            self.match("=")
        else:
            self.syntaxError()

    def Exp(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['('] \
                or self.tokenlist[self.idx][1] in ['ID', 'CONST']:
            t = TreeNode()
            t.nodekind = "ExpK"
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
            TreeNode.kind.exp = "OpK"
            self.match("+")
        elif self.tokenlist[self.idx][2] in ['-']:
            TreeNode.attr.ExpAttr.op = self.tokenlist[self.idx][2]
            TreeNode.kind.exp = "OpK"
            self.match("-")
        else:
            self.syntaxError()

    def Term(self) -> TreeNode:
        if self.tokenlist[self.idx][2] in ['('] \
                or self.tokenlist[self.idx][1] in ['ID', 'CONST']:
            t = TreeNode()
            t.nodekind = "ExpK"
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
            TreeNode.kind.exp = "OpK"
            self.match("*")
        elif self.tokenlist[self.idx][2] in ['/']:
            TreeNode.attr.ExpAttr.op = self.tokenlist[self.idx][2]
            TreeNode.kind.exp = "OpK"
            self.match("/")
        else:
            self.syntaxError()


def ToStr(list):
    """
    列表转不带引号的字符串
    :param list: list[str]
    :return: str
    """
    s = ''
    for l in list[:-1]:
        s = s + str(l) + ","
    s += list[-1]
    return s


def decode(node):
    """
    解码树节点信息，输出信息串
    :param node: class 语法树节点
    :return: str
    """
    label = ''
    if node.nodekind != "":
        label = node.nodekind + "\n"
    if len(node.name) > 0:
        label = label + "ID=" + ToStr(node.name) + "\n"
    if node.type_name != [None]:
        label = label + "Type=" + ToStr(node.type_name) + "\n"
    if node.lineno:
        label = label + "lineNO=" + str(node.lineno) + "\n"
    if node.kind.dec:
        label = label + "kind.dec=" + node.kind.dec + "\n"
    if node.kind.stmt:
        label = label + "kind.stmt=" + node.kind.stmt + "\n"
    if node.kind.exp:
        label = label + "kind.exp=" + node.kind.exp + "\n"
    if node.attr.ArrayAttr.low:
        label = label + "ArrayAttr.low=" + str(node.attr.ArrayAttr.low) + "\n"
        label = label + "ArrayAttr.up=" + str(node.attr.ArrayAttr.up) + "\n"
    if node.attr.ArrayAttr.childType:
        label = label + "ArrayAttr.childType=" + node.attr.ArrayAttr.childType + "\n"
    if node.attr.ProcAttr.paramt:
        label = label + "ProcAttr.paramt=" + node.attr.ProcAttr.paramt + "\n"
    if node.attr.ExpAttr.op:
        label = label + "ExpAttr.op=" + node.attr.ExpAttr.op + "\n"
    if node.attr.ExpAttr.val:
        label = label + "ExpAttr.val=" + str(node.attr.ExpAttr.val) + "\n"
    if node.attr.ExpAttr.varkind:
        label = label + "ExpAttr.varkind=" + node.attr.ExpAttr.varkind + "\n"
    return label


def drawTree(graph, node):
    """
    绘制语法树
    :param node: 语法树节点
    :return: None
    """
    for i in range(3):
        if node.child[i]:
            graph.node(name=str(id(node.child[i])), label=decode(node.child[i]))
            xlabel = 'child[{}]'.format(i)
            graph.edge(tail_name=str(id(node)), head_name=str(id(node.child[i])), xlabel=xlabel, color='red')
            drawTree(graph, node.child[i])
    if node.sibling:
        with graph.subgraph() as s:
            # s.attr(rank='same')
            graph.node(name=str(id(node.sibling)), label=decode(node.sibling))
            s.edge(tail_name=str(id(node)), head_name=str(id(node.sibling)), xlabel="brother", color='blue')
        # graph.edge(tail_name=str(id(node)), head_name=str(id(node.sibling)))
        drawTree(graph, node.sibling)


if __name__ == '__main__':
    tokenlist1 = [(1, 'PROGRAM', 'Program'), (1, 'ID', 'p'), (2, 'TYPE', 'type'), (2, 'ID', 't'), (2, 'EQ', '='), (2, 'INTEGER', 'integer'), (2, 'SEMI', ';'), (2, 'ID', 't'), (2, 'EQ', '='), (2, 'CHAR', 'char'), (2, 'SEMI', ';'), (3, 'VAR', 'var'), (3, 'ID', 't'), (3, 'ID', 'v1'), (3, 'COMMA', ','), (3, 'ID', 'v2'), (3, 'COMMA', ','), (3, 'ID', 'v3'), (3, 'COMMA', ','), (3, 'ID', 'v4'), (3, 'COMMA', ','), (3, 'ID', 'v5'), (3, 'SEMI', ';'), (4, 'ARRAY', 'array'), (4, 'LPAREN', '['), (4, 'CONST', 1), (4, 'UNDERANGE', '..'), (4, 'CONST', 20), (4, 'RPAREN', ']'), (4, 'OF', 'of'), (4, 'INTEGER', 'integer'), (4, 'ID', 'a'), (4, 'COMMA', ','), (4, 'ID', 'b'), (4, 'COMMA', ','), (4, 'ID', 'c'), (4, 'SEMI', ';'), (6, 'PROCEDURE', 'procedure'), (6, 'ID', 'v1Add'), (6, 'LMIDPAREN', '('), (6, 'INTEGER', 'integer'), (6, 'ID', 'v1'), (6, 'RMIDPAREN', ')'), (6, 'SEMI', ';'), (7, 'VAR', 'var'), (7, 'INTEGER', 'integer'), (7, 'ID', 'temp1'), (7, 'SEMI', ';'), (8, 'BEGIN', 'begin'), (9, 'ID', 'temp1'), (9, 'ASSIGN', ':='), (9, 'CONST', 10), (9, 'SEMI', ';'), (10, 'ID', 'v1'), (10, 'ASSIGN', ':='), (10, 'ID', 'v1'), (10, 'PLUS', '+'), (10, 'ID', 'temp1'), (10, 'SEMI', ';'), (11, 'WRITE', 'write'), (11, 'LMIDPAREN', '('), (11, 'ID', 'v1'), (11, 'RMIDPAREN', ')'), (12, 'END', 'end'), (14, 'PROCEDURE', 'procedure'), (14, 'ID', 'v1Dec'), (14, 'LMIDPAREN', '('), (14, 'INTEGER', 'integer'), (14, 'ID', 'v1'), (14, 'RMIDPAREN', ')'), (14, 'SEMI', ';'), (15, 'VAR', 'var'), (15, 'INTEGER', 'integer'), (15, 'ID', 'temp2'), (15, 'SEMI', ';'), (16, 'BEGIN', 'begin'), (17, 'ID', 'temp2'), (17, 'ASSIGN', ':='), (17, 'CONST', 10), (17, 'SEMI', ';'), (18, 'ID', 'v1'), (18, 'ASSIGN', ':='), (18, 'ID', 'v1'), (18, 'MINUS', '-'), (18, 'ID', 'temp2'), (18, 'SEMI', ';'), (19, 'WRITE', 'write'), (19, 'LMIDPAREN', '('), (19, 'ID', 'v1'), (19, 'RMIDPAREN', ')'), (20, 'END', 'end'), (22, 'BEGIN', 'begin'), (23, 'READ', 'read'), (23, 'LMIDPAREN', '('), (23, 'ID', 'v1'), (23, 'RMIDPAREN', ')'), (23, 'SEMI', ';'), (24, 'ID', 'v1Add'), (24, 'LMIDPAREN', '('), (24, 'ID', 'v1'), (24, 'RMIDPAREN', ')'), (24, 'SEMI', ';'), (25, 'WRITE', 'write'), (25, 'LMIDPAREN', '('), (25, 'ID', 'v1'), (25, 'RMIDPAREN', ')'), (26, 'END', 'end')]
    tokenlist1.append((-1, 'DOT', '.'))
    tokenlist1.append((-1, 'EOF', 'EOF'))
    tokenlist2 = [(1, 'PROGRAM', 'Program'), (1, 'ID', 'p'), (2, 'TYPE', 'type'), (2, 'ID', 't'), (2, 'EQ', '='), (2, 'INTEGER', 'integer'), (2, 'SEMI', ';'), (3, 'ID', 't1'), (3, 'EQ', '='), (3, 'CHAR', 'char'), (3, 'SEMI', ';'), (4, 'ID', 't2'), (4, 'EQ', '='), (4, 'RECORD', 'record'), (5, 'INTEGER', 'integer'), (5, 'ID', 'e1'), (5, 'COMMA', ','), (5, 'ID', 'e2'), (5, 'SEMI', ';'), (6, 'CHAR', 'char'), (6, 'ID', 'f1'), (6, 'COMMA', ','), (6, 'ID', 'f2'), (6, 'SEMI', ';'), (7, 'ARRAY', 'array'), (7, 'LPAREN', '['), (7, 'CONST', 1), (7, 'UNDERANGE', '..'), (7, 'CONST', 5), (7, 'RPAREN', ']'), (7, 'OF', 'of'), (7, 'INTEGER', 'integer'), (7, 'ID', 'g1'), (7, 'COMMA', ','), (7, 'ID', 'g2'), (7, 'SEMI', ';'), (8, 'END', 'end'), (8, 'SEMI', ';'), (9, 'VAR', 'var'), (9, 'ID', 't'), (9, 'ID', 'v1'), (9, 'COMMA', ','), (9, 'ID', 'v2'), (9, 'COMMA', ','), (9, 'ID', 'v3'), (9, 'SEMI', ';'), (10, 'ID', 't1'), (10, 'ID', 'v4'), (10, 'SEMI', ';'), (11, 'ARRAY', 'array'), (11, 'LPAREN', '['), (11, 'CONST', 1), (11, 'UNDERANGE', '..'), (11, 'CONST', 20), (11, 'RPAREN', ']'), (11, 'OF', 'of'), (11, 'INTEGER', 'integer'), (11, 'ID', 'a'), (11, 'COMMA', ','), (11, 'ID', 'b'), (11, 'COMMA', ','), (11, 'ID', 'c'), (11, 'SEMI', ';'), (13, 'PROCEDURE', 'procedure'), (13, 'ID', 'v1Add'), (13, 'LMIDPAREN', '('), (13, 'ID', 't'), (13, 'ID', 'v1'), (13, 'RMIDPAREN', ')'), (13, 'SEMI', ';'), (14, 'VAR', 'var'), (14, 'INTEGER', 'integer'), (14, 'ID', 'temp1'), (14, 'SEMI', ';'), (15, 'BEGIN', 'begin'), (16, 'ID', 'temp1'), (16, 'ASSIGN', ':='), (16, 'CONST', 10), (16, 'SEMI', ';'), (17, 'ID', 'v1'), (17, 'ASSIGN', ':='), (17, 'ID', 'v1'), (17, 'PLUS', '+'), (17, 'ID', 'temp1'), (17, 'SEMI', ';'), (18, 'WRITE', 'write'), (18, 'LMIDPAREN', '('), (18, 'ID', 'v1'), (18, 'RMIDPAREN', ')'), (19, 'END', 'end'), (21, 'PROCEDURE', 'procedure'), (21, 'ID', 'v2Dec'), (21, 'LMIDPAREN', '('), (21, 'INTEGER', 'integer'), (21, 'ID', 'v2'), (21, 'RMIDPAREN', ')'), (21, 'SEMI', ';'), (22, 'VAR', 'var'), (22, 'INTEGER', 'integer'), (22, 'ID', 'temp2'), (22, 'SEMI', ';'), (23, 'BEGIN', 'begin'), (24, 'ID', 'temp2'), (24, 'ASSIGN', ':='), (24, 'CONST', 10), (24, 'SEMI', ';'), (25, 'ID', 'v2'), (25, 'ASSIGN', ':='), (25, 'ID', 'v2'), (25, 'MINUS', '-'), (25, 'ID', 'temp2'), (25, 'SEMI', ';'), (26, 'WRITE', 'write'), (26, 'LMIDPAREN', '('), (26, 'ID', 'v2'), (26, 'RMIDPAREN', ')'), (27, 'END', 'end'), (29, 'BEGIN', 'begin'), (30, 'READ', 'read'), (30, 'LMIDPAREN', '('), (30, 'ID', 'v1'), (30, 'RMIDPAREN', ')'), (30, 'SEMI', ';'), (31, 'ID', 'v1Add'), (31, 'LMIDPAREN', '('), (31, 'CONST', 10), (31, 'RMIDPAREN', ')'), (31, 'SEMI', ';'), (32, 'WRITE', 'write'), (32, 'LMIDPAREN', '('), (32, 'ID', 'v1'), (32, 'RMIDPAREN', ')'), (32, 'SEMI', ';'), (33, 'READ', 'read'), (33, 'LMIDPAREN', '('), (33, 'ID', 'v1'), (33, 'RMIDPAREN', ')'), (33, 'SEMI', ';'), (34, 'WRITE', 'write'), (34, 'LMIDPAREN', '('), (34, 'ID', 'a'), (34, 'LPAREN', '['), (34, 'CONST', 1), (34, 'RPAREN', ']'), (34, 'RMIDPAREN', ')'), (35, 'END', 'end'), (35, 'DOT', '.'), (35, 'EOF', 'EOF')]
    tokenlist3 = [(1, 'PROGRAM', 'program'), (1, 'ID', 'pp'), (2, 'TYPE', 'type'), (2, 'ID', 't'), (2, 'EQ', '='), (2, 'INTEGER', 'integer'), (2, 'SEMI', ';'), (3, 'VAR', 'var'), (3, 'INTEGER', 'integer'), (3, 'ID', 'v1'), (3, 'COMMA', ','), (3, 'ID', 'v2'), (3, 'COMMA', ','), (3, 'ID', 'v3'), (3, 'SEMI', ';'), (4, 'CHAR', 'char'), (4, 'ID', 'a1'), (4, 'COMMA', ','), (4, 'ID', 'b'), (4, 'COMMA', ','), (4, 'ID', 'c'), (4, 'SEMI', ';'), (5, 'ARRAY', 'array'), (5, 'LPAREN', '['), (5, 'CONST', 1), (5, 'UNDERANGE', '..'), (5, 'CONST', 20), (5, 'RPAREN', ']'), (5, 'OF', 'of'), (5, 'INTEGER', 'integer'), (5, 'ID', 'd'), (5, 'SEMI', ';'), (6, 'PROCEDURE', 'procedure'), (6, 'ID', 'f'), (6, 'LMIDPAREN', '('), (6, 'RMIDPAREN', ')'), (6, 'SEMI', ';'), (7, 'BEGIN', 'begin'), (8, 'ID', 'v1'), (8, 'ASSIGN', ':='), (8, 'CONST', 20), (8, 'PLUS', '+'), (8, 'CONST', 10), (8, 'SEMI', ';'), (9, 'IF', 'if'), (9, 'ID', 'v1'), (9, 'EQ', '='), (9, 'CONST', 30), (10, 'THEN', 'then'), (10, 'ID', 'a1'), (10, 'ASSIGN', ':='), (10, 'ID', "'e'"), (11, 'ELSE', 'else'), (11, 'ID', 'v2'), (11, 'ASSIGN', ':='), (11, 'CONST', 10), (12, 'FI', 'fi'), (13, 'END', 'End'), (14, 'BEGIN', 'Begin'), (15, 'ID', 'f'), (15, 'LMIDPAREN', '('), (15, 'RMIDPAREN', ')'), (15, 'SEMI', ';'), (16, 'WRITE', 'write'), (16, 'LMIDPAREN', '('), (16, 'ID', 'v1'), (16, 'RMIDPAREN', ')'), (17, 'END', 'end'), (17, 'DOT', '.'), (17, 'EOF', 'EOF')]
    formatTransf = FormatTransformer()
    tokenlist = formatTransf.tokenListTransf(tokenlist3)
    parser = Parser(tokenlist)
    root = parser.parse()

    # for name, value in vars(root).items():
    #     print(name, value)
    # print(ToStr(['a1', 'a2', 'cc', 'b']))
    # print(decode(root.child[1].sibling.child[0].sibling.sibling))

    # graph = Digraph('g', filename='SyntaxTree1.gv', graph_attr={'ranksep': '1'})
    graph = Digraph('g', filename='Syntax Tree.gv')
    graph.graph_attr['splines'] = 'line'
    graph.attr(rankdir='LR')
    # graph.graph_attr['len'] = '10'
    graph.node(name=str(id(root)), label=decode(root))
    # graph.node(name=str(random.randint(1, 10000)), label=decode(root))
    drawTree(graph, root)
    # graph = graph.unflatten(stagger=1)
    graph.view()
