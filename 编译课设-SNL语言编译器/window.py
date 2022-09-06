from tkinter import *
import tkinter as tk
#import time
#import hashlib
from PIL import Image, ImageTk
import SemanticAnalysis
import tkinter.messagebox

import LexicalAnalysis
global timepoint            #计时器
global f2                   #第二页面
global mode   #模式


#-----------------------------界面布局------------------------------------#

class GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name #初始化
        

#------------布局--------------#
    def set_init_window(self):
        self.init_window_name.title("6025编译")                                  #窗口名                       
        #self.init_window_name.resizable(False, False)
        face1(self.init_window_name)
        

class face1():
    def __init__(self,master):
        self.master = master
        self.image_face1_file = Image.open("镇魂曲修.jpg")
        self.image_face1_file = self.image_face1_file.resize((1900,1000))
        self.face1_photo = ImageTk.PhotoImage(self.image_face1_file)

        self.image_face1_p = Image.open("button1.jpg")
        self.image_face1_p = ImageTk.PhotoImage(self.image_face1_p)
        
        self.R =    Frame(self.master ,padx=1,pady=1)
        self.R.grid(row=0,column = 0)
        self.photo_label = Label(self.R , image=self.face1_photo).grid(row = 0, column = 0,rowspan=16,columnspan=16)
        self.face1_enter_button = Button(self.R  , image=self.image_face1_p , font="微软雅黑" , command = lambda:self.to_face2())
        self.face1_enter_button.grid(row=13 ,column =7)

    
    def to_face2(self):
        global f2
        self.R.destroy()
        f2=face2(self.master)


class face2():
    def __init__(self,master):
        global mode
        mode = 1                                                                                #进入双text模式
        self.master = master
        #---------------face2_photo--------------------#
        self.image_file = Image.open("void.jpg")
        self.image_file = self.image_file.resize((1900,1000))
        self.photo = ImageTk.PhotoImage(self.image_file)
        self.F = Frame(self.master ,padx=1,pady=1)
        self.F.grid(row=0,column = 0)
        self.photo_label = Label(self.F , image=self.photo).grid(row = 0, column = 0,rowspan=30,columnspan=40)


        #-----------face2_label--------------#
        #self.image_p = Image.open("aba.jpg")
        #self.image_p = self.image_p.resize((600,800))
        #self.p = ImageTk.PhotoImage(self.image_p)

        self.init_data_label = Label(self.F, text="待编译数据")
        self.init_data_label.grid(row=0, column=6)

        self.result_data_label = Label(self.F, text="编译结果")
        self.result_data_label.grid(row=0, column=20)
        
        #self.result_data_label = Label(self.F, text="图片")
        #self.result_data_label.grid(row=0, column=25)

        #self.log_label = Label(self.F, image = self.p).grid(row=1, column=20 , rowspan =10,columnspan =10 )

        #第二界面_文本框
        self.init_data_Text = Text(self.F, width=90, height=65)               #原始数据录入框
        self.init_data_Text.grid(row=1,column=0, rowspan=10, columnspan=10)         # row 1-11 , column 0-10
        self.result_data_Text = Text(self.F,width=180,height=65)            #处理结果展示
        self.result_data_Text.grid(row=1, column=10, rowspan=10, columnspan=20,sticky=S + W + E + N)     # row 1-11 , column 10-20

        # 滚动条
        self.init_data_Text.scroll = Scrollbar(orient = "vertical", command =self.init_data_Text.yview)
        self.init_data_Text.config(yscrollcommand = self.init_data_Text.scroll.set)
        self.init_data_Text.scroll.grid(row=1, column=1, sticky=S + W + E + N)

        self.result_data_Text.scroll = Scrollbar(orient="vertical", command=self.result_data_Text.yview)
        self.result_data_Text.config(yscrollcommand=self.result_data_Text.scroll.set)
        self.result_data_Text.scroll.grid(row=1, column=1, sticky=S + W + E + N)

        #-----button------#
        self.face2_yy_button = Button(self.F, text="语法分析", bg="lightblue",font="微软雅黑", width=15,command=self.bianyi) 
        self.face2_yy_button.grid(row=12 , column=6)
        self.face2_yy_run_button = Button(self.F, text='加快',bg="lightblue",font="微软雅黑",width=4,command = self.run)
        self.face2_yy_run_button.grid(row=12 , column =7)
        self.face2_yy_run_button = Button(self.F, text='token', bg="lightblue", font="微软雅黑", width=4, command=self.out_token)
        self.face2_yy_run_button.grid(row=12, column=8)
        self.face2_yf_button = Button(self.F, text="LL1语法分析", bg="lightblue",font="微软雅黑", width=15,command=self.LL1)
        self.face2_yf_button.grid(row=12 , column=15)
        self.face2_yfs_button = Button(self.F, text="语法树生成23", bg="lightblue",font="微软雅黑", width=15,command=self.tree)
        self.face2_yfs_button.grid(row=12 , column=25)
        self.face2_dgxj_button = Button(self.F, text="递归下降语法分析", font="微软雅黑",width=15,command=self.digui)
        self.face2_dgxj_button.grid(row=14 , column=6)
        self.str_trans_to_md5_button = Button(self.F, text="语义分析/删除3",font="微软雅黑", width=15,command=self.delete_text3)
        self.str_trans_to_md5_button.grid(row=14 , column=15)
        self.face2_run_button = Button(self.F, text="保存结果并退出",font="微软雅黑", width=15,command=lambda:self.to_face3())          #切换到2
        self.face2_run_button.grid(row=14 , column=25)





#-------------------组件----------------------#
    def create_text2(self):
        self.result_data_label = Label(self.F, text="编译结果")
        self.result_data_label.grid(row=0, column=15)

        self.result_data_Text = Text(self.F, width=90, height=65)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=10, rowspan=10, columnspan=10,sticky=S + W + E + N)  # row 1-11 , column 10-20
        self.result_data_Text.scroll = Scrollbar(orient="vertical", command=self.result_data_Text.yview)
        self.result_data_Text.config(yscrollcommand=self.result_data_Text.scroll.set)
        self.result_data_Text.scroll.grid(row=1, column=1, sticky=S + W + E + N)


    def create_text3(self):
        self.result_label = Label(self.F, text="图片")
        self.result_label.grid(row=0, column=25)


    def create_text23(self):
        self.result_data_label = Label(self.F, text="编译结果")
        self.result_data_label.grid(row=0, column=20)

        self.result_data_Text = Text(self.F, width=180, height=65)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=10, rowspan=10, columnspan=20, sticky=S + W + E + N)
        self.result_data_Text.scroll = Scrollbar(orient="vertical", command=self.result_data_Text.yview)
        self.result_data_Text.config(yscrollcommand=self.result_data_Text.scroll.set)
        self.result_data_Text.scroll.grid(row=1, column=1, sticky=S + W + E + N)


    def delete_text2(self):
        self.result_data_Text.destroy()
        self.result_data_label.destroy()


    def delete_text3(self):
        self.result_label.destroy()


    def delete_text23(self):
        self.result_data_Text.destroy()
        self.result_data_label.destroy()



    def run(self):
        global timepoint
        timepoint = 1

#------------切换模式-----------#
    def change_to1(self):
        global mode
        if (mode ==2 ):
            self.delete_text2()
            self.delete_text3()
            self.create_text23()
            mode = 1

    def change_to2(self):
        global mode
        if (mode == 1):  # 如果不为2模式，则切换至2模式
            self.delete_text23()
            self.create_text2()
            self.create_text3()
            mode = 2
#------------功能函数-----------#

    def display_messagebox(self):
        tk.messagebox.showinfo(title= '错误', message=self.error)

    def messagebox_ex(self,error):
        tk.messagebox.showinfo(title='错误',message=error)
    #---------词法分析------------#
    def bianyi(self):

        global timepoint
        self.src = self.init_data_Text.get(1.0, END).strip()
        if (self.src == ''):                                            #如果待输入数据为空，弹窗报错
            self.error = '待编译数据为空'
            self.display_messagebox()
            return 0

        self.change_to2()
        timepoint = 0                                                   #重置计时器

        self.delete()
        self.obj = LexicalAnalysis.LexicalAnalysis(txt=self.src + '$')
        stateList , self.error, self.obj.tokens  = self.obj.analyze()

        charList = list(self.obj.txt)



        self.tokens = self.obj.tokens  # 一整个token序列
        print(self.tokens)
        j = -1
        begin = 0
        store = 0
        self.delete()
        for i in stateList:
            j = j + 1
            if int(i) in range(1, 14):
                if store != int(i) or int(i) == 13:
                    if store != 0:
                        self.insert(store)
                        self.insert('     ')
                        self.insert(charList[begin:j])
                        self.insert('\n')
                        self.insert('\n')
                    store = i
                    begin = j
                if (timepoint == 0):
                    choose_pic = r"C:\Users\XUECHI\Desktop\picture\图片\Figure_" + str(i) + ".jpg"
                    self.img = Image.open(choose_pic)
                    self.img = self.img.resize((600, 800))
                    self.img_png = ImageTk.PhotoImage(self.img)
                    self.log_label = Label(self.F, image=self.img_png)
                    self.log_label.grid(row=1, column=20, rowspan=10,columnspan=10)  # row 1-11 column 20-30
                self.this = charList[j]
                self.insert(self.this)
                self.insert('\n')

            else:
                self.display_messagebox()
            if(timepoint ==0 ):
                self.master.update()
                self.master.after(100)
            self.log_label.destroy()



    #------------------LL1---------------------#
    def LL1(self):

        global type
        self.change_to1()
        self.delete()
        print("1")
        import LL1
        self.src = self.init_data_Text.get(1.0, END).strip()
        if (self.src == ''):                                            #如果待输入数据为空，弹窗报错
            self.error = '待编译数据为空'
            self.display_messagebox()
            return 0
        self.obj_tokens = LexicalAnalysis.startLexAnalysis(self.src)
        LL1.startLL1(self.obj_tokens)


#--------------递归下降-----------------------#
    def digui(self):
        self.change_to1()
        self.src = self.init_data_Text.get(1.0, END).strip()
        if (self.src == ''):  # 如果待输入数据为空，弹窗报错
            self.error = '待编译数据为空'
            self.display_messagebox()
            return 0
        self.delete()
        SemanticAnalysis.Semantic()




#--------------#语法树------------------------#
    def tree(self):
        import drawTree
        drawTree.startDrawTree()
#-------------进入彩蛋页面--------------------#
    def to_face3(self):
        self.F.destroy()
        face3(self.master)


# -----------输入框输出框操作----------------#

    def insert(self,word):                          #输入
        self.word = word
        self.result_data_Text.insert(END,self.word)

    def insert_n(self,word):                          #输入
        self.word = word
        self.result_data_Text.insert(END,self.word)
        self.result_data_Text.insert(END,'\n')

    def insertn(self):
        self.result_data_Text.insert(END,'\n')

    def insert_d(self,word1,word2):
        num=len(word1)
        self.result_data_Text.insert(END, word1)
        for i in range(70-num):
            self.result_data_Text.insert(END,' ')
        self.result_data_Text.insert(END,word2)
        self.result_data_Text.insert(END,'\n')

    def insert_9(self, a):
        leng=[]
        for i in a:
            leng.append(len(i))
        for j in range(0,8):
            self.result_data_Text.insert(END,a[j])
            print(a[j],end=" ")
            for t in range(15- leng[j]):
                print(" ",end=" ")
                self.result_data_Text.insert(END,' ')
        self.result_data_Text.insert(END,'\n')




    def delete(self):                          #删除
        self.result_data_Text.delete(1.0,END)

    def wait(self):
        self.master.update()
        self.master.after(100)

#--------------得到token序列----------------#
    def get_token(self):
        return self.obj

    def get_txt(self):
        return self.src

    def out_token(self):
        self.delete()
        self.result_data_Text.insert(END, self.obj.tokens)
#--------------换图片------------------#
    def show_picture(self,i):
        choose_pic = r"C:\Users\XUECHI\Desktop\picture\图片\Figure_" + str(i) + ".jpg"
        self.img = Image.open(choose_pic)
        self.img = self.img.resize((460, 600))
        self.img_png = ImageTk.PhotoImage(self.img)
        self.log_label = Label(self.F, image=self.img_png).grid(row=1, column=20, rowspan=10,columnspan=10)  # row 1-11 column 20-30



#--------------第三页面-----------------------#
class face3():
    def __init__(self , master):
        self.master = master
        self.image_face1_file = Image.open("雪修.jpg")
        self.image_face1_file = self.image_face1_file.resize((1500,800))
        self.face1_photo = ImageTk.PhotoImage(self.image_face1_file)
        self.G =    Frame(self.master ,padx=1,pady=1)
        self.G.grid(row=0,column = 0)
        self.photo_label = Label(self.G , image=self.face1_photo).grid(row = 0, column = 0,rowspan=16,columnspan=16)
        self.face1_enter_button = Button(self.G , text="谢谢观看",bg = 'white' , font="微软雅黑",width=15 , command = lambda:self.to_exit())
        self.face1_enter_button.grid(row=13 ,column =7)

    def to_exit(self):
        exit()
        

def gui_start():
    init_window = Tk()
    ljh = GUI(init_window)              #设置窗口默认属性
    ljh.set_init_window()
    init_window.mainloop()


