"""
Semantic Check
"""
class SemanticError(Exception):
    """
    自定义语义错误异常
    """
    def __init__(self, message, lineno):
        """
        语法错误信息
            message:错误具体信息
            status：显示错误所在行号
        """
        super().__init__(message, lineno)
        self.message = message
        self.lineno = lineno


class SemanticChecker:  # 全部 5, 6, 7, 10, 11, 12 ; 部分 3, 4
    def __init__(self, *args, idx, isTree=False):
        self.tokenlist = args if not isTree else None
        self.root = args if isTree else None
        self.idx = idx
        self.errorlist = []  # 语义错误队列

    def getType(self, name):    # 修改复用，获取类型
        for Sym in SymTab[::-1]:
            if Sym.name == name and Sym.kind == 'VAR':
                return Sym.type
        if list(name)[0] == "'":
            return "CHAR"

    def getKind(self, name):    # 修改复用，获取类别
        for Sym in SymTab[::-1]:
            if Sym.name == name:
                return Sym.kind

    def getElementType(self, name, idx):    # 解析变量类型，int，char，array，record
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

    def getRecordDict(self, name):  # 查找记录体结构定义表
        for Sym in SymTab[::-1]:
            if Sym.name == name and Sym.kind == 'VAR':
                return Sym.MemberDict

    def matchBegin(self):   # 标记，检查开
        if self.tokenlist[self.idx][1] != 'BEGIN':
            self.idx += 1
            return False
        else:
            self.idx += 1
            return True

    def matchEnd(self):     # 标记，检查关
        if self.tokenlist[self.idx][1] == 'END':
            return True
        return False

    def checkArrayMember(self):     # 数组，数组成员变量引用是否合法
        if self.tokenlist[self.idx + 1][2] == '[' \
                and self.getType(self.tokenlist[self.idx][2]) != 'ARRAY' \
                and self.tokenlist[self.idx - 1][2] != '.':
            message = "引用不合法：非数组类型标识符使用数组类型引用 In line {a}, \"{b}\"" \
                .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
            self.errorlist.append(message)
            return
        if self.getType(self.tokenlist[self.idx][2]) == 'ARRAY':
            if self.tokenlist[self.idx + 1][2] == '[':
                i = self.idx + 2
                while self.tokenlist[i][1] not in ['ID', 'CONST']:
                    i += 1
                if self.tokenlist[i][1] != 'CONST' \
                        and self.getType(self.tokenlist[i][2]) != 'INTEGER':
                    message = "引用不合法：数组变量下标类型非整形 In line {a}, \"{b}\"" \
                        .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
                    self.errorlist.append(message)
                return
            left = None
            i = self.idx - 1
            while self.tokenlist[i][2] not in ['begin', 'then', 'else', ';', 'do']:
                if self.tokenlist[i][1] == 'ID':
                    left = self.tokenlist[i][2]
                i -= 1
            if self.getKind(left) != 'PROCEDURE':
                message = "引用不合法：数组变量被直接使用 In line {a}, \"{b}\"" \
                    .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
                self.errorlist.append(message)

    def checkRecordMember(self):    # 记录，记录成员变量引用是否合法
        if self.tokenlist[self.idx + 1][2] == '.' \
                and self.getType(self.tokenlist[self.idx][2]) != 'RECORD':
            message = "引用不合法：非记录体变量使用记录体引用格式 In line {a}, \"{b}\"" \
                .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
            self.errorlist.append(message)
            return
        if self.getType(self.tokenlist[self.idx][2]) == 'RECORD':
            left = None
            i = self.idx - 1
            while self.tokenlist[i][2] not in ['begin', 'then', 'else', ';', 'do']:
                if self.tokenlist[i][1] == 'ID':
                    left = self.tokenlist[i][2]
                i -= 1
            if self.tokenlist[self.idx + 1][2] == '.':
                dic = self.getRecordDict(self.tokenlist[self.idx][2])
                if self.tokenlist[self.idx + 2][2] not in dic.keys():
                    message = "引用不合法：记录体域成员变量未定义 In line {a}, \"{b}\"" \
                        .format(a=self.tokenlist[self.idx + 2][0], b=self.tokenlist[self.idx + 2][2])
                    self.errorlist.append(message)
                    return
                    # raise SemanticError(message, self.tokenlist[self.idx + 2][0])
                type = dic[self.tokenlist[self.idx + 2][2]]
                if isinstance(type, tuple):
                    if self.tokenlist[self.idx + 3][2] == '[':
                        if self.tokenlist[self.idx + 4][1] == 'CONST' \
                                and self.tokenlist[self.idx + 5][2] == ']':
                            if type[2] <= self.tokenlist[self.idx + 4][2] <= type[3]:
                                return
                            message = "引用不合法：数组变量下标越界 In line {a}, \"{b}\"" \
                                .format(a=self.tokenlist[self.idx + 4][0], b=self.tokenlist[self.idx + 4][2])
                            self.errorlist.append(message)
                            return
                        if self.tokenlist[self.idx + 4][2] == '(' \
                                and self.tokenlist[self.idx + 5][1] == 'CONST' \
                                and self.tokenlist[self.idx + 7][2] == ']':
                            if type[2] <= self.tokenlist[self.idx + 5][2] <= type[3]:
                                return
                            message = "引用不合法：数组变量下标越界 In line {a}, \"{b}\"" \
                                .format(a=self.tokenlist[self.idx + 5][0], b=self.tokenlist[self.idx + 5][2])
                            self.errorlist.append(message)
                            return
                        i = self.idx + 4
                        while self.tokenlist[i][1] not in ['ID', 'CONST']:
                            i += 1
                        if self.tokenlist[i][1] != 'CONST' \
                                and self.getType(self.tokenlist[i][2]) != 'INTEGER':
                            message = "引用不合法：数组变量下标类型非整形 In line {a}, \"{b}\"" \
                                .format(a=self.tokenlist[self.idx + 2][0], b=self.tokenlist[self.idx + 2][2])
                            self.errorlist.append(message)
                        return
                    if self.getKind(left) != 'PROCEDURE':
                        message = "引用不合法：数组变量被直接使用 In line {a}, \"{b}\"" \
                            .format(a=self.tokenlist[self.idx + 2][0], b=self.tokenlist[self.idx + 2][2])
                        self.errorlist.append(message)
                return
            if self.getKind(left) != 'PROCEDURE':
                message = "引用不合法：记录体结构被直接使用 In line {a}, \"{b}\"" \
                    .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
                self.errorlist.append(message)

    def checkProcedureCall(self):   # 过程调用是否合法
        if self.tokenlist[self.idx + 1][2] != '(' \
                and self.getKind(self.tokenlist[self.idx][2]) == 'PROCEDURE':
            message = "引用不合法：过程标识符被直接使用 In line {a}, \"{b}\"" \
                .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
            self.errorlist.append(message)
            return
        if self.tokenlist[self.idx + 1][2] == '(' \
                and self.getKind(self.tokenlist[self.idx][2]) != 'PROCEDURE':
            message = "引用不合法：过程调用语句中的标识符不是过程标识符 In line {a}, \"{b}\""\
                .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
            self.errorlist.append(message)
            # raise SemanticError(message, self.tokenlist[self.idx][0])

    def checkAssignment(self):  # 赋值语句左端是否为标识符；赋值语句左右两端类型是否相容
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
            message = "表达式不合法：赋值语句左端不是变量标识符 In line {a}, \"{b}\""\
                .format(a=self.tokenlist[ii][0], b=self.tokenlist[ii][2])
            self.errorlist.append(message)
            return
            # raise SemanticError(message, self.tokenlist[self.idx][0])
        if self.getElementType(left, ii) == 'INTEGER' and right == 'CONST':
            return
        if self.getElementType(left, ii) != self.getElementType(right, j):
            message = "表达式不合法：赋值语句左右两侧类型不相容 In line {a}, \"{b}\" and \"{c}\""\
                .format(a=self.tokenlist[ii][0], b=self.tokenlist[ii][2], c=self.tokenlist[j][2])
            self.errorlist.append(message)
            # raise SemanticError(message, self.tokenlist[self.idx][0])

    def checkOperation(self):   # 表达式运算符分量是否相容
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
            message = "表达式不合法：表达式中运算符分量类型不一致 In line {a}, \"{b}\" and \"{c}\"" \
                .format(a=self.tokenlist[ii][0], b=self.tokenlist[ii][2], c=self.tokenlist[j][2])
        else:
            message = "表达式不合法：表达式中运算符分量类型不一致 In line {a}" \
                .format(a=self.tokenlist[ii][0])
        self.errorlist.append(message)
        # raise SemanticError(message, self.tokenlist[self.idx][0])

    def checkCmparison(self):   # if，while条件判断部分是否合法
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
        message = "比较不合法：条件判断部分比较类型不一致 In line {a}, \"{b}\" and \"{c}\""\
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