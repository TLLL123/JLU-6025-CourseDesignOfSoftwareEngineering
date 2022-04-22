import LexicalAnalysis as tokens
from graphviz import Digraph
#将树可视化参考链接：http://www.graphviz.org/doc/info/shapes.html

class GrammaticalAnalysis_LL1:
    TERMINAL=[
        'PROGRAM','ID','TYPE','INTEGER','CHAR','ARRAY','OF','INTC','RECORD','END',
        'VAR','PROCEDURE','BEGIN','IF','THEN','ELSE','FI','WHILE','DO','ENDWH',
        'READ','WRITE','RETURN','+','-','*','/','(',')','[',']',',',';',':=','=','..','>','<','.'
    ]

    LL1Table={
        'Program': {'PROGRAM': ['ProgramHead', 'DeclarePart', 'ProgramBody']},
        'ProgramHead': {'PROGRAM': ['PROGRAM', 'ProgramName']},
        'ProgramName': {'ID': ['ID']},
        'DeclarePart':{'TYPE':['TypeDecpart','VarDecpart','ProcDecpart'],'VAR':['TypeDecpart','VarDecpart','ProcDecpart'],'PROCEDURE':['TypeDecpart','VarDecpart','ProcDecpart'],'BEGIN':['TypeDecpart','VarDecpart','ProcDecpart']},
        'TypeDecpart': {'VAR': [], 'PROCEDURE': [], 'BEGIN': [],
                        'TYPE': ['TypeDec']},
        'TypeDec': {'TYPE': ['TYPE', 'TypeDecList']},
        'TypeDecList': {'ID': ['TypeId', '=', 'TypeDef', ';', 'TypeDecMore']},
        'TypeDecMore': {'VAR': [], 'PROCEDURE':[], 'BEGIN':[],
                        'ID': ['TypeDecList']},#不同
        'TypeId': {'ID': ['ID']},
        'TypeDef': {'INTEGER': ['BaseType'], 'CHAR': ['BaseType'],
                    'ARRAY': ['StructureType'],'RECORD': ['StructureType'],
                    'ID': ['ID'],},
        'BaseType': {'INTEGER': ['INTEGER'],
                     'CHAR': ['CHAR']},
        'StructureType': {'ARRAY': ['ArrayType'],
                          'RECORD': ['RecType']},
        'ArrayType': {'ARRAY': ['ARRAY', '[', 'Low', '..', 'Top', ']', 'OF', 'BaseType']},
        'Low': {'INTC': ['INTC']},
        'Top': {'INTC': ['INTC']},
        'RecType': {'RECORD': ['RECORD', 'FieldDecList', 'END']},
        'FieldDecList': {'INTEGER': ['BaseType', 'IdList', ';', 'FieldDecMore'],'CHAR': ['BaseType', 'IdList', ';', 'FieldDecMore'],
                         'ARRAY': ['ArrayType', 'IdList', ';', 'FieldDecMore']},
        'FieldDecMore': {'END': [],
                         'INTEGER': ['FieldDecList'], 'CHAR': ['FieldDecList'], 'ARRAY': ['FieldDecList']},
        'IdList': {'ID': ['ID', 'IdMore']},
        'IdMore': {';': [],
                   ',': [',', 'IdList']},
        'VarDecpart':{'PROCEDURE':[],'BEGIN':[],
                      'VAR':['VarDec']},#不同
        'VarDec': {'VAR': ['VAR', 'VarDecList']},
        'VarDecList': {'INTEGER': ['TypeDef', 'VarIdList', ';', 'VarDecMore'],'CHAR': ['TypeDef', 'VarIdList', ';', 'VarDecMore'],'ARRAY': ['TypeDef', 'VarIdList', ';', 'VarDecMore'],'RECORD': ['TypeDef', 'VarIdList', ';', 'VarDecMore'],'ID': ['TypeDef', 'VarIdList', ';', 'VarDecMore'],},
        'VarDecMore': {'PROCEDURE': [], 'BEGIN': [],
                       'INTEGER': ['VarDecList'], 'CHAR': ['VarDecList'], 'ARRAY': ['VarDecList'],'RECORD': ['VarDecList'],'ID': ['VarDecList']},#不同
        'VarIdList': {'ID': ['ID', 'VarIdMore']},
        'VarIdMore': {';': [],
                      ',': [',', 'VarIdList']},#不同
        'ProcDecpart': {'BEGIN': [],
                        'PROCEDURE': ['ProcDec']},#不同
        'ProcDec': {'PROCEDURE': ['PROCEDURE', 'ProcName', '(', 'ParamList', ')', ';', 'ProcDecPart', 'ProcBody','ProcDecMore']},
        'ProcDecMore': {'BEGIN': [],
                        'PROCEDURE': ['ProcDec']},
        'ProcName': {'ID': ['ID']},
        'ParamList': {')': [],
                      'VAR': ['ParamDecList'], 'INTEGER': ['ParamDecList'], 'CHAR': ['ParamDecList'],'ARRAY': ['ParamDecList'], 'RECORD': ['ParamDecList'], 'ID': ['ParamDecList']},
        'ParamDecList': {'VAR': ['Param', 'ParamMore'], 'INTEGER': ['Param', 'ParamMore'],'CHAR': ['Param', 'ParamMore'], 'ARRAY': ['Param', 'ParamMore'],'RECORD': ['Param', 'ParamMore'], 'ID': ['Param', 'ParamMore']},
        'ParamMore': {')': [],
                      ';': [';', 'ParamDecList']},
        'Param': {'INTEGER': ['TypeDef', 'FormList'],'CHAR': ['TypeDef', 'FormList'], 'ARRAY': ['TypeDef', 'FormList'], 'RECORD': ['TypeDef', 'FormList'],'ID': ['TypeDef', 'FormList'],
                  'VAR': ['VAR', 'TypeDef', 'FormList']},
        'FormList': {'ID': ['ID', 'FidMore'],},#不同
        'FidMore': {';': [], ')': [],
                    ',': {',', 'FormList'}},
        'ProcDecPart':{'TYPE':['DeclarePart'],'VAR':['DeclarePart'],'PROCEDURE':['DeclarePart'],'BEGIN':['DeclarePart']},
        'ProcBody': {'BEGIN': ['ProgramBody']},
        'ProgramBody': {'BEGIN': ['BEGIN', 'StmList', 'END']},
        'StmList': {'ID': ['Stm', 'StmMore'], 'IF': ['Stm', 'StmMore'], 'WHILE': ['Stm', 'StmMore'],
                    'RETURN': ['Stm', 'StmMore'],'READ': ['Stm', 'StmMore'], 'WRITE': ['Stm', 'StmMore']},
        'StmMore': {'END': [], 'ELSE': [], 'FI': [], 'ENDWH': [],
                    ';': [';', 'StmList']},
        'Stm': {'IF': ['ConditionalStm'],
                'WHILE': ['LoopStm'],
                'READ': ['InputStm'],
                'WRITE': ['OutputStm'],
                'RETURN': ['ReturnStm'],
                'ID': ['ID', 'AssCall']},
        'AssCall': {':=': ['AssignmentRest'], '.': ['AssignmentRest'], '[': ['AssignmentRest'],
                    '(': ['CallStmRest']},#不同
        'AssignmentRest': {'[': ['VariMore', ':=', 'Exp'], ':=': ['VariMore', ':=', 'Exp'],'.': ['VariMore', ':=', 'Exp']},#不同
        'ConditionalStm': {'IF': ['IF', 'RelExp', 'THEN', 'StmList', 'ELSE', 'StmList', 'FI']},
        'LoopStm': {'WHILE': ['WHILE', 'RelExp', 'DO', 'StmList', 'ENDWH']},
        'InputStm': {'READ': ['READ', '(', 'Invar', ')']},
        'Invar':{'ID':['ID']},
        'OutputStm': {'WRITE': ['WRITE', '(', 'Exp', ')']},
        'ReturnStm': {'RETURN': ['RETURN', '(', 'Exp', ')']},#不同
        'CallStmRest': {'(': ['(', 'ActParamList', ')']},
        'ActParamList': {')': [],
                         '(': ['Exp', 'ActParamMore'],'INTC': ['Exp', 'ActParamMore'], 'ID': ['Exp', 'ActParamMore']},
        'ActParamMore': {')': [],
                         ',': [',', 'ActParamList']},
        'RelExp': {'(': ['Exp', 'OtherRelE'], 'INTC': ['Exp', 'OtherRelE'], 'ID': ['Exp', 'OtherRelE']},
        'OtherRelE': {'<': ['CmpOp', 'Exp'], '=': ['CmpOp', 'Exp']},#不同
        'Exp': {'(': ['Term', 'OtherTerm'], 'INTC': ['Term', 'OtherTerm'],'ID': ['Term', 'OtherTerm']},
        'OtherTerm': {'<': [], '=': [],']': [],'THEN': [], 'ELSE': [], 'FI': [],'DO': [], 'ENDWH': [],')': [], 'END': [], ';': [], ',': [],
                      '+': ['AddOp', 'Exp'], '-': ['AddOp', 'Exp']},
        'Term': {'(': ['Factor', 'OtherFactor'], 'INTC': ['Factor', 'OtherFactor'], 'ID': ['Factor', 'OtherFactor']},
        'OtherFactor': {'+': [], '-': [],'<': [], '=': [],']': [],'THEN': [],'ELSE': [], 'FI': [],'DO': [], 'ENDWH': [], ')':[], 'END':[], ';': [], ',': [],
                        '*': ['MultOp', 'Term'], '/': ['MultOp', 'Term']},
        'Factor': {'(': ['(', 'Exp', ')'],
                   'INTC': ['INTC'],
                   'ID': ['Variable']},
        'Variable': {'ID': ['ID', 'VariMore']},
        'VariMore': {':=': [],'*': [], '/': [],'+': [], '-': [], '<': [], '=': [], 'THEN': [],'ELSE': [],'FI':[],'DO': [],'ENDWH':[],')': [],'END':[],';': [],',': [],']':[],
                     '[': ['[', 'Exp', ']'],
                     '.': ['.', 'FieldVar']},
        'FieldVar': {'ID': ['ID', 'FieldVarMore']},
        'FieldVarMore': {':=': [],'*': [], '/': [],'+': [], '-': [], '<': [], '=': [], 'THEN': [],'ELSE': [],'FI':[],'DO': [],'ENDWH':[],')': [],'END':[],';': [],',': [],']':[],
                         '[': ['[', 'Exp', ']']},#不同
        'CmpOp': {'<': ['<'],
                  '=': ['=']},
        'AddOp': {'+': ['+'],
                  '-': ['-']},
        'MultOp': {'*': ['*'],
                   '/': ['/']},
    }

    reverseMap={
                        'EQ': '='  ,   'LT': '<'       , 'PLUS': '+'     , 'MINUS': '-',
        'TIMES': '*'  , 'OVER': '/',   'LPAREN': '['   , 'RPAREN': ']'   , 'DOT': '.',
                        'SEMI': ';',   'COMMA': ','    , 'LMIDPAREN': '(', 'RMIDPAREN': ')',
        'CONST':'INTC', 'ASSIGN':':=', 'UNDERANGE':'..',
    }
    flag=0#有语法错误则修改为1

    def __init__(self,root):
        self.root=root
        self.matchTags=[]#记录所有终极符结点的序号

    def analysis(self,code_list,wordlist,linenum_list,root):
        nodeCount=1
        ana_list = [root]  # 分析栈初始状态
        LL1Table = self.LL1Table
        pdeal = 0  # 输入流当前处理到了哪
        #print('\n\33[34m{0:<46}\33[31m|{1:<50}'.format("输入流当前单词", "分析栈"))
        tempChildren = []
        for i in ana_list:tempChildren.append(i.data)
        #print('\33[34m{0:<50}\33[31m|{1:<50}'.format('', str(tempChildren)))
        matchTags=self.matchTags

        while True:
            if ana_list == [] and pdeal==len(code_list)-2 and code_list[pdeal]=='.' and code_list[pdeal+1]=='EOF':
                print('\33[32m{0:<50}'.format("无语法错误"))
                break
            else:
                if pdeal>=len(code_list):
                    #print("请检查输入，输入不能为空")
                    self.flag=1
                    break
                # 分析栈顶为终极符且与输入流当前值相同
                elif ana_list[0].data==code_list[pdeal]:
                    ana_list[0].word=wordlist[pdeal]

                    pdeal += 1
                    matchTags.append(ana_list[0].tag)
                    ana_list.pop(0)

                    tempChildren = []
                    for i in ana_list:tempChildren.append(i.data)
                    #print('\33[32m{0:<50}\33[33m|{1:<50}'.format("MATCH:"+str(code_list[pdeal-1]),str(tempChildren)))
                # 分析栈顶为非终极符，查表用相应产生式右部进行替换
                elif ana_list[0].data in LL1Table and code_list[pdeal] in LL1Table[ana_list[0].data]:
                    fatherNode=ana_list[0]
                    i = 1
                    for item in LL1Table[ana_list[0].data][code_list[pdeal]]:
                        nodeCount+=1
                        sonNode=Node([],item,nodeCount,None)
                        fatherNode.children.append(sonNode)

                        ana_list.insert(i, sonNode)
                        i += 1
                    if(i==1):#产生式右部为空
                        nodeCount+=1
                        sonNode=Node([],"ε",nodeCount,None)
                        fatherNode.children.append(sonNode)

                    ana_list.pop(0)

                    tempChildren=[]
                    for i in ana_list:tempChildren.append(i.data)
                    #print('\33[34m{0:<50}\33[31m|{1:<50}'.format(str(code_list[pdeal]),str(tempChildren)))
                # 出现语法错误
                else:
                    self.flag=1
                    #print("\33[31mLL(1)分析中断，第" + str(linenum_list[pdeal]) + "行单词" + str(wordlist[pdeal]) + "出现语法错误")
                    break
        return self.flag

class Node:
    def __init__(self,children,data,tag,word):
        self.children=children
        self.data=data#记录对应的终极符
        self.tag=tag
        self.word=word#记录对应的单词，仅叶节点才有

def drawTree(root,matchTags):
    dot = Digraph(comment='Tree')
    def connectNode(node):
        if(len(node.children)>0):
            for child in node.children:
                if(child.tag in matchTags):
                    dot.node(str(child.tag), child.data+'---'+str(child.word), shape='plaintext',fontcolor='crimson')
                else:
                    dot.node(str(child.tag),child.data,shape='plaintext')
                dot.edge(str(node.tag),str(child.tag),arrowshape='none')
                connectNode(child)#递归
    dot.node(str(root.tag),root.data,shape='plaintext')
    connectNode(root)
    dot.render('SyntaxTree-output/SyntaxTree', view=True)

def startDrawTree():
    obj_tokens = tokens.startLexAnalysis(tokens.codeInput)
    if obj_tokens == None:#表明有词法错误
        exit()
    codelist = []  # 单词对应的终极符序列
    linenumlist = []  # 标志每个单词所在的行号
    wordlist = []  # 单词序列
    for i in obj_tokens:
        if i[1] in GrammaticalAnalysis_LL1.reverseMap:
            codelist.append(GrammaticalAnalysis_LL1.reverseMap[i[1]])
        else:
            codelist.append(i[1])
        wordlist.append(i[2])
        linenumlist.append(i[0])
    root = Node([], 'Program', 1, None)
    obj_LL1 = GrammaticalAnalysis_LL1(root)
    obj_LL1.flag = obj_LL1.analysis(codelist, wordlist, linenumlist, root)  # 从语法树根结点开始做语法分析
    if (obj_LL1.flag == 1):
        print("\33[30m请按提示修改语法错误后，再尝试进行语法分析并生成语法树")
        exit()
    else:
        drawTree(root, obj_LL1.matchTags)
        print('\33[39m{0:<50}'.format("语法树见'SyntaxTree-output/SyntaxTree.pdf'"))

startDrawTree()
