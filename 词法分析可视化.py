from tkinter import *
import time
import hashlib
import matplotlib.image as imgplt
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


global num
num =1

global src

class GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name                                                              #初始化

#------------布局--------------#
    def set_init_window(self):
        self.init_window_name.title("6025编译")                                  #窗口名                       
        self.init_window_name.geometry('1600x800+10+10')
        '''self.img = Image.open('cat.gif')
        self.img_png = ImageTk.PhotoImage(self.img)'''


        #self.init_window_name["bg"] = "pink"                                   
        #self.init_window_name.attributes("-alpha",1)                       
        self.init_data_label = Label(self.init_window_name, text="待编译数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="编译结果")
        self.result_data_label.grid(row=0, column=12)
        '''self.log_label = Label(self.init_window_name, text="图片", image = self.img_png )
        self.log_label.grid(row=10, column=40)'''

        
        #文本框
        self.init_data_Text = Text(self.init_window_name, width=70, height=50)               #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=50)            #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=10, columnspan=10)
        #self.log_data_Text = Text(self.init_window_name, width=70, height=50)  
        #self.log_data_Text.grid(row=1, column=24, rowspan =10 ,columnspan=10) 
        #按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="编译", bg="lightblue", width=10,command=self.bianyi) 
        self.str_trans_to_md5_button.grid(row=1, column=48)


#------------功能函数-----------#
    def bianyi(self):
        global src
        global num
        src = self.init_data_Text.get(1.0,END).strip().replace("\n","") 
        for i in range(1,10):
            choose_pic = "Figure_"+ str(i) +".jpg"
            self.img = Image.open(choose_pic)
            self.img_png = ImageTk.PhotoImage(self.img)
            self.log_label = Label(self.init_window_name, text="图片", image = self.img_png )
            self.log_label.grid(row=10, column=40)
            
            '''
            if int(src) in range (1,13):
                self.result_data_Text.delete(1.0 ,END)
                self.result_data_Text.insert(1.0,  ____ )
                
            else:
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0, "ERROR")
            '''
            self.init_window_name.update()
            self.init_window_name.after(1000)
            
        '''
        choose_pic = "Figure_"+ src  +".jpg"
        self.img = Image.open(choose_pic)
        self.img_png = ImageTk.PhotoImage(self.img)
        self.log_label = Label(self.init_window_name, text="图片", image = self.img_png )
        self.log_label.grid(row=10, column=40)
        '''

    
   
#------------获取当前时间--------------#

    def gettime():
        var.set(time.strftime("%H:%M:%S"))  # 获取当前时间
        root.after(1000, gettime) 

#-------------选择图片--------------------#

        
        
    




# ------------主函数--------------#

def gui_start():
    init_window = Tk()
    ljh = GUI(init_window)              #设置窗口默认属性
    ljh.set_init_window()
    init_window.mainloop()




gui_start()
        
    
