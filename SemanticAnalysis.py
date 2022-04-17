'''
构造全局符号表，扫描完一层后删除当前层符号表
检查当前层内重复定义错误、
未定义就使用错误、
函数调用时参数类型及个数的匹配错误
'''
import LexicalAnalysis as tokens

class Symbol:#符号表元素
    def __init__(self,name,level,kind,type,ElemType,Low,Up):
        self.name=name
        self.level=level
        self.kind=kind
        self.type=type
        self.ElemType=ElemType
        self.Low=Low
        self.Up=Up

parameterDict={}#形参表

#print(tokens.obj.txt)
tokens=tokens.obj.tokens
#print(tokens)
SymTab=[]#元素是Sym对象
Level=0#当前层数
lineSkipNum=0

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

def name2type(name):#用于检查形实参是否匹配
    for Sym in SymTab:
        if Sym.kind == 'VAR' and Sym.name == name:
            return Sym.type
    if isinstance(name, int) == 1:
        return 'INTEGER'
    elif isinstance(name, str) == 1:
        return 'CHAR'

def returnSymItem(name):
    for Sym in SymTab:
        if Sym.name==name:
            return Sym

def outFormat(content):
    if content==None:
        return ''
    else:
        return str(content)

class SemanticError(Exception):
    def __init__(self, message, lineno):
        super().__init__(message, lineno)
        self.message = message
        self.lineno = lineno

class SemanticChecker:#功能5,6,7,10,11,12
    def __init__(self, *args, idx, isTree=False):
        self.tokenlist = args if not isTree else None
        self.root = args if isTree else None
        self.idx = idx

    '''
    getType调用还有问题
    '''
    def getType(self, name):
        if name.upper() in ['INTEGER', 'CHAR']:
            return name.upper()
        for Sym in SymTab:
            if Sym.kind == 'TYPE' and Sym.name == name:
                return Sym.type

    def getKind(self, name):
        if name.upper() in ['INTEGER', 'CHAR']:
            return name.upper()
        for Sym in SymTab:
            if Sym.name == name:
                return Sym.kind

    def getElementType(self, name):
        return self.getType(name)

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
            print(self.tokenlist[self.idx][2])
            print(self.getKind(self.tokenlist[self.idx][2]))
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
        if left == 'CONST' and right == 'CONST':
            return
        elif left == 'CONST' and self.getElementType(right) == 'INTEGER':
            return
        elif right == 'CONST' and self.getElementType(left) == 'INTEGER':
            return
        elif self.getElementType(left) == self.getElementType(right):
            return
        message = "if和while语句的条件判断部分不是bool型"
        raise SemanticError(message, self.tokenlist[self.idx][0])

    def tokenListCheck(self):
        # self.idx = 0
        # isbegin = False
        # while self.idx < len(self.tokenlist):
        #     if not isbegin:
        #         if not self.matchBegin():
        #             continue
        #         isbegin = True
        #     if self.tokenlist[self.idx][1] == 'ID':
        #         self.checkArrayMember()
        #         self.checkRecordMember()
        #         self.checkProcedureCall()
        #     if self.tokenlist[self.idx][2] == ':=':
        #         self.checkAssignment()
        #     if self.tokenlist[self.idx][2] in ['+', '-', '*', '/']:
        #         self.checkOperation()
        #     if self.tokenlist[self.idx][2] in ['=', '<']:
        #         self.checkCmparison()
        #     if self.matchEnd():
        #         isbegin = False
        #     self.idx += 1
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

semanticErrorFlag=0
lineSkipNum=[]
#print('\33[31m')#错误信息用红字输出
for i in range(len(tokens)):
    if(tokens[i][0] in lineSkipNum):
        continue
    if tokens[i][1]=='PROGRAM':
        SymTab.append(Symbol(tokens[i+1][2],Level,'PROGRAM',None,None,None,None))
        Level+=1
    elif tokens[i][1]=='TYPE':
        lineSkipNum=[tokens[i][0]]
        flag=0
        for j in range(i+1,len(tokens)):
            if tokens[j][1]=='VAR' or tokens[j][1]=='PROCEDURE' or tokens[j][1]=='BEGIN':#将跨行的类型别名也计入统计
                break
            lineSkipNum.append(tokens[j][0])
            if tokens[j][1]=='ID':
                if redefinition(tokens[j][2],Level)==1:
                    flag=1;semanticErrorFlag=1
                    print("\33[31m第"+str(tokens[j][0])+"行，标识符"+tokens[j][2]+"重复定义，请修改错误后再进行语义分析")
                    break
                SymTab.append(Symbol(tokens[j][2],Level,'TYPE',tokens[j+2][1],None,None,None))
        if flag==1:
            break
    elif tokens[i][1]=='VAR':
        lineSkipNum=[tokens[i][0]]
        nowType=None
        if tokens[i + 1][1] != 'INTEGER' and tokens[i + 1][1] != 'CHAR':
            for Sym in SymTab:
                if Sym.name==tokens[i+1][2]:
                    nowType=Sym.type
                    break
        else:
            nowType=tokens[i+1][1]
        if nowType==None:
            semanticErrorFlag=1
            print("\33[31m第"+str(tokens[i][0])+"行，类型"+tokens[i+1][2]+"未定义，请修改错误后再进行语义分析")
            break
        flag=0
        for j in range(i+2,len(tokens)):
            if(tokens[j][2]==';'):#统计到i后第一个;之前
                lineSkipNum.append(tokens[j][0])
                break
            lineSkipNum.append(tokens[j][0])
            if(tokens[j][1]=='ID'):
                if redefinition(tokens[j][2],Level)==1:
                    semanticErrorFlag = 1;flag = 1
                    print("\33[31m第" + str(tokens[j][0]) + "行，标识符" + tokens[j][2] + "重复定义，请修改错误后再进行语义分析")
                    break
                SymTab.append(Symbol(tokens[j][2],Level,'VAR',nowType,None,None,None))
        if flag==1:
            break
    elif tokens[i][1]=='ARRAY':
        lineSkipNum=[]
        for j in range(i,i+8):
            lineSkipNum.append(tokens[j][0])
        flag=0
        for j in range(i+8,len(tokens)):
            if tokens[j][2]==';':#统计到i后第一个;前为止
                lineSkipNum.append(tokens[j][0])
                break
            lineSkipNum.append(tokens[j][0])
            if tokens[j][1]=='ID':
                if redefinition(tokens[j][2], Level) == 1:
                    semanticErrorFlag = 1;flag = 1
                    print("\33[31m第" + str(tokens[j][0]) + "行，标识符" + tokens[j][2] + "重复定义，请修改错误后再进行语义分析")
                    break
                SymTab.append(Symbol(tokens[j][2], Level, 'VAR', 'ARRAY', tokens[i + 7][1],tokens[i+2][2],tokens[i+4][2]))
        if flag==1:
            break
    elif tokens[i][1]=='PROCEDURE':
        if(redefinition(tokens[i+1][2],Level)==1):
            semanticErrorFlag=1
            print("\33[31m第" + str(tokens[i+1][0]) + "行，标识符" + tokens[i+1][2] + "重复定义，请修改错误后再进行语义分析")
            break
        SymTab.append(Symbol(tokens[i+1][2],Level,'PROCEDURE',None,None,None,None))
        parameterDict.update({tokens[i+1][2]:[]})
        for j in range(i+3,len(tokens)):
            if tokens[j][2]==')':
                break
            if tokens[j+1][1]=='ID' and tokens[j][2]!=';':
                parameterDict[tokens[i+1][2]].append(getType(tokens[j][2]))
        Level+=1
    elif getType(str(tokens[i][2])) in ['INTEGER','CHAR']:#函数参数
        if(redefinition(tokens[i+1][2],Level)==1):
            semanticErrorFlag=1
            print("\33[31m第" + str(tokens[i+1][0]) + "行，标识符" + tokens[i+1][2] + "重复定义，请修改错误后再进行语义分析")
            break
        SymTab.append(Symbol(tokens[i+1][2],Level,'VAR',getType(tokens[i][2]),'None',None,None))
    elif tokens[i][1]=='END':
        #想进行正常语义分析需要保留下行语句，删了则可以输出完整符号表
        #delNowLevel(Level)
        Level-=1
    elif tokens[i][1]=='BEGIN':
        lineSkipNum=[]
        lineSkipNum.append(tokens[i][0])
        j = i + 1
        flag=0
        while tokens[j][1]!='END':
            lineSkipNum.append(tokens[j][0])
            if(tokens[j][1]=='ID'):
                if judgeDefine(tokens[j][2])==0:
                    semanticErrorFlag=1;flag=1
                    print("\33[31m第"+str(tokens[j][0])+"行，标识符"+tokens[j][2]+"未定义就使用，请修改错误后再继续进行语义分析")
                    break
                if tokens[j+1][2]=='[':#检查数组可能的相关错误
                    if returnSymItem(tokens[j][2]).Up==None and returnSymItem(tokens[j][2]).Low==None:
                        semanticErrorFlag = 1;flag = 1
                        print("\33[31m第" + str(tokens[j][0]) + "行，标识符" + str(tokens[j][2]) + "不是数组类型，请修改错误后再继续进行语义分析")
                        break
                    if tokens[j+2][1]=='ID':#用变量访问数组，直接跳过不作分析
                        j+=1
                        continue
                    if tokens[j+2][2]<returnSymItem(tokens[j][2]).Low or tokens[j+2][2]>returnSymItem(tokens[j][2]).Up:
                        semanticErrorFlag = 1;flag=1
                        print("\33[31m第"+str(tokens[j+1][0])+"行，数组"+str(tokens[j][2])+"下标越界,请修改错误后再继续进行语义分析")
                        break
                elif tokens[j][2] in parameterDict:#检查函数调用时参数的匹配问题
                    realParList=[]
                    k=j+2
                    while tokens[k][2]!=')':#提取实参列表
                        if tokens[k][1]=='ID' and judgeDefine(tokens[k][2])==1:
                            realParList.append(name2type(tokens[k][2]))
                        elif tokens[k][1]=='CONST':
                            realParList.append(name2type(tokens[k][2]))
                        k+=1
                    if realParList!=parameterDict[tokens[j][2]]:
                        semanticErrorFlag = 1;flag=1
                        if len(realParList)==len(parameterDict):
                            print("\33[31m第" + str(tokens[j][0]) + "行，调用" + str(tokens[j][2]) + "函数时形实参个数不相同，请修改后再进行语义分析")
                        else:
                            print("\33[31m第" + str(tokens[j][0]) + "行，调用" + str(tokens[j][2]) + "函数时形实参类型不匹配，请修改后再进行语义分析")
                        break
            tokenlist1 = tokens
            checker = SemanticChecker(*tokenlist1, idx=j, isTree=False)
            checker.tokenListCheck()
            if flag==1:
                break
            j+=1
        lineSkipNum.append(tokens[j][0])
        if semanticErrorFlag==1:
            break

print("\33[34m{0:<15}{1:<15}{2:<15}{3:<15}{4:<15}{5:<15}{6:<15}".format("name", "level","kind","type","ElemType","Low","Up"))
for i in SymTab:
    print('\33[34m{0:<15}{1:<15}{2:<15}{3:<15}{4:<15}{5:<15}{6:<15}'.format(outFormat(i.name), outFormat(i.level),outFormat(i.kind),outFormat(i.type),outFormat(i.ElemType),outFormat(i.Low),outFormat(i.Up)))

print("\33[31m形参表：")
print(parameterDict)

if semanticErrorFlag==0:
    print("\33[30m无语义错误")
