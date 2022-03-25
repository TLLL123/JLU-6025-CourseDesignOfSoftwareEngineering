import LexicalAnalysis as tokens

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
        'AssCall': {':=': ['AssignmentRest'],
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
        'VariMore': {':=': [],'*': [], '/': [],'+': [], '-': [], '<': [], '=': [], 'THEN': [],'ELSE': [],'FI':[],'DO': [],'ENDWH':[],')': [],'END':[],';': [],',': [],
                     '[': ['[', 'Exp', ']'],
                     '.': ['.', 'FieldVar']},
        'FieldVar': {'ID': ['ID', 'FieldVarMore']},
        'FieldVarMore': {':=': [],'*': [], '/': [],'+': [], '-': [], '<': [], '=': [], 'THEN': [],'ELSE': [],'FI':[],'DO': [],'ENDWH':[],')': [],'END':[],';': [],',': [],
                         '[': ['[', 'Exp', ']']},#不同
        'CmpOp': {'<': ['<'],
                  '=': ['=']},
        'AddOp': {'+': ['+'],
                  '-': ['-']},
        'MultOp': {'*': ['*'],
                   '/': ['/']},
        'PROGRAM': {'PROGRAM': ['MATCH']},
        'ID': {'ID': ['MATCH']},
        'TYPE': {'TYPE': ['MATCH']},
        'INTEGER': {'INTEGER': ['MATCH']},
        'CHAR': {'CHAR': ['MATCH']},
        'ARRAY': {'ARRAY': ['MATCH']},
        'OF': {'OF': ['MATCH']},
        'INTC': {'INTC': ['MATCH']},
        'RECORD': {'RECORD': ['MATCH']},
        'END': {'END': ['MATCH']},
        'VAR': {'VAR': ['MATCH']},
        'PROCEDURE': {'PROCEDURE': ['MATCH']},
        'BEGIN': {'BEGIN': ['MATCH']},
        'IF': {'IF': ['MATCH']},
        'THEN': {'THEN': ['MATCH']},
        'ELSE': {'ELSE': ['MATCH']},
        'FI': {'FI': ['MATCH']},
        'WHILE': {'WHILE': ['MATCH']},
        'DO': {'DO': ['MATCH']},
        'ENDWH': {'ENDWH': ['MATCH']},
        'READ': {'READ': ['MATCH']},
        'WRITE': {'WRITE': ['MATCH']},
        'RETURN': {'RETURN': ['MATCH']},
        '+': {'+': ['MATCH']},
        '-': {'-': ['MATCH']},
        '*': {'*': ['MATCH']},
        '/': {'/': ['MATCH']},
        '(': {'(': ['MATCH']},
        ')': {')': ['MATCH']},
        '[': {'[': ['MATCH']},
        ']': {']': ['MATCH']},
        ',': {',': ['MATCH']},
        ';': {';': ['MATCH']},
        ':=': {':=': ['MATCH']},
        '..': {'..': ['MATCH']},
        '>': {'>': ['MATCH']},
        '<': {'<': ['MATCH']},
        '.': {'.': ['MATCH']},
        '=': {'=': ['MATCH']}
    }
    reverseMap={
                        'EQ': '='  ,   'LT': '<'       , 'PLUS': '+'     , 'MINUS': '-',
        'TIMES': '*'  , 'OVER': '/',   'LPAREN': '['   , 'RPAREN': ']'   , 'DOT': '.',
                        'SEMI': ';',   'COMMA': ','    , 'LMIDPAREN': '(', 'RMIDPAREN': ')',
        'CONST':'INTC', 'ASSIGN':':=', 'UNDERANGE':'..',
    }

    def analysis(self,code_list,linenum_list):
        print('\33[34m{0:<46}\33[31m|{1:<50}'.format("输入流当前单词","分析栈"))
        #code_list = ['PROGRAM', 'ID', 'TYPE', 'ID', '=', 'INTEGER', ';', 'VAR', 'ID', 'ID', ';', 'BEGIN', 'READ', '(','ID', ')', ';', 'ID', ':=', 'ID', '+', 'INTC', ';', 'WRITE', '(', 'ID', ')', 'END', '.','EOF']  # 输入流
        ana_list = ['Program']  # 分析栈初始状态
        ana_tab = self.LL1Table
        pdeal = 0  # 输入流当前处理到了哪

        while True:
            if ana_list == []:
                print('\33[32m{0:<50}'.format("无语法错误"))
                return
            else:
                # 输入流当前值不属于任何产生式的predict集合
                if code_list[pdeal] not in ana_tab[ana_list[0]]:
                    print("LL(1)分析中断，第"+str(linenum_list[pdeal])+"行单词" + str(code_list[pdeal]) + "出现语法错误")
                    return
                # 分析栈头符为终极符时，与输入流当前扫描到的终极符不一样
                elif ((ana_list[0] in self.TERMINAL) and (code_list[pdeal] in self.TERMINAL) and (ana_list[0] != code_list[pdeal])):
                    print("LL(1)分析中断，第"+str(linenum_list[pdeal])+"行单词" + str(code_list[pdeal]) + "出现语法错误")
                    return
                # 分析栈与输入流待扫描元素不同时为空
                elif ((len(ana_list) == 0 and code_list[pdeal] != '.') or (code_list[pdeal] == '.' and len(ana_list) != 0)):
                    print("LL(1)分析中断，第"+str(linenum_list[pdeal])+"行单词" + str(code_list[pdeal]) + "出现语法错误")
                    return

                # 分析栈顶为终极符且与输入流当前值相同
                elif len(ana_tab[ana_list[0]][code_list[pdeal]]) == 1 and ana_tab[ana_list[0]][code_list[pdeal]][0] == 'MATCH':
                    pdeal += 1
                    ana_list.pop(0)
                    print('\33[32m{0:<50}'.format("MATCH:"+str(code_list[pdeal-1])))
                # 分析栈顶为非终极符，查表用相应产生式右部进行替换
                else:
                    k = 1
                    for item in ana_tab[ana_list[0]][code_list[pdeal]]:
                        ana_list.insert(k, item)
                        k += 1
                    print('\33[34m{0:<50}\33[31m|{1:<50}'.format(str(code_list[pdeal]),str(ana_list)))
                    ana_list.pop(0)
                    print('\33[34m{0:<50}\33[31m|{1:<50}'.format(str(code_list[pdeal]),str(ana_list)))

obj_tokens=tokens.LexicalAnalysis(txt=tokens.code2)
print(tokens.code2)
obj_tokens.analyze()
if(len(obj_tokens.errors)!=0):
    print("请按提示修改错误后再进行语法分析")
    exit()
print("此程序的token序列:")
print(obj_tokens.tokens)

codelist=[]
linenumlist=[]#标志每个单词所在的行号
for i in obj_tokens.tokens:
    if i[1] in GrammaticalAnalysis_LL1.reverseMap:
        codelist.append(GrammaticalAnalysis_LL1.reverseMap[i[1]])
    else:
        codelist.append(i[1])
    linenumlist.append(i[0])
print("codelist:")
print(codelist)
print("linenumlist:")
print(linenumlist)

obj_LL1=GrammaticalAnalysis_LL1()
obj_LL1.analysis(codelist,linenumlist)