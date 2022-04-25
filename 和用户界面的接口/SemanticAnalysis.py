'''
构造全局符号表，扫描完一层后删除当前层符号表
检查当前层内重复定义错误、
未定义就使用错误、
函数调用时参数类型及个数的匹配错误
'''
import LexicalAnalysis as LA

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
tokens=LA.startLexAnalysis(LA.codeInput)
if tokens == None:  # 表明有词法错误
    exit()
scanTokenList=[]#辅助获取符号表，标记扫描过了的token
for i in tokens:
    scanTokenList.append(0)
#print(len(tokens))
#print(len(scanTokenList))
SymTab=[]#元素是Sym对象
recordSym={}#记录表
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
    return None

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
        return ""
    else:
        return str(content)

semanticErrorFlag=0
#print('\33[31m')#错误信息用红字输出
i=0
while tokens[i][1]!='EOF':
    if tokens[i][1]=='PROGRAM':
        SymTab.append(Symbol(tokens[i+1][2],Level,'PROGRAM',None,None,None,None))
        Level+=1
        i += 2;continue
    elif tokens[i][1]=='TYPE':#类型别名，记录的定义
        flag=0
        for j in range(i+1,len(tokens)):
            if tokens[j][1] in ['VAR','PROCEDURE','BEGIN']:#统计所有类型
                i=j
                break
            if tokens[j][1]=='ID' and tokens[j+1][2]=='=':
                if redefinition(tokens[j][2],Level)==1:
                    flag=1;semanticErrorFlag=1
                    print("\33[31m第"+str(tokens[j][0])+"行，标识符"+tokens[j][2]+"重复定义，请修改错误后再进行语义分析")
                    break

                if tokens[j+2][1]=='ARRAY':
                    SymTab.append(Symbol(tokens[j][2],Level,'TYPE','ARRAY',getType(tokens[j+9][2]),tokens[j+4][2],tokens[j+6][2]))
                elif tokens[j+2][1]!='RECORD':
                    SymTab.append(Symbol(tokens[j][2],Level,'TYPE',getType(tokens[j+2][2]),None,None,None))
                else:#记录类型的别名
                    SymTab.append(Symbol(tokens[j][2],Level,'TYPE','RECORD',None,None,None))
                    recordSym.update({tokens[j][2]:{}})
                    k=j+3
                    while tokens[k][1]!='END':
                        if tokens[k][1]=='INTEGER' and tokens[k-1][1]!='OF':
                            while tokens[k][2]!=';':
                                if tokens[k][1]=='ID':
                                    recordSym[tokens[j][2]].update({tokens[k][2]:'INTEGER'})
                                k+=1
                        elif tokens[k][1]=='CHAR':
                            while tokens[k][2]!=';':
                                if tokens[k][1]=='ID':
                                    recordSym[tokens[j][2]].update({tokens[k][2]:'CHAR'})
                                k+=1
                        elif tokens[k][1]=='ARRAY':
                            m=k
                            while tokens[k][2]!=';':
                                if tokens[k][1]=='ID':
                                    recordSym[tokens[j][2]].update({tokens[k][2]:('ARRAY',getType(tokens[m+7][2]),tokens[m+2][2],tokens[m+4][2])})
                                k+=1
                        k+=1
        if flag==1:
            break
        continue
    elif tokens[i][1]=='VAR':
        j=i+1
        while tokens[j][1] not in ['VAR','ARRAY','PROCEDURE','BEGIN']:
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
                semanticErrorFlag=1
                print("\33[31m第"+str(tokens[j][0])+"行，类型"+tokens[j][2]+"未定义，请修改错误后再进行语义分析")
                break
            flag=0
            for k in range(j+1,len(tokens)):
                if(tokens[k][2]==';'):#统计到i+2后第一个;之前
                    j=k+1
                    break
                if(tokens[k][1]=='ID'):
                    if redefinition(tokens[k][2],Level)==1:
                        semanticErrorFlag = 1;flag = 1
                        print("\33[31m第" + str(tokens[k][0]) + "行，标识符" + tokens[k][2] + "重复定义，请修改错误后再进行语义分析")
                        break
                    if nowType=='ARRAY':
                        ElemType=None;Low=None;Up=None
                        for SymItem in SymTab:
                            if SymItem.name==tokens[j][2]:
                                ElemType=SymItem.ElemType;Low=SymItem.Low;Up=SymItem.Up
                        SymTab.append(Symbol(tokens[k][2],Level,'VAR','ARRAY',ElemType,Low,Up))
                    elif nowType=='RECORD':
                        SymTab.append(Symbol(tokens[k][2], Level, 'VAR', 'RECORD', tokens[j][2], None, None))
                    else:
                        SymTab.append(Symbol(tokens[k][2],Level,'VAR',nowType,None,None,None))
            if flag==1:
                break
        if semanticErrorFlag==1:
            break
        i=j;continue
    elif tokens[i][1]=='ARRAY':
        for j in range(i+8,len(tokens)):
            if tokens[j][2]==';':#统计到i后第一个;前为止
                i=j+1
                break
            if tokens[j][1]=='ID':
                if redefinition(tokens[j][2], Level) == 1:
                    semanticErrorFlag = 1
                    print("\33[31m第" + str(tokens[j][0]) + "行，标识符" + tokens[j][2] + "重复定义，请修改错误后再进行语义分析")
                    break
                SymTab.append(Symbol(tokens[j][2], Level, 'VAR', 'ARRAY', tokens[i + 7][1],tokens[i+2][2],tokens[i+4][2]))
        if semanticErrorFlag==1:
            break
        continue
    elif tokens[i][1]=='PROCEDURE':
        if(redefinition(tokens[i+1][2],Level)==1):
            semanticErrorFlag=1
            print("\33[31m第" + str(tokens[i+1][0]) + "行，标识符" + tokens[i+1][2] + "重复定义，请修改错误后再进行语义分析")
            break
        SymTab.append(Symbol(tokens[i+1][2],Level,'PROCEDURE',None,None,None,None))
        Level += 1
        parameterDict.update({tokens[i+1][2]:[]})
        j=i+3
        while tokens[j][2]!=';':
            nowType = getType(tokens[j][2])
            if nowType==None:
                if tokens[j][1]=='VAR':
                    j+=1
                    continue
                print("\33[31m第" + str(tokens[j][0]) + "行，类型标识符" + tokens[j][2] + "未定义，请修改错误后再进行语义分析")
                semanticErrorFlag=1;break
            k = j
            while tokens[k][2] not in[';',')']:#统计一个类型后面所有的变量
                if tokens[k][1]=='ID':
                    parameterDict[tokens[i+1][2]].append(nowType)
                    SymTab.append(Symbol(tokens[k][2],Level,'VAR',nowType,None,None,None))
                k+=1
            j=k+1
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
                    semanticErrorFlag=1
                    print("\33[31m第"+str(tokens[j][0])+"行，标识符"+tokens[j][2]+"未定义就使用，请修改错误后再继续进行语义分析")
                    break
                if tokens[j+1][2]=='[':#检查数组可能的相关错误
                    if returnSymItem(tokens[j][2]).Up==None and returnSymItem(tokens[j][2]).Low==None:
                        semanticErrorFlag = 1
                        print("\33[31m第" + str(tokens[j][0]) + "行，标识符" + str(tokens[j][2]) + "不是数组类型，请修改错误后再继续进行语义分析")
                        break
                    if tokens[j+2][1]=='ID':#用变量访问数组，直接跳过不作分析
                        j+=1
                        continue
                    if tokens[j+2][2]<returnSymItem(tokens[j][2]).Low or tokens[j+2][2]>returnSymItem(tokens[j][2]).Up:
                        semanticErrorFlag = 1
                        print("\33[31m第"+str(tokens[j+1][0])+"行，数组"+str(tokens[j][2])+"下标越界,请修改错误后再继续进行语义分析")
                        break
                elif tokens[j+1][2]=='(' and tokens[j][2] in parameterDict:#检查函数调用时参数的匹配问题
                    realParList=[]
                    k=j+2
                    parmOverFlag=0
                    while tokens[k][2]!=')':#提取实参列表
                        m=k
                        flag=0
                        while tokens[m][2]!=',':
                            if tokens[m+1][2]==';' or tokens[m+1][1]=='END':
                                parmOverFlag=1
                                break
                            if tokens[m][1] == 'ID' and '\'' not in tokens[m][2]:
                                if judgeDefine(tokens[m][2]) == 0:
                                    print("\33[31m第" + str(tokens[k][0]) + "行，变量标识符" + tokens[k][2] + "未定义就使用，请修改错误后再继续进行语义分析")
                                    semanticErrorFlag = 1;break
                            if flag==0 and tokens[m][1] in ['ID','CONST']:#若实参是一个表达式，用第一个变量的类型作为整体类型
                                flag=1
                                realParList.append(name2type(tokens[m][2]))
                            m+=1
                        k=m+1
                        if semanticErrorFlag == 1:
                            break
                        if parmOverFlag==1:
                            break
                    #print(realParList)
                    if semanticErrorFlag==1:
                        break
                    if realParList!=parameterDict[tokens[j][2]]:
                        semanticErrorFlag = 1
                        if len(realParList)==len(parameterDict):
                            print("\33[31m第" + str(tokens[j][0]) + "行，调用" + str(tokens[j][2]) + "函数时形实参个数不相同，请修改后再进行语义分析")
                        else:
                            print("\33[31m第" + str(tokens[j][0]) + "行，调用" + str(tokens[j][2]) + "函数时形实参类型不匹配，请修改后再进行语义分析")
                        break
                    #j=k+1
                    #continue
            j+=1
        if semanticErrorFlag==1:
            break
        i=j
        continue
    i += 1

print("\33[31m---------------------------------------符号表：-----------------------------------------------")
print("\33[31m{0:<15}{1:<15}{2:<15}{3:<15}{4:<15}{5:<15}{6:<15}".format("name", "level","kind","type","ElemType","Low","Up"))
for i in SymTab:
    print('\33[34m{0:<15}{1:<15}{2:<15}{3:<15}{4:<15}{5:<15}{6:<15}'.format(outFormat(i.name), outFormat(i.level),outFormat(i.kind),outFormat(i.type),outFormat(i.ElemType),outFormat(i.Low),outFormat(i.Up)))

print("\33[31m形参表：\33[34m")
print(parameterDict)

print("\33[31m记录表：\33[34m")
print(recordSym)

if semanticErrorFlag==0:
    print("\33[32m无语义错误")
