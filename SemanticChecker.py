
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
                i = self.idx + 2
                while self.tokenlist[i][1] not in ['ID', 'CONST']:
                    i += 1
                if self.tokenlist[i][1] == 'CONST' \
                        or self.getType(self.tokenlist[i][2]) == 'INTEGER':
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
            if self.tokenlist[i][2] == ']':
                while self.tokenlist[i][2] != '[':
                    i -= 1
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
    tokenlist1 = ''
    checker = SemanticChecker(*tokenlist1, isTree=False)
    checker.tokenListCheck()
    # for aa in checker.tokenlist:
    #     print(aa)
    # print(checker.tokenlist)