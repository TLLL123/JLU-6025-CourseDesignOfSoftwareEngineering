'''
构造全局符号表，扫描完一层后删除当前层符号表
检查当前层内重复定义错误（类型、结构体内部成员、变量）、
a[x]/r.a[x]中a是不是数组，r是不是结构体、
未定义就使用错误、
数组用常数访问时的下标越界错误、
函数调用时参数类型及个数的匹配错误（考虑到了变量/常数/数组成员/记录成员/记录的数组成员等复杂情况）
'''
import LexicalAnalysis as LA
from functools import partial


class Symbol:#符号表元素
    def __init__(self,name,level,kind,type,ElemType,Low,Up,ParameterDict,MemberDict):
        self.name=name
        self.level=level
        self.kind=kind
        self.type=type
        self.ElemType=ElemType
        self.Low=Low
        self.Up=Up
        self.ParameterDict=ParameterDict
        self.MemberDict=MemberDict

"""*****************************增加**********************************"""
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
                if self.tokenlist[i][1] != 'CONST' \
                        and self.getType(self.tokenlist[i][2]) != 'INTEGER':
                    message = "数组变量下标类型不合法 In line {a}, \"{b}\"" \
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
                message = "数组变量引用不合法 In line {a}, \"{b}\"" \
                    .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
                self.errorlist.append(message)

    def checkRecordMember(self):
        if self.tokenlist[self.idx + 1][2] == '.' \
                and self.getType(self.tokenlist[self.idx][2]) != 'RECORD':
            message = "变量引用不合法 In line {a}, \"{b}\"" \
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
                    message = "记录体结构域成员变量未定义 In line {a}, \"{b}\"" \
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
                            message = "数组变量下标越界 In line {a}, \"{b}\"" \
                                .format(a=self.tokenlist[self.idx + 4][0], b=self.tokenlist[self.idx + 4][2])
                            self.errorlist.append(message)
                            return
                        if self.tokenlist[self.idx + 4][2] == '(' \
                                and self.tokenlist[self.idx + 5][1] == 'CONST' \
                                and self.tokenlist[self.idx + 7][2] == ']':
                            if type[2] <= self.tokenlist[self.idx + 5][2] <= type[3]:
                                return
                            message = "数组变量下标越界 In line {a}, \"{b}\"" \
                                .format(a=self.tokenlist[self.idx + 5][0], b=self.tokenlist[self.idx + 5][2])
                            self.errorlist.append(message)
                            return
                        i = self.idx + 4
                        while self.tokenlist[i][1] not in ['ID', 'CONST']:
                            i += 1
                        if self.tokenlist[i][1] != 'CONST' \
                                and self.getType(self.tokenlist[i][2]) != 'INTEGER':
                            message = "数组变量下标类型不合法 In line {a}, \"{b}\"" \
                                .format(a=self.tokenlist[self.idx + 2][0], b=self.tokenlist[self.idx + 2][2])
                            self.errorlist.append(message)
                        return
                    if self.getKind(left) != 'PROCEDURE':
                        message = "数组变量引用不合法 In line {a}, \"{b}\"" \
                            .format(a=self.tokenlist[self.idx + 2][0], b=self.tokenlist[self.idx + 2][2])
                        self.errorlist.append(message)
                return
            if self.getKind(left) != 'PROCEDURE':
                message = "记录体结构引用不合法 In line {a}, \"{b}\"" \
                    .format(a=self.tokenlist[self.idx][0], b=self.tokenlist[self.idx][2])
                self.errorlist.append(message)

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
        for error in self.errorlist:
            print('\033[1;31;40m')
            print('\033[7;31m{}\033[1;31;40m'.format(error))
            print('\033[0m')
"""*****************************增加**********************************"""


#print(tokens.obj.txt)
tokens=LA.startLexAnalysis(LA.codeInput)
if tokens == None:  # 表明有词法错误
    exit()
scanTokenList=[]#辅助获取符号表，标记扫描过了的token
for i in tokens:
    scanTokenList.append(0)
#print(len(tokens))
#print(len(scanTokenList))
SymTab=[]#元素是Sym对象
Level=0#当前层数

def redefinition(name,Level):#声明阶段，判断此标识符在当前层是否重复定义
    for Sym in SymTab:
        if Sym.level==Level:
            if Sym.name==name:
                return 1
    return 0

def delNowLevel(Level):#删除当前层符号表
    while True:
        if SymTab[-1].level==Level:
            SymTab.pop()
        if SymTab[-1].level!=Level:
            break

def judgeDefine(ID):
    for Sym in SymTab:
        if Sym.name==ID:
            return 1
    return 0

def getType(name):
    if name.upper() in ['INTEGER','CHAR']:
        return name.upper()
    for Sym in SymTab:
        if Sym.kind=='TYPE' and Sym.name==name:
            return Sym.type
    return None

def name2type(name):#用于检查形实参是否匹配
    for Sym in SymTab:
        if Sym.kind == 'VAR' and Sym.name == name:
            return Sym.type
    if isinstance(name, int) == 1:
        return 'INTEGER'
    elif isinstance(name, str) == 1:
        return 'CHAR'

def returnSymItem(name):#倒着查表以返回最近一次定义的变量
    for Sym in SymTab[::-1]:
        if Sym.name==name:
            return Sym
    return None

def outFormat(content):
    if content==None:
        return "---"
    else:
        return str(content)

def printSymTab():
    print("\33[31m--------------------------------------------------------------------------------符号表：------------------------------------------------------------------------------------")
    print("\33[31m{0:<20}{1:<20}{2:<20}{3:<20}{4:<20}{5:<20}{6:<20}{7:<20}{8:<20}".format("name", "level", "kind", "type", "ElemType", "Low", "Up","ParameterDict","MemberDict"))
    for i in SymTab:
        print('\33[34m{0:<20}{1:<20}{2:<20}{3:<20}{4:<20}{5:<20}{6:<20}{7:<20}{8:<20}'.format(outFormat(i.name), outFormat(i.level),outFormat(i.kind), outFormat(i.type),outFormat(i.ElemType), outFormat(i.Low),outFormat(i.Up),outFormat(i.ParameterDict),outFormat(i.MemberDict)))

semanticErrorFlag=0
#print('\33[31m')#错误信息用红字输出
i=0
while tokens[i][1]!='EOF':
    if tokens[i][1]=='PROGRAM':
        SymTab.append(Symbol(tokens[i+1][2],Level,'PROGRAM',None,None,None,None,None,None))
        Level+=1
        i += 2;continue
    elif tokens[i][1]=='TYPE':#INTEGER/CHAR/ARRAY/RECORD的别名，别名的别名
        flag=0
        for j in range(i+1,len(tokens)):
            if tokens[j][1] in ['VAR','PROCEDURE','BEGIN']:#统计所有类型
                i=j
                break
            if tokens[j][1]=='ID' and tokens[j+1][2]=='=':
                if redefinition(tokens[j][2],Level)==1:
                    flag=1;semanticErrorFlag=1
                    print("\33[31m第"+str(tokens[j][0])+"行，类型标识符"+tokens[j][2]+"重复定义，请修改错误后再进行语义分析")
                    break
                if tokens[j+2][1]=='ARRAY':
                    SymTab.append(Symbol(tokens[j][2],Level,'TYPE','ARRAY',getType(tokens[j+9][2]),tokens[j+4][2],tokens[j+6][2],None,None))
                elif tokens[j+2][1]!='RECORD':
                    SymTab.append(Symbol(tokens[j][2],Level,'TYPE',getType(tokens[j+2][2]),None,None,None,None,None))
                else:#记录类型的别名
                    memberDict={}
                    k=j+3
                    while tokens[k][1]!='END':
                        if tokens[k][1]=='INTEGER' and tokens[k-1][1]!='OF':
                            while tokens[k][2]!=';':
                                if tokens[k][1]=='ID':
                                    if tokens[k][2] in memberDict:
                                        print("\33[31m第"+str(tokens[k][0])+"行，标识符"+tokens[k][2]+"已经存在于记录"+tokens[j][2]+"的成员列表中，请修改错误后再进行语义分析")
                                        semanticErrorFlag=1;break
                                    memberDict.update({tokens[k][2]:'INTEGER'})
                                k+=1
                            if semanticErrorFlag==1:
                                break
                        elif tokens[k][1]=='CHAR':
                            while tokens[k][2]!=';':
                                if tokens[k][1]=='ID':
                                    if tokens[k][2] in memberDict:
                                        print("\33[31m第"+str(tokens[k][0])+"行，标识符"+tokens[k][2]+"已经存在于记录"+tokens[j][2]+"的成员列表中，请修改错误后再进行语义分析")
                                        semanticErrorFlag=1;break
                                    memberDict.update({tokens[k][2]:'CHAR'})
                                k+=1
                            if semanticErrorFlag==1:
                                break
                        elif tokens[k][1]=='ARRAY':
                            m=k
                            while tokens[k][2]!=';':
                                if tokens[k][1]=='ID':
                                    if tokens[k][2] in memberDict:
                                        print("\33[31m第"+str(tokens[k][0])+"行，标识符"+tokens[k][2]+"已经存在于记录"+tokens[j][2]+"的成员列表中，请修改错误后再进行语义分析")
                                        semanticErrorFlag=1;break
                                    memberDict.update({tokens[k][2]:('ARRAY',getType(tokens[m+7][2]),tokens[m+2][2],tokens[m+4][2])})
                                k+=1
                            if semanticErrorFlag==1:
                                break
                        k+=1
                    if semanticErrorFlag==1:
                        break
                    SymTab.append(Symbol(tokens[j][2], Level, 'TYPE', 'RECORD', None, None, None,None,memberDict))
        if flag==1:
            break
        if semanticErrorFlag==1:
            break
        continue
    elif tokens[i][1]=='VAR':
        j=i+1
        while tokens[j][1] not in ['PROCEDURE','BEGIN']:
            #先提取类型，再向符号表里添加表项
            nowType=None
            if tokens[j][1] != 'INTEGER' and tokens[j][1] != 'CHAR':
                for Sym in SymTab:
                    if Sym.name==tokens[j][2]:
                        nowType=Sym.type
                        break
            else:
                nowType=tokens[j][1]
            if nowType==None:
                if tokens[j][1] in ['ARRAY','RECORD']:#数组/记录后直接跟变量定义
                    nowType=tokens[j][1]
                else:
                    semanticErrorFlag=1
                    print("\33[31m第"+str(tokens[j][0])+"行，类型"+tokens[j][2]+"未定义，请修改错误后再进行语义分析")
                    break
            flag=0
            k=j+1
            while tokens[k][2]!=';':#统计到i+2后第一个;之前
                if tokens[j][1] not in['ARRAY','RECORD']:#INTEGER / CHAR / INTEGER或CHAR或ARRAY或RECORD的别名来定义变量
                    if(tokens[k][1]=='ID'):
                        if redefinition(tokens[k][2],Level)==1:
                            semanticErrorFlag = 1;flag = 1
                            print("\33[31m第" + str(tokens[k][0]) + "行，标识符" + tokens[k][2] + "重复定义，请修改错误后再进行语义分析")
                            break
                        if nowType=='ARRAY':#用数组别名定义数组
                            ElemType = None;Low = None;Up = None
                            for SymItem in SymTab:
                                if SymItem.name == tokens[j][2]:
                                    ElemType = SymItem.ElemType;Low = SymItem.Low;Up = SymItem.Up
                            SymTab.append(Symbol(tokens[k][2], Level, 'VAR', 'ARRAY', ElemType, Low, Up,None,None))
                            k+=1;continue
                        elif nowType=='RECORD':#用结构体别名定义结构体变量
                            SymTab.append(Symbol(tokens[k][2], Level, 'VAR', 'RECORD', tokens[j][2], None, None,None,returnSymItem(tokens[j][2]).MemberDict))
                            k += 1;continue
                        else:#常规变量定义
                            if redefinition(tokens[k][2],Level)==1:
                                semanticErrorFlag = 1;flag = 1
                                print("\33[31m第" + str(tokens[k][0]) + "行，变量标识符" + tokens[k][2] + "重复定义，请修改错误后再进行语义分析")
                                break
                            SymTab.append(Symbol(tokens[k][2],Level,'VAR',nowType,None,None,None,None,None))
                            k+=1;continue
                elif tokens[j][1]=='ARRAY':#数组不起别名直接跟定义
                    ElemType = getType(tokens[j+7][2]);Low = tokens[j+2][2];Up = tokens[j+4][2]
                    m=j+8
                    while tokens[m][2]!=';':
                        if tokens[m][1]=='ID':
                            if redefinition(tokens[m][2],Level)==1:
                                semanticErrorFlag = 1;flag = 1
                                print("\33[31m第" + str(tokens[m][0]) + "行，数组变量标识符" + tokens[m][2] + "重复定义，请修改错误后再进行语义分析")
                                break
                            SymTab.append(Symbol(tokens[m][2],Level,'VAR','ARRAY',ElemType,Low,Up,None,None))
                        m+=1
                    if semanticErrorFlag==1:
                        break
                    k=m;continue
                elif tokens[j][1]=='RECORD':#结构体不起别名直接跟定义
                    dictTemp={}
                    while tokens[k][1] != 'END':
                        if tokens[k][1] == 'INTEGER' and tokens[k - 1][1] != 'OF':
                            while tokens[k][2] != ';':
                                if tokens[k][1] == 'ID':
                                    if tokens[k][2] in dictTemp:
                                        print("\33[31m第"+str(tokens[k][0])+"行，标识符"+tokens[k][2]+"已经存在于当前记录的成员列表中，请修改错误后再进行语义分析")
                                        semanticErrorFlag=1;break
                                    dictTemp.update({tokens[k][2]: 'INTEGER'})
                                k += 1;continue
                            if semanticErrorFlag==1:
                                break
                        elif tokens[k][1] == 'CHAR':
                            while tokens[k][2] != ';':
                                if tokens[k][1] == 'ID':
                                    if tokens[k][2] in dictTemp:
                                        print("\33[31m第"+str(tokens[k][0])+"行，标识符"+tokens[k][2]+"已经存在于当前记录的成员列表中，请修改错误后再进行语义分析")
                                        semanticErrorFlag=1;break
                                    dictTemp.update({tokens[k][2]: 'CHAR'})
                                k += 1;continue
                            if semanticErrorFlag==1:
                                break
                        elif tokens[k][1] == 'ARRAY':
                            m = k
                            while tokens[k][2] != ';':
                                if tokens[k][1] == 'ID':
                                    if tokens[k][2] in dictTemp:
                                        print("\33[31m第"+str(tokens[k][0])+"行，标识符"+tokens[k][2]+"已经存在于当前记录的成员列表中，请修改错误后再进行语义分析")
                                        semanticErrorFlag=1;break
                                    dictTemp.update({tokens[k][2]: ('ARRAY', getType(tokens[m + 7][2]), tokens[m + 2][2], tokens[m + 4][2])})
                                k += 1;continue
                            if semanticErrorFlag==1:
                                break
                        k+=1
                    if semanticErrorFlag==1:
                        break
                    k+=1
                    while tokens[k][2]!=';':
                        if tokens[k][1]=='ID':
                            if redefinition(tokens[k][2],Level)==1:
                                semanticErrorFlag = 1;flag = 1
                                print("\33[31m第" + str(tokens[k][0]) + "行，记录变量标识符" + tokens[k][2] + "重复定义，请修改错误后再进行语义分析")
                                break
                            SymTab.append(Symbol(tokens[k][2],Level,'VAR','RECORD',None,None,None,None,dictTemp))
                        k+=1
                    if flag==1:
                        break
                    j=k+1;continue

                k+=1
            if semanticErrorFlag==1:
                break
            j=k+1
            if flag==1:
                break
        if semanticErrorFlag==1:
            break
        i=j;continue
    elif tokens[i][1]=='PROCEDURE':
        if(redefinition(tokens[i+1][2],Level)==1):
            semanticErrorFlag=1
            print("\33[31m第" + str(tokens[i+1][0]) + "行，过程标识符" + tokens[i+1][2] + "重复定义，请修改错误后再进行语义分析")
            break
        SymTab.append(Symbol(tokens[i + 1][2], Level, 'PROCEDURE', None, None, None, None, None, None))
        Level += 1
        parameterList=[]
        j=i+3
        while tokens[j][2] not in [';',')']:
            nowType = getType(tokens[j][2])
            if nowType==None:
                if tokens[j][1]=='VAR':
                    j+=1
                    continue
                print("\33[31m第" + str(tokens[j][0]) + "行，类型标识符" + tokens[j][2] + "未定义，请修改错误后再进行语义分析")
                semanticErrorFlag=1;break
            k = j+1
            while tokens[k][2] not in[';',')']:#统计一个类型后面所有的变量
                if tokens[k][1]=='ID':
                    parameterList.append(nowType)
                    SymTab.append(Symbol(tokens[k][2],Level,'VAR',nowType,None,None,None,None,None))
                k+=1
            j=k+1
        returnSymItem(tokens[i+1][2]).ParameterDict=parameterList
        if tokens[j][2]==')':
            i=j+2
        elif tokens[j][2]==';':
            i=j+1
        if semanticErrorFlag==1:
            break
        continue
    elif tokens[i][1]=='END':
        #想进行正常语义分析需要保留下行语句，注释掉则可以输出完整符号表
        #delNowLevel(Level)
        Level-=1
    elif tokens[i][1]=='BEGIN':#检查使用有关的错误
        j = i + 1
        while tokens[j][1]!='END':
            if(tokens[j][1]=='ID'):
                if '\'' not in tokens[j][2] and judgeDefine(tokens[j][2])==0:
                    if tokens[j-1][2]!='.':
                        semanticErrorFlag=1
                        print("\33[31m第"+str(tokens[j][0])+"行，标识符"+tokens[j][2]+"未定义就使用，请修改错误后再继续进行语义分析")
                        break
                    elif tokens[j][2] not in returnSymItem(tokens[j-2][2]).MemberDict:
                        print("\33[31m第" + str(tokens[j][0]) + "行，记录" + tokens[j-2][2] + "不存在成员" + tokens[j][2] + "，请修改错误后再继续进行语义分析")
                        semanticErrorFlag = 1;break
                if tokens[j+1][2]=='.':
                    item=returnSymItem(tokens[j][2])
                    if item.type!='RECORD':
                        print("\33[31m第" + str(tokens[j][0]) + "行，标识符" + tokens[j][2] + "不是记录体变量，请修改错误后再继续进行语义分析")
                        semanticErrorFlag = 1;break
                if tokens[j+1][2]=='[':#检查数组可能的相关错误
                    tempItem=returnSymItem(tokens[j][2])
                    Low=Up=0
                    if tempItem==None:
                        if returnSymItem(tokens[j-2][2]).type=='RECORD':#记录成员是一个数组
                            Low=(returnSymItem(tokens[j-2][2]).MemberDict[tokens[j][2]])[2]
                            Up=(returnSymItem(tokens[j-2][2]).MemberDict[tokens[j][2]])[3]
                    else:
                        if tempItem.Up==None and tempItem.Low==None:#常规数组
                            semanticErrorFlag = 1
                            print("\33[31m第" + str(tokens[j][0]) + "行，标识符" + str(tokens[j][2]) + "不是数组类型，请修改错误后再继续进行语义分析")
                            break
                        Low=returnSymItem(tokens[j][2]).Low
                        Up=returnSymItem(tokens[j][2]).Up
                    k=j+2
                    indexLen=0#只对用CONST访问数组的情况作越界检查
                    while tokens[k][2]!=']':
                        indexLen+=1
                        k+=1
                    if indexLen>1:
                        j+=1;continue
                    if tokens[j+2][1]=='ID':#用变量访问数组，直接跳过不作分析
                        j+=1;continue
                    if tokens[j+2][2]<Low or tokens[j+2][2]>Up:
                        semanticErrorFlag = 1
                        print("\33[31m第"+str(tokens[j+1][0])+"行，数组"+str(tokens[j][2])+"下标访问越界，请修改错误后再继续进行语义分析")
                        break
                elif tokens[j+1][2]=='(':#检查函数调用时参数的匹配问题
                    if returnSymItem(tokens[j][2]).kind!='PROCEDURE':
                        print("\33[31m第"+str(tokens[j][0])+"行，标识符"+str(tokens[j][2])+"不是过程标识符，请修改错误后再继续进行语义分析")
                        semanticErrorFlag=1;break
                    realParList=[]
                    formParList=returnSymItem(tokens[j][2]).ParameterDict
                    k=j+2
                    parmOverFlag=0
                    while tokens[k][2]!=')':#提取实参列表
                        m=k
                        flag=0
                        while tokens[m][2]!=',':
                            if tokens[m+1][2]==';' or tokens[m+1][1]=='END':
                                parmOverFlag=1
                                break
                            if tokens[m][1] == 'ID' and '\'' not in tokens[m][2] and tokens[m-1][2]!='.':
                                if judgeDefine(tokens[m][2]) == 0:
                                    print("\33[31m第" + str(tokens[k][0]) + "行，变量标识符" + tokens[k][2] + "未定义就使用，请修改错误后再继续进行语义分析")
                                    semanticErrorFlag = 1;break
                            if tokens[m+1][2]=='[' and tokens[m-1][2]!='.':#数组变量成员作实参
                                item=returnSymItem(tokens[m][2])
                                if item.type!='ARRAY':
                                    print("\33[31m第" + str(tokens[m][0]) + "行，标识符" + tokens[m][2] + "不是数组类型，请修改错误后再继续进行语义分析")
                                    semanticErrorFlag = 1;break
                                realParList.append(returnSymItem(tokens[m][2]).ElemType)
                            elif tokens[m+1][2]=='.':#结构体变量成员变量作实参
                                item=returnSymItem(tokens[m][2])
                                if item.type!='RECORD':
                                    print("\33[31m第" + str(tokens[m][0]) + "行，标识符" + tokens[m][2] + "不是记录体变量，请修改错误后再继续进行语义分析")
                                    semanticErrorFlag = 1;break
                                if tokens[m+2][2] in returnSymItem(tokens[m][2]).MemberDict:
                                    tempMember=(returnSymItem(tokens[m][2]).MemberDict)[tokens[m+2][2]]
                                else:
                                    tempMember=None
                                if tempMember==None:
                                    print("\33[31m第" + str(tokens[m][0]) + "行，记录" + tokens[m][2] + "不存在成员"+tokens[m+2][2]+"，请修改错误后再继续进行语义分析")
                                    semanticErrorFlag = 1;break
                                else:
                                    if type(tempMember)==tuple:
                                        realParList.append(tempMember[1])
                                    else:
                                        realParList.append(tempMember)
                            elif flag==0 and tokens[m][1] in ['ID','CONST'] and tokens[m-1][2] not in ['[','.']:#若实参是一个表达式，用第一个变量的类型作为整体类型
                                flag=1
                                realParList.append(name2type(tokens[m][2]))
                            m+=1
                        k=m+1
                        if semanticErrorFlag == 1:
                            break
                        if parmOverFlag==1:
                            break
                    #输出实参表
                    print(tokens[j][2]+':'+str(realParList))
                    if semanticErrorFlag==1:
                        break
                    if realParList!=formParList:
                        semanticErrorFlag = 1
                        if len(realParList)==len(formParList):
                            print("\33[31m第" + str(tokens[j][0]) + "行，调用" + str(tokens[j][2]) + "函数时形实参类型不匹配，请修改后再进行语义分析")
                        else:
                            print("\33[31m第" + str(tokens[j][0]) + "行，调用" + str(tokens[j][2]) + "函数时形实参个数不相同，请修改后再进行语义分析")
                        break
                    #j=k+1
                    #continue
            """*****************************增加**********************************"""
            SemanticChecker(*tokens, idx=j, isTree=False).tokenListCheck()
            """*****************************增加**********************************"""
            if semanticErrorFlag == 1:
                break
            j+=1
        if semanticErrorFlag==1:
            break
        i=j
        continue
    i += 1

printSymTab()

if semanticErrorFlag==0:
    print("\33[32m无语义错误")