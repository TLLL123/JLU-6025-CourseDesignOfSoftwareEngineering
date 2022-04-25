import sys
# -*- coding:ANSI -*-
import string

class LexicalAnalysis:
    def __init__(self,txt):
        self.stateTransitionTable={
            0: {0: 1, 1: 2, 2: 3, 3: 4, 4: 3, 5: 6, 6: 13, 7: 8, 8: 10, 9: 13},
            1: {0: 1, 1: 1, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},
            2: {0: 13, 1: 2, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},
            3: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},
            4: {0: 13, 1: 13, 2: 13, 3: 13, 4: 5, 5: 13, 6: 13, 7: 13, 8: 13, 9: 13},
            5: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},
            6: {0: 6, 1: 6, 2: 6, 3: 6, 4: 6, 5: 6, 6: 7, 7: 6, 8: 6, 9: 6},
            7: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},
            8: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 9, 8: 0, 9: 0},
            9: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},
            10: {0: 11, 1: 11, 2: 13, 3: 13, 4: 13, 5: 13, 6: 13, 7: 13, 8: 13, 9: 13},
            11: {0: 13, 1: 13, 2: 13, 3: 13, 4: 13, 5: 13, 6: 13, 7: 13, 8: 12, 9: 13},
            12: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},
            13: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        }
        self.txt=txt
        self.tokens=[]
        self.delimiters='+-*/();[]<, '
        self.reservedWords=[
            'PROGRAM', 'PROCEDURE', 'TYPE', 'VAR', 'IF',
            'THEN', 'ELSE', 'FI', 'WHILE', 'DO',
            'ENDWH', 'BEGIN', 'END', 'READ', 'WRITE',
            'ARRAY', 'OF', 'RECORD', 'RETURN',
            'INTEGER', 'CHAR'
        ]
        self.operators={
                         '=': 'EQ',  '<': 'LT',    '+': 'PLUS',     '-': 'MINUS',
            '*': 'TIMES','/': 'OVER','[': 'LPAREN',']': 'RPAREN',   '.': 'DOT',
                         ';': 'SEMI',',': 'COMMA', '(': 'LMIDPAREN',')': 'RMIDPAREN'

        }
        self.errors=[]
        self.errorLines=[]

    def getCharType(self,ch):
        if ch in string.ascii_letters: return 0
        if ch.isdigit(): return 1
        if ch in self.delimiters: return 2
        if ch == ':':return 3
        if ch=='=': return 4
        if ch=='{': return 5
        if ch=='}': return 6
        if ch=='.': return 7
        if ch=='\'':return 8
        return 9#其它字符

    def getToken(self,state,line,buf):
        word = "".join(buf)
        if(state==1):
            CapsLK=word.upper()
            if CapsLK in self.reservedWords:
                return (line,CapsLK,word)
            else:
                return (line,"ID",word)
        if(state==2):
            number=int(word)#恰巧SNL语言没有浮点型数
            return (line,"CONST",number)
        if(state==3):return (line,self.operators[word],word)
        if(state==4):pass
        if(state==5):return (line,"ASSIGN",word)
        if(state==6):pass
        if(state==7):return (line,"NOTES",word)
        if(state==8):return (line,"DOT",word)
        if(state==9):return (line,"UNDERANGE",word)
        if(state==10):pass
        if(state==11):pass
        if(state==12):return (line,"ID",word)
        if(state==13):return (line,"ERROR",word)

    def analyze(self):
        txt=self.txt
        nowState=0
        stateList=[]
        line=1
        charbuf=[]
        for ch in txt:
            chCopy=ch
            if ch in '\t\n':
                ch=' '
            chtype=self.getCharType(ch)
            nextState=self.stateTransitionTable[nowState][chtype]
            if(nextState!=0):#当前单词尚未识别完毕
                charbuf.append(ch)
                nowState=nextState
                #print(nowState)
                stateList.append(nowState)
            else:#已完成一个单词的识别
                if charbuf != [' ']:#跳过空格
                    newToken=self.getToken(nowState,line,charbuf)
                    if(newToken[1]=="NOTES"):pass
                    elif(newToken[1]=="ERROR"):
                        tempString="第"+str(line)+"行"+"单词"+newToken[2]+"出现词法错误"
                        self.errors.append(tempString)
                        self.errorLines.append(line)
                    else:
                        self.tokens.append(newToken)
                nowState=self.stateTransitionTable[0][chtype]
                #print(nowState)
                stateList.append(nowState)
                charbuf=[ch]
            if(chCopy=='\n'):
                line+=1
            if(ch=='$'):
                self.tokens.append((line,"EOF","文件结束符号，无语义信息"))

        return stateList

code1='''{}program pp
type t=integer;
var integer v1,v2,v3;
char a1,b,c;
array [1..20] of integer d;
procedure f();
   begin
      v1 := 20 + 10;
      if v1 = 30
      then v2 := 30
      else v2:=10
      fi
   end
begin
   f();
   write(v1)
end.'''

code2='''program p
type t=integer;
t1=char;
t2=record
        integer e1;
        char f1;
        array[1..5] of integer g1;
        integer e2;
        char f2;
        array[1..5] of integer g2;
   end;
var t v1,v2,v3;
t1 v4;
t2 rec1;
array[1..20] of integer a,b,c;

procedure v1Add(t v1);
var integer temp1;
begin
   temp1:=10;
   v1:=v1+temp1;
   write(v1)
end

procedure v2Dec(integer v2);
var integer temp2;
begin
   temp2:=10;
   v2:=v2-temp2;
   write(v2)
end

begin
   {rec1.e1:=10;
   rec1.f1:='a';
   rec1.g1[5]:=10;}
   
   v4:='a';
   
   {v4:=v1;
   v4:=a[1];
   v1:=v2+v4;}
   
   if v1<0
   then read(v1)
   else write(v1)
   fi;
   
   while 0<v1
   do v1:=v1-1
   endwh;
   
   read(v1);
   v1Add(v1);
   v2Dec(v2);
   write(v1);
   read(v1);
   write(a[1])
end.'''

code3='''program  bubble
var  integer  i,j,num;
     array [1..20] of integer  a;
procedure  q(var integer num);
var  integer i,j,k;
     integer t,temp;
     {char 123}{语法错误}
{阿斯蒂阿斯蒂}{词法错误}
begin
  i:=1;
   while i < num do
     j:=num-i+1;
     k:=1;
     while k<j  do
    	if a[k+1] < a[k]  
        then   
	        t:=a[k];
		    a[k]:=a[k+1];
		    a[k+1]:=t
        else  temp:=0
        fi;   
     k:=k+1
     endwh;
  i:=i+1
  endwh
end

begin
   read(num);
   i:=1;
   while i<(num+1)  do
     read(j);
     a[i]:=j;
     i:=i+1
   endwh;
   q(num);
   i:=1;
   while  i<(num+1) do 
       write(a[i]);
       i:=i+1
   endwh
end.'''

code4='''{值参、变参结合功能测试}program sd
var 
    integer x,y,z;     
    procedure f(integer x,y;var integer z;char c);
    begin
	z:=x+y+z;
	write(x);
	write(y);
	write(z)
    end
begin
x:=3;
y:=4;
z:=5;
f(x,y,z,'a');
write(x);
write(y);
write(z);
f(6,(x+(y+z)),y,'a');
write(x);
write(y);
write(z);
f(x+y,y/x,x,'a');
write(x);
write(y);
write(z)
end.'''

with open(sys.path[0]+"/SNL语言例子/一般例子/c1.txt", "r", encoding='ANSI')as f:
    codeInput = f.read()#多行字符串，接收外部输入

def startLexAnalysis(codeInput):
    if len(codeInput) == 0:
        print("请检查输入，输入不能为空！")
        exit()
    obj = LexicalAnalysis(txt=codeInput + '$')
    # 字符序列列表charList
    charList = list(obj.txt)
    # print(charList)
    # print(len(charList))
    # 状态序列列表stateList，每个元素均和charList对应
    stateList = obj.analyze()
    # print(stateList)
    # print(len(stateList))
    if (len(obj.errors) == 0):
        print("\33[32m无词法错误，此代码段的token序列如下：\33[30m")
        print(*obj.tokens, sep='\n')
        return obj.tokens
    else:
        print(*obj.errors, sep='\n')
        print("\33[31m请按提示修改此法错误后再进行后续工作")
        return None

startLexAnalysis(codeInput)
