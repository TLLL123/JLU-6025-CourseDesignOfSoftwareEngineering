
class SemanticError(Exception):
    def __init__(self, message, lineno):
        super().__init__(message, lineno)
        self.message = message
        self.lineno = lineno


class SemanticChecker:  # 功能 5, 6, 7, 10, 11, 12
    def __init__(self, *args, idx, isTree=False):
        self.tokenlist = args if not isTree else None
        self.root = args if isTree else None
        self.idx = idx
        self.errorlist = []

    def getType(self, name):
        for Sym in SymTab[::-1]:
            if Sym.name == name and Sym.kind == 'VAR':
                return Sym.type
        if list(name)[0] == "'":
            return "CHAR"

    def getKind(self, name):
        for Sym in SymTab[::-1]:
            if Sym.name == name:
                return Sym.kind

    def getElementType(self, name, idx):
        for Sym in SymTab[::-1]:
            if Sym.name == name and Sym.kind == 'VAR':
                if Sym.type == "ARRAY":
                    return Sym.ElemType
                elif Sym.type == "RECORD":
                    try:
                        type = Sym.MemberDict[self.tokenlist[idx + 2][2]]
                        return type[1] if isinstance(type, tuple) else type
                    except:
                        return None
                else:
                    return Sym.type
        if list(name)[0] == "'":
            return "CHAR"

    def getRecordDict(self, name):
        for Sym in SymTab[::-1]:
            if Sym.name == name and Sym.kind == 'VAR':
                return Sym.MemberDict

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
        if self.tokenlist[self.idx + 1][2] == '[' \
                and self.getType(self.tokenlist[self.idx][2]) != 'ARRAY' \
                and self.tokenlist[self.idx - 1][2] != '.':
            message = "变量引用不合法 In line {a}, \"{b}\"" \
                .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
            self.errorlist.append(message)
            return
        if self.getType(self.tokenlist[self.idx][2]) == 'ARRAY':
            if self.tokenlist[self.idx + 1][2] == '[':
                i = self.idx + 2
                while self.tokenlist[i][1] not in ['ID', 'CONST']:
                    i += 1
                if self.tokenlist[i][1] == 'CONST' \
                        or self.getType(self.tokenlist[i][2]) == 'INTEGER':
                    return
            message = "数组变量下标类型不合法 In line {a}, \"{b}\""\
                .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
            self.errorlist.append(message)
            # raise SemanticError(message, self.tokenlist[self.idx][0])

    def checkRecordMember(self):
        if self.tokenlist[self.idx + 1][2] == '.' \
                and self.getType(self.tokenlist[self.idx][2]) != 'RECORD':
            message = "变量引用不合法 In line {a}, \"{b}\"" \
                .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
            self.errorlist.append(message)
            return
        if self.getType(self.tokenlist[self.idx][2]) == 'RECORD':
            if self.tokenlist[self.idx + 1][2] != '.':
                message = "记录体结构引用不合法 In line {a}, \"{b}\""\
                    .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
                self.errorlist.append(message)
                return
                # raise SemanticError(message, self.tokenlist[self.idx][0])
            dic = self.getRecordDict(self.tokenlist[self.idx][2])
            if self.tokenlist[self.idx + 2][2] not in dic.keys():
                message = "记录体结构域成员变量未定义 In line {a}, \"{b}\""\
                    .format(a=self.tokenlist[self.idx + 2][0], b=self.tokenlist[self.idx + 2][2])
                self.errorlist.append(message)
                return
                # raise SemanticError(message, self.tokenlist[self.idx + 2][0])
            type = dic[self.tokenlist[self.idx + 2][2]]
            if isinstance(type, tuple):
                if self.tokenlist[self.idx + 3][2] != '[':
                    message = "数组变量引用不合法 In line {a}, \"{b}\""\
                        .format(a=self.tokenlist[self.idx + 2][0], b=self.tokenlist[self.idx + 2][2])
                    self.errorlist.append(message)
                    return
                    # raise SemanticError(message, self.tokenlist[self.idx + 2][0])
                if self.tokenlist[self.idx + 4][1] == 'CONST' \
                        and self.tokenlist[self.idx + 5][2] == ']':
                    if type[2] <= self.tokenlist[self.idx + 4][2] <= type[3]:
                        return
                    message = "数组变量下标越界 In line {a}, \"{b}\""\
                        .format(a=self.tokenlist[self.idx + 4][0], b=self.tokenlist[self.idx + 4][2])
                    self.errorlist.append(message)
                    return
                    # raise SemanticError(message, self.tokenlist[self.idx + 4][0])
                if self.tokenlist[self.idx + 4][2] == '(' \
                        and self.tokenlist[self.idx + 5][1] == 'CONST' \
                        and self.tokenlist[self.idx + 7][2] == ']':
                    if type[2] <= self.tokenlist[self.idx + 5][2] <= type[3]:
                        return
                    message = "数组变量下标越界 In line {a}, \"{b}\""\
                        .format(a=self.tokenlist[self.idx + 5][0], b=self.tokenlist[self.idx + 5][2])
                    self.errorlist.append(message)
                    return
                i = self.idx + 4
                while self.tokenlist[i][1] not in ['ID', 'CONST']:
                    i += 1
                if self.tokenlist[i][1] == 'CONST' \
                        or self.getType(self.tokenlist[i][2]) == 'INTEGER':
                    return
                message = "数组变量下标类型不合法 In line {a}, \"{b}\""\
                    .format(a=self.tokenlist[self.idx + 2][0], b=self.tokenlist[self.idx + 2][2])
                self.errorlist.append(message)
                # raise SemanticError(message, self.tokenlist[self.idx + 2][0])

    def checkProcedureCall(self):
        if self.tokenlist[self.idx + 1][2] != '(' \
                and self.getKind(self.tokenlist[self.idx][2]) == 'PROCEDURE':
            message = "变量使用不合法 In line {a}, \"{b}\"" \
                .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
            self.errorlist.append(message)
            return
        if self.tokenlist[self.idx + 1][2] == '(' \
                and self.getKind(self.tokenlist[self.idx][2]) != 'PROCEDURE':
            message = "过程调用语句中的标识符不是过程标识符 In line {a}, \"{b}\""\
                .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
            self.errorlist.append(message)
            # raise SemanticError(message, self.tokenlist[self.idx][0])

    def checkAssignment(self):
        left = None
        ii = i = self.idx - 1
        while self.tokenlist[i][2] not in ['begin', 'then', 'else', ';', 'do']:
            if self.tokenlist[i][1] == 'ID':
                left = self.tokenlist[i][2]
                ii = i
            i -= 1
        j = self.idx + 1
        while self.tokenlist[j][1] not in ['ID', 'CONST']:
            j += 1
        right = self.tokenlist[j][2] if self.tokenlist[j][1] == 'ID' else self.tokenlist[j][1]
        if self.getKind(left) != 'VAR':
            message = "赋值语句左端不是变量标识符 In line {a}, \"{b}\""\
                .format(a=self.tokenlist[ii][0], b=self.tokenlist[ii][2])
            self.errorlist.append(message)
            return
            # raise SemanticError(message, self.tokenlist[self.idx][0])
        if self.getElementType(left, ii) == 'INTEGER' and right == 'CONST':
            return
        if self.getElementType(left, ii) != self.getElementType(right, j):
            message = "赋值语句左右两边类型不相容 In line {a}, \"{b}\" and \"{c}...\""\
                .format(a=self.tokenlist[ii][0], b=self.tokenlist[ii][2], c=self.tokenlist[j][2])
            self.errorlist.append(message)
            # raise SemanticError(message, self.tokenlist[self.idx][0])

    def checkOperation(self):
        left = None
        ii = i = self.idx - 1
        while self.tokenlist[i][2] not in [':=', '[', '(', '+', '-', '*', '/']:
            if self.tokenlist[i][2] == ']':
                while self.tokenlist[i][2] != '[':
                    i -= 1
            if self.tokenlist[i][1] in ['ID', 'CONST']:
                left = self.tokenlist[i][2] if self.tokenlist[i][1] == 'ID' else self.tokenlist[i][1]
                ii = i
            i -= 1
        j = self.idx + 1
        while self.tokenlist[j][1] not in ['ID', 'CONST']:
            j += 1
        right = self.tokenlist[j][2] if self.tokenlist[j][1] == 'ID' else self.tokenlist[j][1]
        if left == 'CONST' and right == 'CONST':
            return
        elif left == 'CONST' and self.getElementType(right, j) == 'INTEGER':
            return
        elif right == 'CONST' and self.getElementType(left, ii) == 'INTEGER':
            return
        elif self.getElementType(left, ii) == self.getElementType(right, j):
            return
        if ii + 2 == j:
            message = "表达式中运算符的分量不一致 In line {a}, \"{b}\" and \"{c}\"" \
                .format(a=self.tokenlist[ii][0], b=self.tokenlist[ii][2], c=self.tokenlist[j][2])
        else:
            message = "表达式中运算符的分量不一致 In line {a}" \
                .format(a=self.tokenlist[ii][0])
        self.errorlist.append(message)
        # raise SemanticError(message, self.tokenlist[self.idx][0])

    def checkCmparison(self):
        left = None
        ii = i = self.idx - 1
        while self.tokenlist[i][2] not in ['while', 'if']:
            if self.tokenlist[i][1] in ['ID', 'CONST']:
                left = self.tokenlist[i][2] if self.tokenlist[i][1] == 'ID' else self.tokenlist[i][1]
                ii = i
            i -= 1
        j = self.idx + 1
        while self.tokenlist[j][1] not in ['ID', 'CONST']:
            j += 1
        right = self.tokenlist[j][2] if self.tokenlist[j][1] == 'ID' else self.tokenlist[j][1]
        if left == 'CONST' and right == 'CONST':
            return
        elif left == 'CONST' and self.getElementType(right, j) == 'INTEGER':
            return
        elif right == 'CONST' and self.getElementType(left, ii) == 'INTEGER':
            return
        elif self.getElementType(left, ii) == self.getElementType(right, j):
            return
        message = "if和while语句的条件判断部分不是bool型 In line {a}, \"{b}\" and \"{c}\""\
            .format(a=self.tokenlist[ii][0], b=self.tokenlist[ii][2], c=self.tokenlist[j][2])
        self.errorlist.append(message)
        # raise SemanticError(message, self.tokenlist[self.idx][0])

    def tokenListCheck(self):
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
        for error in self.errorlist:
            print('\033[1;31;40m')
            print('\033[7;31m{}\033[1;31;40m'.format(error))
            print('\033[0m')


SymTab = []


if __name__ == '__main__':
    tokenlist1 = ''
    checker = SemanticChecker(*tokenlist1, idx=0, isTree=False)
    checker.tokenListCheck()
    # for aa in checker.tokenlist:
    #     print(aa)
    # print(checker.tokenlist)