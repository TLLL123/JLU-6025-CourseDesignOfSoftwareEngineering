import os
from pymysql import connect
import BuildTable

DATABASE_CONFIG = {'user': 'root',
                   'password': '123456'}

DATABASE_INFO = {"database": 'teaching_management4'}

class DbConnect:#三人均可调用，参数给正确即可
    def __init__(self):
        self.__db = connect(**DATABASE_CONFIG)
        self.__cursor = self.__db.cursor()
        self.__database = DATABASE_INFO['database']

    def __exe(self, sql, data=None):
        try:
            self.__cursor.execute(sql, data)
        except Exception as e:
            return {"status": False, "info": e}
        try:
            self.__db.commit()
        except Exception as e:
            return {"status": False, "info": e}
        return {"status": True, "info": 'ok'}

    def __reset(self):#重要
        self.close()
        DATABASE_CONFIG['database'] = self.__database
        self.__db = connect(**DATABASE_CONFIG)
        self.__cursor = self.__db.cursor()

    def create(self):
        #sql_1 = "create database if not exists {} character set gbk COLLATE gbk_chinese_ci;".format(self.__database)
        sql_1 = "create database {} character set gbk COLLATE gbk_chinese_ci;".format(self.__database)
        sql_2 = BuildTable.buildTable["course"]
        sql_3 = BuildTable.buildTable["section"]
        sql_4 = BuildTable.buildTable["instructor"]
        sql_5 = BuildTable.buildTable["teaches"]
        sql_6 = BuildTable.buildTable["student"]
        sql_7 = BuildTable.buildTable["takes"]
        sql_8 = BuildTable.buildTable["studentAccount"]
        sql_9 = BuildTable.buildTable["instructorAccount"]
        res = self.__exe(sql_1)
        if not res['status']:
            print("数据库创建失败", res['info'])
            self.__reset()  # 为数据库添加配置
            return
        self.__reset()  # 为数据库添加配置
        res = self.__exe(sql_2)
        if not res['status']:
            print("数据表创建失败", res['info'])
        res = self.__exe(sql_3)
        if not res['status']:
            print("数据表创建失败", res['info'])
        res = self.__exe(sql_4)
        if not res['status']:
            print("数据表创建失败", res['info'])
        res = self.__exe(sql_5)
        if not res['status']:
            print("数据表创建失败", res['info'])
        res = self.__exe(sql_6)
        if not res['status']:
            print("数据表创建失败", res['info'])
        res = self.__exe(sql_7)
        if not res['status']:
            print("数据表创建失败", res['info'])
        res = self.__exe(sql_8)
        if not res['status']:
            print("数据表创建失败", res['info'])
        res = self.__exe(sql_9)
        if not res['status']:
            print("数据表创建失败", res['info'])
            return
        print("数据库{}创建成功，8张数据表创建成功".format(DATABASE_INFO["database"]))
        return {"status": True, "info": 'ok'}

    def insert(self, table,data):#table参数是字符串，data参数是元组
        sql=""
        if table=='student':
            sql = "insert into student value (%s,%s,%s,%s)"
        elif table=='takes':
            sql = "insert into takes value (%s,%s,%s,%s,%s,%s)"
        elif table=='instructor':
            sql = "insert into instructor value (%s,%s,%s,%s)"
        elif table=='teaches':
            sql = "insert into teaches value (%s,%s,%s,%s,%s)"
        elif table=='course':
            sql = "insert into course value (%s,%s,%s,%s)"
        elif table=='section':
            sql = "insert into section value (%s,%s,%s,%s,%s,%s,%s)"
        elif table=='studentaccount':
            sql = "insert into studentaccount value (%s,%s)"
        elif table=='instructoraccount':
            sql = "insert into instructoraccount value (%s,%s)"
        res = self.__exe(sql, data)
        if not res['status']:
            print("数据插入失败", res['info'])
            return
        return {'status': True, "info": 'ok'}

    def delete(self,table,key):#table参数是字符串，key参数是字符串
        sql = ""
        if table=='student':
            sql = "delete from student where ID = %s"
        elif table=='takes':
            sql = "delete from takes where ID = %s and course_id = %s and sec_id = %s and semester = %s and year = %s"
        elif table=='instructor':
            sql = "delete from instructor where ID = %s"
        elif table=='teaches':
            sql = "delete from teaches where ID = %s and course_id = %s and sec_id = %s and semester = %s and year = %s"
        elif table=='course':
            sql = "delete from course where course_id = %s"
        elif table=='section':
            sql = "delete from section where course_id = %s and sec_id = %s and semester = %s and year = %s"
        elif table=='studentaccount':
            sql = "delete from studentaccount where ID = %s"
        elif table=='instructoraccount':
            sql = "delete from instructoraccount where ID = %s"

        res = self.__exe(sql,key)
        if not res['status']:
            print("数据删除失败", res['info'])
            return
        return {'status': True, "info": 'ok'}

    def update(self,table,oldkey,newrecord):#table参数是字符串，oldkey参数是元组，newrecord参数是元组
        sql = ""
        if table=='student':
            sql = "update student set ID=%s,name=%s,dept_name=%s,tot_cred=%s where ID = %s"
        elif table=='takes':
            sql = "update takes set ID=%s,course_id=%s,sec_id=%s,semester=%s,year=%s,grade=%s where ID = %s and course_id=%s and sec_id=%s and semester=%s and year=%s"
        elif table=='instructor':
            sql = "update instructor set ID=%s,name=%s,dept_name=%s,salary=%s where ID = %s"
        elif table=='teaches':
            sql = "update takes set ID=%s,course_id=%s,sec_id=%s,semester=%s,year=%s where ID = %s and course_id=%s and sec_id=%s and semester=%s and year=%s"
        elif table=='course':
            sql = "update course set course_id=%s,title=%s,dept_name=%s,credits=%s where course_id = %s"
        elif table=='section':
            sql = "update course set course_id=%s,sec_id=%s,semester=%s,year=%s,building=%s,room_number=%s,time_slot_id=%s where course_id=%s and sec_id=%s and semester=%s and year=%s"
        elif table=='studentaccount':
            sql = "update studentaccount set ID = %s,password = %s where ID = %s"
        elif table=='instructoraccount':
            sql = "update instructoraccount set ID = %s,password = %s where ID = %s"

        data=newrecord+oldkey

        res = self.__exe(sql,data)
        if not res['status']:
            print("数据更新失败", res['info'])
            return
        return {'status': True, "info": 'ok'}

    def select(self,table):#table参数是字符串
        sql = "select * from {}".format(table)
        res = self.__exe(sql)
        if not res['status']:
            print("未查询到数据", res['info'])
            return
        return self.__cursor.fetchall()

    def close(self):
        self.__cursor.close()
        self.__db.close()

class StudentaccountInfoEdit:
    def __init__(self,dbInit):
        self.__db = dbInit

    def select(self, key):
        res = self.__db.select("studentaccount")
        print(res)
        for ID, password in res:
            if ID == key:
                return password

    def update(self,key):
        oldID = key
        newpass = input("请输入修改后的新密码：")

        oldkey = (oldID,)
        newrecord = (oldID, newpass,)
        if self.__db.update("studentaccount", oldkey, newrecord):
            print("更新成功！")

class StudentInfoEdit:
    def __init__(self,dbInit):
        self.__db = dbInit

    def insert(self):#尚未用到
        ID = input("请输入学号：")
        name = input("请输入姓名：")
        dept_name=input("请输入系名：")
        tot_cred=input("请输入总学分：")
        data=(ID,name,dept_name,tot_cred)
        if self.__db.insert("student",data):
            print("插入成功！")
        self.select(ID)

    def delete(self):#尚未用到
        sid_needToDelete = input("请输入想删除学生信息的学号：")
        if self.__db.delete("student",sid_needToDelete):
            print("删除成功！")
        header = "学号 - 姓名 - 系名 - 总学分"
        print(header)
        res = self.__db.select("student")
        for ID, name, dept_name, tot_cred in res:
            print("{} - {} - {} - {}".format(ID, name, dept_name, tot_cred))

    def update(self,key):
        oldID = key
        newID=input("请输入修改后的新学号：")
        newname=input("请输入修改后的新姓名：")
        newdept_name=input("请输入修改后的新系名：")
        newtot_cred=input("请输入修改后的新总学分：")

        oldkey=(oldID,)
        newrecord=(newID,newname,newdept_name,newtot_cred,)
        if self.__db.update("student",oldkey,newrecord):
            print("更新成功！")

    def select(self,key):
        sid_needToSearch = key
        header = "学号 - 姓名 - 系名 - 总学分"
        print(header)
        res = self.__db.select("student")
        for ID, name, dept_name,tot_cred in res:
            if(ID==sid_needToSearch):
                print("{} - {} - {} - {}".format(ID, name, dept_name,tot_cred))

class TakesInfoEdit:
    def __init__(self,dbInit):
        self.__db = dbInit

    def select(self,key):
        header = "学号 - 课程号 - 课程段 - 学期 - 学年 - 成绩"
        print(header)
        res = self.__db.select("takes")
        for ID,course_id,sec_id,semester,year,grade in res:
            if ID==key:
                print("{} - {} - {} - {} - {} - {}".format(ID,course_id,sec_id,semester,year,grade))

    def insert(self,key):
        ID = key
        course_id = input("请输入课程号：")
        sec_id=input("请输入课程段：")
        semester=input("请输入学期：")
        year=input("请输入学年：")
        grade=''

        data=(ID,course_id,sec_id,semester,year,grade)
        if self.__db.insert("takes",data):
            print("插入成功！")
        self.select(key)

    def delete(self,key):
        ID = key
        course_id = input("请输入课程号：")
        sec_id = input("请输入课程段：")
        semester = input("请输入学期：")
        year = input("请输入学年：")
        takeNeedToDelete=(ID,course_id,sec_id,semester,year,)

        if self.__db.delete("takes",takeNeedToDelete):
            print("课程"+course_id+"退选成功！")
        self.select(key)

class Menu:
    def stuLogin(self):
        studentaccountInfo = StudentaccountInfoEdit(dbInit)
        stuInfo=StudentInfoEdit(dbInit)
        takesInfo=TakesInfoEdit(dbInit)

        while True:
            try:
                id = input("请输入学生账号：")
                pw = input("请输入学生密码：")
                print("0000000000000000")
                if pw == studentaccountInfo.select(id):
                    print("1111111111111111")
                    break
                else:
                    print("账号密码输入有误，请重新输入！")
            except:
                print("账号密码输入有误，请重新输入！")

        print("您的相关个人信息如下：")
        stuInfo.select(id)
        print("您的选课信息如下：")
        takesInfo.select(id)
        while True:
            info = \
"""\33[31m请选择：
\33[34m1. 修改登录密码
2. 修改个人信息
3. 选课
4. 退课
5. 退出程序
\33[31m输入功能对应序号："""
            menu = input(info)
            print("\33[30m")
            if menu == "1":
                studentaccountInfo.update(id)
            elif menu == "2":
                stuInfo.update(id)
            elif menu == "3":
                takesInfo.insert(id)
            elif menu == '4':
                takesInfo.delete(id)
            elif menu == "5":
                dbInit.close()
                print("退出成功！")
                exit(0)
            else:
                print("输入菜单有误，请重新输入")

    def run(self):
        while True:
            info = \
"""\33[31m请选择：
\33[34m1. 学生登录
2. 教师登录
3. 管理员登录
4. 退出程序
\33[31m输入功能对应序号："""
            menu = input(info)
            print("\33[30m")
            if menu == "1":
                self.stuLogin()
            elif menu == "2":
                pass#教师相关
            elif menu =='3':
                pass#管理员相关
            elif menu == "4":
                print("退出成功！")
                exit(0)
            else:
                print("输入菜单有误，请重新输入")

dbInit=DbConnect()
dbInit.create()

file=None
try:
    file=open("initFlag.txt",mode='x')
    file.write("此文件标志着数据库已创建，数据表已创建，相关数据已完成初始化")
    dbInit.insert("student", ('00000001', 'John', 'Comp.Sci.', '20'))
    dbInit.insert("student", ('00000002', 'Mike', 'Physics.', '25'))
    dbInit.insert("student", ('00000003', 'Kyle', 'Music.', '30'))
    dbInit.insert("studentaccount", ('00000001', '00000001'))
    dbInit.insert("studentaccount", ('00000002', '00000002'))
    dbInit.insert("studentaccount", ('00000003', '00000003'))
    dbInit.insert("course", ('CS-101', '数据库原理', 'Comp.Sci.', '3'))
    dbInit.insert("course", ('FIN-201', '经济史概论', 'Finance.', '3'))
    dbInit.insert("course", ('BIO-301', '生物信息学', 'Biology', '4'))
    dbInit.insert("section", ('CS-101', '1', 'Fall', '2022', 'YiFuLou', '101', '15:30'))
    dbInit.insert("section", ('FIN-201', '1', 'Fall', '2022', 'JingXinLou', '202', '15:30'))
    dbInit.insert("section", ('BIO-301', '2', 'Spring', '2022', 'LiSiGuangLou', '303', '13:30'))
    dbInit.insert("takes", ('00000001', 'FIN-201', '1', 'Fall', '2022', '98'))
    dbInit.insert("takes", ('00000001', 'CS-101', '1', 'Fall', '2022', '97'))
    dbInit.insert("takes", ('00000001', 'BIO-301', '2', 'Spring', '2022', ''))
    dbInit.insert("takes", ('00000002', 'FIN-201', '1', 'Fall', '2022', '95'))
    dbInit.insert("takes", ('00000002', 'CS-101', '1', 'Fall', '2022', ''))
    dbInit.insert("takes", ('00000002', 'BIO-301', '2', 'Spring', '2022', '96'))
    dbInit.insert("takes", ('00000003', 'FIN-201', '1', 'Fall', '2022', ''))
    dbInit.insert("takes", ('00000003', 'CS-101', '1', 'Fall', '2022', '94'))
    dbInit.insert("takes", ('00000003', 'BIO-301', '2', 'Spring', '2022', '96'))
except:
    print("程序非首次执行，数据库、数据表均已创建，且相关数据已完成初始化")

view = Menu()
view.run()
