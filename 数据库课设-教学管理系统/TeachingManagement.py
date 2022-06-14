import os
import time
from pymysql import connect
import BuildTable

DATABASE_CONFIG = {'user': 'root',
                   'password': '123456'}

DATABASE_INFO = {"database": 'teaching_management4'}

#三人均可调用，参数给正确即可
class DbConnect:
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

    def reset(self):#重要
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
            self.reset()  # 为数据库添加配置
            return
        self.reset()  # 为数据库添加配置
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

#学生角色相关
class StudentaccountInfoEdit:
    def __init__(self,dbInit):
        self.__db = dbInit

    def select(self, key):
        res = self.__db.select("studentaccount")
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
        self.select(sid_needToDelete)

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
        print("\33[34m{0:<15}{1:<15}{2:<15}{3:<15}".format("学号", "姓名", "系名", "总学分"))
        res = self.__db.select("student")
        for ID, name, dept_name,tot_cred in res:
            if(ID==sid_needToSearch):
                print("\33[30m{0:<15}{1:<15}{2:<20}{3:<20}".format(ID, name, dept_name,tot_cred))

    def select_return(self, key):
        res = self.__db.select("student")
        for ID, name, dept_name, tot_cred in res:
            if ID == key:
                return (ID, name, dept_name, tot_cred)

class TakesInfoEdit:
    def __init__(self,dbInit):
        self.__db = dbInit

    def select(self,key):
        print("\33[34m{0:<15}{1:<15}{2:<15}{3:<15}{4:<15}{5:<15}".format("学号", "课程号", "课程段", "学期", "学年", "成绩"))
        res = self.__db.select("takes")
        for ID,course_id,sec_id,semester,year,grade in res:
            if ID==key:
                print("\33[30m{0:<15}{1:<15}{2:<15}{3:<15}{4:<15}{5:<15}".format(ID,course_id,sec_id,semester,year,grade))

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

#教师角色相关
class InstructoraccountInfoEdit:
    def __init__(self,dbInit):
        self.__db = dbInit

    def select(self, key):
        # header = ("职工号", "密码")
        res = self.__db.select("instructoraccount")
        for ID, password in res:
            if ID == key:
                return password

class InstructorInfoEdit:
    def __init__(self, dbInit):
        self.__db = dbInit

    def select(self, key):
        res = self.__db.select("instructor")
        for ID, name, dept_name, salary in res:
            if ID == key:
                return (ID, name, dept_name, salary)

    def update(self, key):
        res = self.__db.select("instructor")
        for ID, name, dept_name, salary in res:
            if ID == key:
                print("%3s   %20s   %13s   %4s" % ("职工号", "姓名", "学院", "工资"))
                print("%5s   %21s   %14s   %5s" % (ID, name, dept_name, salary))
                newname = input("请输入新姓名：")
                newdept_name = input("请输入新院名：")
                newID = ID
                newSalary = salary
                oldkey = (key,)
                newrecord = (newID, newname, newdept_name, newSalary,)
                if self.__db.update("instructor", oldkey, newrecord):
                    print("\33[34m更新成功！您目前的个人信息如下：\33[30m")
                print("%3s   %20s   %13s   %4s" % ("职工号", "姓名", "学院", "工资"))
                print("%5s   %21s   %14s   %5s" % (newID, newname, newdept_name, newSalary))

class TeachesInfoEdit:
    def __init__(self,dbInit):
        self.__db = dbInit

    def select(self, key):
        res = self.__db.select("teaches")
        list = []
        for ID, coures_id, sec_id, semester, year in res:
            if ID == key:
                list.append((ID, coures_id, sec_id, semester, year,))
        return list

    def insert(self, ID):
        res = self.__db.select("section")
        print("系统内记录的所有课程信息如下：")
        print("%8s%8s%8s%8s%10s%8s%8s" % ("课程", "课程阶段", "学期", "年份", "教学楼", "教室", "时间段"))
        for coures_id, sec_id, semester, year, building, room_number, time_slot_id in res:
            print("%10s%9s%10s%9s%12s%9s%10s" % (coures_id, sec_id, semester, year, building, room_number, time_slot_id))
        coures_id = input("请选择课程ID：")
        sec_id = input("请选择课程阶段：")
        semester = input("请选择学期：")
        year = input("请选择学年：")
        data = (ID, coures_id, sec_id, semester, year)
        if self.__db.insert("teaches", data):
            print("\33[34m添加成功！目前您所教的全部课程信息如下：\33[30m")
        res = self.select(ID)
        # header = "课程 - 课程阶段 - 学期 - 年份"
        print("%8s%8s%8s%8s" % ("课程", "课程阶段", "学期", "年份"))
        for i in res:
            print("%10s%9s%10s%9s" % (i[1], i[2], i[3], i[4]))

    def delete(self, ID):
        print("目前您所教的全部课程信息如下：")
        res = self.select(ID)
        # header = "课程 - 课程阶段 - 学期 - 年份"
        print("%8s%8s%8s%8s" % ("课程", "课程阶段", "学期", "年份"))
        for i in res:
            print("%10s%9s%10s%9s" % (i[1], i[2], i[3], i[4]))
        coures_id = input("请选择要删除课程的ID：")
        sec_id = input("请选择要删除课程的阶段：")
        semester = input("请选择要删除课程的学期：")
        year = input("请选择要删除课程的学年：")
        data = (ID, coures_id, sec_id, semester, year)
        if self.__db.delete("teaches", data):
            print("\33[34m删除成功！目前您所教的全部课程信息如下：\33[30m")
        res = self.select(ID)
        print("%8s%8s%8s%8s" % ("课程", "课程阶段", "学期", "年份"))
        for i in res:
            print("%10s%9s%10s%9s" % (i[1], i[2], i[3], i[4]))

class GradesInfoEdit:
    def __init__(self,dbInit):
        self.__db = dbInit

    def select(self, key):
        takes = self.__db.select("takes")
        teaches = self.__db.select("teaches")
        list = []
        for ID, coures_id, sec_id, semester, year in teaches:
            if ID == key:
                list.append((coures_id, sec_id, semester, year,))
        res = []
        for ID, coures_id, sec_id, semester, year, grade in takes:
            ii = (coures_id, sec_id, semester, year,)
            if ii in list:
                res.append((ID, coures_id, sec_id, semester, year, grade,))
        return res

    def insert(self, key):
        res = self.select(key)
        print("在您所负责的课程中，学生相关选课信息如下：")
        print("%8s%8s%8s%8s%8s%8s" % ("学号", "课程", "课程阶段", "学期", "年份", "成绩"))
        for i in res:
            print("%9s%10s%9s%10s%9s%9s" % (i[0], i[1], i[2], i[3], i[4], i[5]))
        ID = input("请选择学生学号：")
        coures_id = input("请选择课程ID：")
        sec_id = input("请选择具体课程段：")
        semester = input("请选择课程的学期：")
        year = input("请选择课程的学年：")
        grade = input("请输入学生成绩：")
        newrecord = (ID, coures_id, sec_id, semester, year, grade,)
        oldkey = (ID, coures_id, sec_id, semester, year,)
        if self.__db.update("takes", oldkey, newrecord):
            print("\33[34m添加成功！目前在您所负责的课程中，学生相关选课信息如下：\33[30m")
        res = self.select(key)
        print("%8s%8s%8s%8s%8s%8s" % ("学号", "课程", "课程阶段", "学期", "年份", "成绩"))
        for i in res:
            print("%9s%10s%9s%10s%9s%9s" % (i[0], i[1], i[2], i[3], i[4], i[5]))

    def delete(self, key):
        res = self.select(key)
        print("在您所负责的课程中，学生相关选课信息如下：")
        print("%8s%8s%8s%8s%8s%8s" % ("学号", "课程", "课程阶段", "学期", "年份", "成绩"))
        for i in res:
            print("%9s%10s%9s%10s%9s%9s" % (i[0], i[1], i[2], i[3], i[4], i[5]))
        ID = input("请选择学生学号：")
        coures_id = input("请选择课程ID：")
        sec_id = input("请选择具体课程段：")
        semester = input("请选择课程的学期：")
        year = input("请选择课程的学年：")
        grade = ''
        newrecord = (ID, coures_id, sec_id, semester, year, grade,)
        oldkey = (ID, coures_id, sec_id, semester, year,)
        if self.__db.update("takes", oldkey, newrecord):
            print("\33[34m删除成功！目前在您所负责的课程中，学生相关选课信息如下：\33[30m")
        res = self.select(key)
        print("%8s%8s%8s%8s%8s%8s" % ("学号", "课程", "课程阶段", "学期", "年份", "成绩"))
        for i in res:
            print("%9s%10s%9s%10s%9s%9s" % (i[0], i[1], i[2], i[3], i[4], i[5]))

    def update(self, key):
        res = self.select(key)
        print("在您所负责的课程中，学生相关选课信息如下：")
        print("%8s%8s%8s%8s%8s%8s" % ("学号", "课程", "课程阶段", "学期", "年份", "成绩"))
        for i in res:
            print("%9s%10s%9s%10s%9s%9s" % (i[0], i[1], i[2], i[3], i[4], i[5]))
        ID = input("请选择学生学号：")
        coures_id = input("请选择课程ID：")
        sec_id = input("请选择具体课程段：")
        semester = input("请选择课程的学期：")
        year = input("请选择课程的学年：")
        grade = input("请输入修改后学生成绩：")
        newrecord = (ID, coures_id, sec_id, semester, year, grade,)
        oldkey = (ID, coures_id, sec_id, semester, year,)
        if self.__db.update("takes", oldkey, newrecord):
            print("\33[34m修改成功！目前在您所负责的课程中，学生相关选课信息如下：\33[30m")
        res = self.select(key)
        print("%8s%8s%8s%8s%8s%8s" % ("学号", "课程", "课程阶段", "学期", "年份", "成绩"))
        for i in res:
            print("%9s%10s%9s%10s%9s%9s" % (i[0], i[1], i[2], i[3], i[4], i[5]))

class Menu:
    def stuLogin(self):
        studentaccountInfo = StudentaccountInfoEdit(dbInit)
        stuInfo=StudentInfoEdit(dbInit)
        takesInfo=TakesInfoEdit(dbInit)

        while True:
            try:
                id = input("请输入学生账号：")
                pw = input("请输入学生密码：")
                if pw == studentaccountInfo.select(id):
                    break
                else:
                    print("账号密码输入有误，请重新输入！")
            except:
                print("账号密码输入有误，请重新输入！")

        info = stuInfo.select_return(id)
        print("\33[31m登陆中...")
        print(time.strftime("\33[34m%Y-%m-%d %H:%M:%S", time.localtime()) + ',',"\33[32m{}\33[34m, welcome！\33[30m".format(info[1]))

        while True:
            info = info = \
"""\33[31m请选择您的功能：
\33[34m个人信息管理：
        1. 查看登陆密码
        2. 修改登录密码
        3. 查看个人信息
        4. 修改个人信息
所选课程管理：
        5. 查看所选课程
        6. 新增选课
        7. 退选课程
其他：            
        0. 退出系统
\33[31m数字+回车确认您的功能："""
            menu = input(info)
            print("\33[30m")
            if menu == "1":
                nowpw=studentaccountInfo.select(id)
                print("您当前登陆密码为：\33[31m"+str(nowpw)+"\33[30m")
            elif menu == '2':
                studentaccountInfo.update(id)
            elif menu == '3':
                print("您的相关个人信息如下：")
                stuInfo.select(id)
            elif menu == "4":
                stuInfo.update(id)
            elif menu == "5":
                print("您的选课信息如下：")
                takesInfo.select(id)
            elif menu == "6":
                takesInfo.insert(id)
            elif menu == '7':
                takesInfo.delete(id)
            elif menu == "0":
                dbInit.close()
                print("退出成功！")
                exit(0)
            else:
                print("输入菜单有误，请重新输入")

    def instructorLogin(self):
        instructoraccountInfo = InstructoraccountInfoEdit(dbInit)
        instructorInfo = InstructorInfoEdit(dbInit)
        teachesInfo = TeachesInfoEdit(dbInit)
        gradesInfo = GradesInfoEdit(dbInit)
        ID = ""
        while True:
            try:
                ID = input("请输入您的教职工号：")
                pw = input("请输入您的登录密码：")
                if pw == instructoraccountInfo.select(ID):
                    break
                else:
                    print("账号密码输入有误，请重新输入！")
            except:
                print("账号密码输入有误，请重新输入！")
        info = instructorInfo.select(ID)
        print("\33[31m登陆中...")
        print(time.strftime("\33[34m%Y-%m-%d %H:%M:%S", time.localtime()) + ',', "\33[32m{}\33[34m, welcome！".format(info[1]))
        # print("您的选课信息如下：")
        #TeachesInfoEdit.select(ID)

        while True:
            info = \
"""\33[31m请选择您的功能：
\33[34m个人信息管理：
        1. 查看我的信息
        2. 修改我的信息
所教课程管理：
        3. 查看所教课程
        4. 添加所教课程
        5. 删除所教课程
学生成绩管理：
        6. 学生成绩预览
        7. 添加成绩
        8. 删除成绩
        9. 修改成绩
其他：            
        0. 退出系统
\33[31m数字+回车确认您的功能："""
            menu = input(info)
            print("\33[30m")
            if menu == "0":
                print("退出成功！")
                exit(0)
            elif menu == "1":
                res = instructorInfo.select(ID)
                # header = "职工号 - 姓名 - 学院 - 工资"
                print("%3s   %20s   %13s   %4s" % ("职工号", "姓名", "学院", "工资"))
                print("%5s   %21s   %14s   %5s" % (res[0], res[1], res[2], res[3]))
                print()
            elif menu == "2":
                instructorInfo.update(ID)
            elif menu == "3":
                res = teachesInfo.select(ID)
                # header = "课程 - 课程阶段 - 学期 - 年份"
                print("%8s%8s%8s%8s" % ("课程", "课程阶段", "学期", "年份"))
                for i in res:
                    print("%10s%9s%10s%9s" % (i[1], i[2], i[3], i[4]))
                print()
            elif menu == "4":
                teachesInfo.insert(ID)
            elif menu == "5":
                teachesInfo.delete(ID)
            elif menu == "6":
                res = gradesInfo.select(ID)
                # header = "学号 - 课程 - 课程阶段 - 学期 - 年份 - 成绩"
                print("%8s%8s%8s%8s%8s%8s" % ("学号", "课程", "课程阶段", "学期", "年份", "成绩"))
                for i in res:
                    print("%9s%10s%9s%10s%9s%9s" % (i[0], i[1], i[2], i[3], i[4], i[5]))
                print()
            elif menu == "7":
                gradesInfo.insert(ID)
            elif menu == "8":
                gradesInfo.delete(ID)
            elif menu == "9":
                gradesInfo.update(ID)
            else:
                print("输入数字有误，请您重新输入")

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
                self.stuLogin()#学生相关
            elif menu == "2":
                self.instructorLogin()#教师相关
            elif menu =='3':
                pass#管理员相关
            elif menu == "4":
                print("退出成功！")
                exit(0)
            else:
                print("输入菜单有误，请重新输入")

dbInit=DbConnect()

file=None
try:
    file=open("initFlag.txt",mode='x')
    file.write("此文件标志着数据库已创建，数据表已创建，相关数据已完成初始化")
    dbInit.create()
    dbInit.insert("course", ('CS-101', '数据库原理', 'Comp.Sci.', '3'))
    dbInit.insert("course", ('FIN-201', '经济史概论', 'Finance.', '3'))
    dbInit.insert("course", ('BIO-301', '生物信息学', 'Biology', '4'))
    dbInit.insert("section", ('CS-101', '1', 'Fall', '2022', 'YiFuLou', '101', '15:30'))
    dbInit.insert("section", ('FIN-201', '1', 'Fall', '2022', 'JingXinLou', '202', '15:30'))
    dbInit.insert("section", ('BIO-301', '2', 'Spring', '2022', 'LiSiGuangLou', '303', '13:30'))

    dbInit.insert("student", ('00000001', 'John', 'Comp.Sci.', '20'))
    dbInit.insert("student", ('00000002', 'Mike', 'Physics.', '25'))
    dbInit.insert("student", ('00000003', 'Kyle', 'Music.', '30'))
    dbInit.insert("studentaccount", ('00000001', '00000001'))
    dbInit.insert("studentaccount", ('00000002', '00000002'))
    dbInit.insert("studentaccount", ('00000003', '00000003'))
    dbInit.insert("takes", ('00000001', 'FIN-201', '1', 'Fall', '2022', '98'))
    dbInit.insert("takes", ('00000001', 'CS-101', '1', 'Fall', '2022', '97'))
    dbInit.insert("takes", ('00000001', 'BIO-301', '2', 'Spring', '2022', ''))
    dbInit.insert("takes", ('00000002', 'FIN-201', '1', 'Fall', '2022', '95'))
    dbInit.insert("takes", ('00000002', 'CS-101', '1', 'Fall', '2022', ''))
    dbInit.insert("takes", ('00000002', 'BIO-301', '2', 'Spring', '2022', '96'))
    dbInit.insert("takes", ('00000003', 'FIN-201', '1', 'Fall', '2022', ''))
    dbInit.insert("takes", ('00000003', 'CS-101', '1', 'Fall', '2022', '94'))
    dbInit.insert("takes", ('00000003', 'BIO-301', '2', 'Spring', '2022', '96'))

    dbInit.insert("instructor", ('001', 'Charles W. Bachman', 'Comp.Sci.', '80'))
    dbInit.insert("instructor", ('002', 'Edgar F. Codd', 'Comp.Sci.', '80'))
    dbInit.insert("instructor", ('003', 'James Gray', 'Comp.Sci.', '70'))
    dbInit.insert("instructor", ('004', 'Michael Stonebraker', 'Comp.Sci.', '70'))
    dbInit.insert("instructoraccount", ('001', "001"))
    dbInit.insert("instructoraccount", ('002', '002'))
    dbInit.insert("instructoraccount", ('003', '003'))
    dbInit.insert("instructoraccount", ('004', '004'))
    dbInit.insert("teaches", ('001', 'CS-101', '1', 'Fall', '2022'))
    dbInit.insert("teaches", ('001', 'FIN-201', '1', 'Fall', '2022'))
except:
    dbInit.reset()
    print("程序非首次执行，数据库、数据表均已创建，且相关数据已完成初始化")

view = Menu()
view.run()
