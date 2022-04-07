'''
构造全局符号表，扫描完一层后删除当前层符号表
检查当前层内重复定义错误、未定义就使用错误
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

print(tokens.code2)
tokens=tokens.obj.tokens
print(tokens)
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

def returnSymItem(name):
    for Sym in SymTab:
        if Sym.name==name:
            return Sym

def outFormat(content):
    if content==None:
        return ''
    else:
        return str(content)

semanticErrorFlag=0
lineSkipNum=[]
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
                    print("第"+str(tokens[j][0])+"行，标识符"+tokens[j][2]+"重复定义，请修改错误后再进行语义分析")
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
            print("第"+str(tokens[i][0])+"行，类型"+tokens[i+1][2]+"未定义，请修改错误后再进行语义分析")
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
                    print("第" + str(tokens[j][0]) + "行，标识符" + tokens[j][2] + "重复定义，请修改错误后再进行语义分析")
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
                    print("第" + str(tokens[j][0]) + "行，标识符" + tokens[j][2] + "重复定义，请修改错误后再进行语义分析")
                    break
                SymTab.append(Symbol(tokens[j][2], Level, 'VAR', 'ARRAY', tokens[i + 7][1],tokens[i+2][2],tokens[i+4][2]))
        if flag==1:
            break
    elif tokens[i][1]=='PROCEDURE':
        if(redefinition(tokens[i+1][2],Level)==1):
            semanticErrorFlag=1
            print("第" + str(tokens[i+1][0]) + "行，标识符" + tokens[i+1][2] + "重复定义，请修改错误后再进行语义分析")
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
            print("第" + str(tokens[i+1][0]) + "行，标识符" + tokens[i+1][2] + "重复定义，请修改错误后再进行语义分析")
            break
        SymTab.append(Symbol(tokens[i+1][2],Level,'VAR',getType(tokens[i][2]),'None',None,None))
    elif tokens[i][1]=='END':
        #想进行正常语义分析需要保留下行语句，删了则可以输出完整符号表
        #delNowLevel(Level)
        Level-=1
    elif tokens[i][1]=='BEGIN':
        lineSkipNum=[]
        j=i+1
        flag=0
        while tokens[j][1]!='END':
            lineSkipNum.append(tokens[j][0])
            if(tokens[j][1]=='ID'):
                if judgeDefine(tokens[j][2])==0:
                    semanticErrorFlag=1;flag=1
                    print("第"+str(tokens[j][0])+"行，标识符"+tokens[j][2]+"未定义就使用，请修改错误后再继续进行语义分析")
                    break
                if tokens[j+1][2]=='[':
                    if tokens[j+2][2]<returnSymItem(tokens[j][2]).Low or tokens[j+2][2]>returnSymItem(tokens[j][2]).Up:
                        semanticErrorFlag = 1;flag=1
                        print("第"+str(tokens[j+1][0])+"行，数组"+str(tokens[j][2])+"下标越界,请修改错误后再继续进行语义分析")
                        break
            if flag==1:
                break
            j+=1

print("\33[34m{0:<15}{1:<15}{2:<15}{3:<15}{4:<15}{5:<15}{6:<15}".format("name", "level","kind","type","ElemType","Low","Up"))
for i in SymTab:
    print('\33[34m{0:<15}{1:<15}{2:<15}{3:<15}{4:<15}{5:<15}{6:<15}'.format(outFormat(i.name), outFormat(i.level),outFormat(i.kind),outFormat(i.type),outFormat(i.ElemType),outFormat(i.Low),outFormat(i.Up)))

print("\33[31m形参表：")
print(parameterDict)

if semanticErrorFlag==0:
    print("\33[30m无语义错误")