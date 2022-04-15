
class SemanticError(Exception):
    def __init__(self, message, lineno):
        super().__init__(message, lineno)
        self.message = message
        self.lineno = lineno


class SemanticChecker:
    def __init__(self, *args, isTree=False):
        self.tokenlist = args if not isTree else None
        self.root = args if isTree else None
        self.idx = 0

    def getType(self, name):
        pass

    def getKind(self, name):
        pass

    def getElementType(self, name):
        pass

    def matchBegin(self):
        if self.tokenlist[self.idx][1] != 'BEGIN':
            self.idx += 1
            return False
        else:
            self.idx += 1
            return True

    def matchEnd(self):
        if self.tokenlist[self.idx][1] == 'END':
            return True
        return False

    def checkArrayMember(self):
        if self.getType(self.tokenlist[self.idx][2]) == 'ARRAY':
            if self.tokenlist[self.idx + 1][2] == '[':
                if self.tokenlist[self.idx + 2][1] == 'CONST' \
                        or self.getType(self.tokenlist[self.idx + 2][2]) == 'INTEGER':
                    return
            message = "数组成员变量引用不合法"
            raise SemanticError(message, self.tokenlist[self.idx][0])

    def checkRecordMember(self):
        if self.getType(self.tokenlist[self.idx][2]) == 'RECORD':
            if self.tokenlist[self.idx + 1][2] == '.':
                # if self.tokenlist[self.idx + 1][2] in 记录中的域
                pass

    def checkProcedureCall(self):
        if self.tokenlist[self.idx + 1][2] == '(' \
                and self.getKind(self.tokenlist[self.idx][2]) != 'PROCEDURE':
            message = "过程调用语句中的标识符不是过程标识符"
            raise SemanticError(message, self.tokenlist[self.idx][0])

    def checkAssignment(self):
        left = None
        i = self.idx - 1
        while self.tokenlist[i][2] not in ['begin', 'then', 'else', ';', 'do']:
            if self.tokenlist[i][1] == 'ID':
                left = self.tokenlist[i][2]
            i -= 1
        i = self.idx + 1
        while self.tokenlist[i][1] not in ['ID', 'CONST']:
            i += 1
        right = self.tokenlist[i][2] if self.tokenlist[i][1] == 'ID' else self.tokenlist[i][1]
        if self.getKind(left) != 'VAR':
            message = "赋值语句左端不是变量标识符"
            raise SemanticError(message, self.tokenlist[self.idx][0])
        if self.getElementType(left) == 'INTEGER' and right == 'CONST':
            return
        if self.getElementType(left) != self.getElementType(right):
            message = "赋值语句左右两边类型不相容"
            raise SemanticError(message, self.tokenlist[self.idx][0])

    def checkOperation(self):
        left = None
        i = self.idx - 1
        while self.tokenlist[i][2] not in [':=', '[', '(', '+', '-', '*', '/']:
            if self.tokenlist[i][1] in ['ID', 'CONST']:
                left = self.tokenlist[i][2] if self.tokenlist[i][1] == 'ID' else self.tokenlist[i][1]
            i -= 1
        i = self.idx + 1
        while self.tokenlist[i][1] not in ['ID', 'CONST']:
            i += 1
        right = self.tokenlist[i][2] if self.tokenlist[i][1] == 'ID' else self.tokenlist[i][1]
        if left =='CONST' and right == 'CONST':
            return
        elif left =='CONST' and self.getElementType(right) == 'INTEGER':
            return
        elif right =='CONST' and self.getElementType(left) == 'INTEGER':
            return
        elif self.getElementType(left) == self.getElementType(right):
            return
        message = "表达式中运算符的分量不一致"
        raise SemanticError(message, self.tokenlist[self.idx][0])

    def checkCmparison(self):
        left = None
        i = self.idx - 1
        while self.tokenlist[i][2] not in ['while', 'if']:
            if self.tokenlist[i][1] in ['ID', 'CONST']:
                left = self.tokenlist[i][2] if self.tokenlist[i][1] == 'ID' else self.tokenlist[i][1]
            i -= 1
        i = self.idx + 1
        while self.tokenlist[i][1] not in ['ID', 'CONST']:
            i += 1
        right = self.tokenlist[i][2] if self.tokenlist[i][1] == 'ID' else self.tokenlist[i][1]
        if left =='CONST' and right == 'CONST':
            return
        elif left =='CONST' and self.getElementType(right) == 'INTEGER':
            return
        elif right =='CONST' and self.getElementType(left) == 'INTEGER':
            return
        elif self.getElementType(left) == self.getElementType(right):
            return
        message = "if和while语句的条件判断部分不是bool型"
        raise SemanticError(message, self.tokenlist[self.idx][0])

    def tokenListCheck(self):
        self.idx = 0
        isbegin = False
        while self.idx < len(self.tokenlist):
            if not isbegin:
                if not self.matchBegin():
                    continue
                isbegin = True
            if self.tokenlist[self.idx][1] == 'ID':
                self.checkArrayMember()
                self.checkRecordMember()
                self.checkProcedureCall()
            if self.tokenlist[self.idx][2] == ':=':
                self.checkAssignment()
            if self.tokenlist[self.idx][2] in ['+', '-', '*', '/']:
                self.checkOperation()
            if self.tokenlist[self.idx][2] in ['=', '<']:
                self.checkCmparison()
            if self.matchEnd():
                isbegin = False
            self.idx += 1


if __name__ == '__main__':
    tokenlist1 = [(1, 'PROGRAM', 'Program'), (1, 'ID', 'p'), (2, 'TYPE', 'type'), (2, 'ID', 't'), (2, 'EQ', '='), (2, 'INTEGER', 'integer'), (2, 'SEMI', ';'), (2, 'ID', 't'), (2, 'EQ', '='), (2, 'CHAR', 'char'), (2, 'SEMI', ';'), (3, 'VAR', 'var'), (3, 'ID', 't'), (3, 'ID', 'v1'), (3, 'COMMA', ','), (3, 'ID', 'v2'), (3, 'COMMA', ','), (3, 'ID', 'v3'), (3, 'COMMA', ','), (3, 'ID', 'v4'), (3, 'COMMA', ','), (3, 'ID', 'v5'), (3, 'SEMI', ';'), (4, 'ARRAY', 'array'), (4, 'LPAREN', '['), (4, 'CONST', 1), (4, 'UNDERANGE', '..'), (4, 'CONST', 20), (4, 'RPAREN', ']'), (4, 'OF', 'of'), (4, 'INTEGER', 'integer'), (4, 'ID', 'a'), (4, 'COMMA', ','), (4, 'ID', 'b'), (4, 'COMMA', ','), (4, 'ID', 'c'), (4, 'SEMI', ';'), (6, 'PROCEDURE', 'procedure'), (6, 'ID', 'v1Add'), (6, 'LMIDPAREN', '('), (6, 'INTEGER', 'integer'), (6, 'ID', 'v1'), (6, 'RMIDPAREN', ')'), (6, 'SEMI', ';'), (7, 'VAR', 'var'), (7, 'INTEGER', 'integer'), (7, 'ID', 'temp1'), (7, 'SEMI', ';'), (8, 'BEGIN', 'begin'), (9, 'ID', 'temp1'), (9, 'ASSIGN', ':='), (9, 'CONST', 10), (9, 'SEMI', ';'), (10, 'ID', 'v1'), (10, 'ASSIGN', ':='), (10, 'ID', 'v1'), (10, 'PLUS', '+'), (10, 'ID', 'temp1'), (10, 'SEMI', ';'), (11, 'WRITE', 'write'), (11, 'LMIDPAREN', '('), (11, 'ID', 'v1'), (11, 'RMIDPAREN', ')'), (12, 'END', 'end'), (14, 'PROCEDURE', 'procedure'), (14, 'ID', 'v1Dec'), (14, 'LMIDPAREN', '('), (14, 'INTEGER', 'integer'), (14, 'ID', 'v1'), (14, 'RMIDPAREN', ')'), (14, 'SEMI', ';'), (15, 'VAR', 'var'), (15, 'INTEGER', 'integer'), (15, 'ID', 'temp2'), (15, 'SEMI', ';'), (16, 'BEGIN', 'begin'), (17, 'ID', 'temp2'), (17, 'ASSIGN', ':='), (17, 'CONST', 10), (17, 'SEMI', ';'), (18, 'ID', 'v1'), (18, 'ASSIGN', ':='), (18, 'ID', 'v1'), (18, 'MINUS', '-'), (18, 'ID', 'temp2'), (18, 'SEMI', ';'), (19, 'WRITE', 'write'), (19, 'LMIDPAREN', '('), (19, 'ID', 'v1'), (19, 'RMIDPAREN', ')'), (20, 'END', 'end'), (22, 'BEGIN', 'begin'), (23, 'READ', 'read'), (23, 'LMIDPAREN', '('), (23, 'ID', 'v1'), (23, 'RMIDPAREN', ')'), (23, 'SEMI', ';'), (24, 'ID', 'v1Add'), (24, 'LMIDPAREN', '('), (24, 'ID', 'v1'), (24, 'RMIDPAREN', ')'), (24, 'SEMI', ';'), (25, 'WRITE', 'write'), (25, 'LMIDPAREN', '('), (25, 'ID', 'v1'), (25, 'RMIDPAREN', ')'), (26, 'END', 'end')]
    tokenlist2 = [(1, 'PROGRAM', 'program'), (1, 'ID', 'pp'), (2, 'TYPE', 'type'), (2, 'ID', 't'), (2, 'EQ', '='),
     (2, 'INTEGER', 'integer'), (2, 'SEMI', ';'), (3, 'VAR', 'var'), (3, 'INTEGER', 'integer'), (3, 'ID', 'v1'),
     (3, 'COMMA', ','), (3, 'ID', 'v2'), (3, 'COMMA', ','), (3, 'ID', 'v3'), (3, 'SEMI', ';'), (4, 'CHAR', 'char'),
     (4, 'ID', 'a1'), (4, 'COMMA', ','), (4, 'ID', 'b'), (4, 'COMMA', ','), (4, 'ID', 'c'), (4, 'SEMI', ';'),
     (5, 'ARRAY', 'array'), (5, 'LPAREN', '['), (5, 'CONST', 1), (5, 'UNDERANGE', '..'), (5, 'CONST', 20),
     (5, 'RPAREN', ']'), (5, 'OF', 'of'), (5, 'INTEGER', 'integer'), (5, 'ID', 'd'), (5, 'SEMI', ';'),
     (6, 'PROCEDURE', 'procedure'), (6, 'ID', 'f'), (6, 'LMIDPAREN', '('), (6, 'RMIDPAREN', ')'), (6, 'SEMI', ';'),
     (7, 'BEGIN', 'begin'), (8, 'ID', 'v1'), (8, 'ASSIGN', ':='), (8, 'CONST', 20), (8, 'PLUS', '+'), (8, 'CONST', 10),
     (8, 'SEMI', ';'), (9, 'IF', 'if'), (9, 'ID', 'v1'), (9, 'EQ', '='), (9, 'CONST', 30), (10, 'THEN', 'then'),
     (10, 'ID', 'a1'), (10, 'ASSIGN', ':='), (10, 'ID', "'e'"), (11, 'ELSE', 'else'), (11, 'ID', 'v2'),
     (11, 'ASSIGN', ':='), (11, 'CONST', 10), (12, 'FI', 'fi'), (13, 'END', 'End'), (14, 'BEGIN', 'Begin'),
     (15, 'ID', 'f'), (15, 'LMIDPAREN', '('), (15, 'RMIDPAREN', ')'), (15, 'SEMI', ';'), (16, 'WRITE', 'write'),
     (16, 'LMIDPAREN', '('), (16, 'ID', 'v1'), (16, 'RMIDPAREN', ')'), (17, 'END', 'end'), (17, 'DOT', '.'),
     (17, 'EOF', '文件结束符号，无语义信息')]
    checker = SemanticChecker(*tokenlist2, isTree=False)
    checker.tokenListCheck()
    # for aa in checker.tokenlist:
    #     print(aa)
    # print(checker.tokenlist)