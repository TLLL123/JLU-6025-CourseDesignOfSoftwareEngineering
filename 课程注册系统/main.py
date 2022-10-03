import flask
from flask import url_for  # 进行网页跳转
import os  # 用于操作系统文件的依赖库
import re  # 引入正则表达式对用户输入进行限制
import pymysql  # 连接数据库
import xlrd2

worksheet = xlrd2.open_workbook('databaseConfig.xls')
sheet_names= worksheet.sheet_names()
sheet_name=sheet_names[0]# xls文件中的第一页表格
sheet = worksheet.sheet_by_name(sheet_name)
rows = sheet.nrows # 获取行数
cols = sheet.ncols # 获取列数，尽管没用到
databaseParameter=[0,0,0,0,0,0]

for i in range(6):
    databaseParameter[i]=sheet.col_values(i)[1]

# 初始化
app = flask.Flask(__name__)
db=[]
# 初始化数据库连接
# 使用pymysql.connect方法连接本地mysql数据库
# db = pymysql.connect(host='localhost', port=3306, charset='utf8', database="course_registration_system2", user='root', password='123456')

#连接服务器中的远程数据库
try:
    db = pymysql.connect(host=databaseParameter[0],
                         port=int(databaseParameter[1]),
                         charset=databaseParameter[2],
                         database=databaseParameter[3],
                         user=databaseParameter[4],
                         password=databaseParameter[5],
                         connect_timeout=1,
                         read_timeout=1,
                         write_timeout=1)
except Exception as errorMsg:
    #print("\33[31m数据库连接失败，请确保数据库已打开，且数据库配置文件中的参数正确，再尝试重新连接！\33[36m")
    #print(errorMsg)
    #print(type(errorMsg))
    if errorMsg.args[0]==1045:
        print("\33[31m数据库连接失败，请确保数据库配置文件中的参数正确，再尝试重新连接！\33[36m")
        print(errorMsg)
    elif errorMsg.args[0]==2013:
        print("\33[31m数据库连接失败，请确保数数据库已打开，再尝试重新连接！\33[36m")
        print(errorMsg)
    else:
        print("\33[31m数据库连接失败，请确保相关配置正确，再尝试重新连接！\33[36m")
        print(errorMsg)

    exit()

# 操作数据库，获取db下的cursor对象
cursor = db.cursor()

#全局变量
users = []# 存的是用户名
f2 = open("closeRegisterFlag.txt", encoding="utf-8", mode='r+')
f2.write("0")#初始是未关闭注册，仍允许选课

@app.route("/", methods=["GET", "POST"])
def login():
    # 增加会话保护机制(未登陆前login的session值为空)
    flask.session['login'] = ''
    if flask.request.method == 'POST':
        user=""
        global user_id
        user_id= flask.request.values.get("user", "")
        pwd = flask.request.values.get("pwd", "")
        print(user_id,pwd)
        # print(user_id)
        if user_id != '' and pwd != '':  # 与数据库中数据进行比较
            msg = '用户名或密码错误'
            sql = "select * from login where name='" + user_id + "' and passwd='" + pwd + "';"
            cursor.execute(sql)
            result = cursor.fetchone()
            # print(result[2])
            # 匹配得到结果即管理员数据库中存在此管理员
            if result:
                # 登陆成功
                flask.session['login'] = 'OK'

                if result[2]==1:
                    users.append(user_id)
                    return flask.redirect(flask.url_for('add_professor'))
                elif result[2]==2:
                    users.append(user_id)
                    print("xxxx:",users)
                    return flask.redirect(flask.url_for('teacher'))
                else:
                    sql1 = "select name from students where student_id=%s"
                    cursor.execute(sql1, user_id)
                    re = cursor.fetchone()
                    user = re[0]
                    users.append(user)  # 存储登陆成功的用户名用于显示
                    print(user_id)
                    return flask.redirect(flask.url_for('choose_course'))
                # return flask.redirect('/file')
        else:  # 输入验证不通过
            msg = '非法输入'
    else:
        msg = ''
        user = ''
    return flask.render_template('login.html', msg=msg, user=user)

user_id=10#存的是用户id

#查询空教室用
def avi_conf(sem_id,wek_id,day_id,s_time,e_time):
    print("succ1")
    pos=[]
    sql="select classroom_id,name from classrooms"
    cursor.execute(sql)
    room=cursor.fetchall()
    print('room',room)
    for line_1 in room:
        flag=0
        arr = [0] * 2000  # 即[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        room_id=line_1[0]
        print(sem_id,room_id)
        sql = "select se.start_week,se.end_week,se.start_time,se.end_time,se.weekday from sections se inner join takes ta on se.takes_id=ta.takes_id where ta.semester_id=%s and se.classroom_id=%s"
        cursor.execute(sql, (sem_id,room_id))
        table = cursor.fetchall()
        print(table)
        for line in table:
            print("has")
            for wek in range(line[0], line[1] + 1):  # 3-15
                for i in range(line[2], line[3] + 1):
                    print(wek, line[4], i, (wek - 1) * 7 * 11 + (line[4] - 1) * 11 + (i - 1) * 1)
                    arr[(wek - 1) * 7 * 11 + (line[4] - 1) * 11 + (i - 1) * 1] = 1
        print("hasq")
        for line in ((int(wek_id), int(wek_id), int(s_time), int(e_time), int(day_id)),):
            # print(type(line[0]))
            wek=line[0]
            # print(type(line[2]),type(line[3]))
            for i in range(line[2], line[3]+1):  # 7-9
                print("okq")
                print(wek, line[4], i, (wek - 1) * 7 * 11 + (line[4] - 1) * 11 + (i - 1) * 1)
                if (arr[(wek - 1) * 7 * 11 + (line[4] - 1) * 11 + (i - 1) * 1] == 1):
                    flag=1
                    break
                # if(flag==1):break
            if (flag == 1): break
        if(flag==0):pos.append(line_1)
    print("succ")
    return pos

#选课，防止课程冲突用
def conf(stu_id,takes_id):
    arr = [0] * 2000  # 即[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sql="select semester_id from takes where takes_id=%s";
    cursor.execute(sql,takes_id)
    sem_id=cursor.fetchall()
    sem_id=sem_id[0][0]
    #print("sem_id:",sem_id[0][0])
    print(stu_id,sem_id)
    sql="select se.start_week,se.end_week,se.start_time,se.end_time,se.weekday from student_takes st inner join sections se inner join takes ta on st.takes_id=se.takes_id and se.takes_id=ta.takes_id where student_id=%s and ta.semester_id=%s"
    cursor.execute(sql,(stu_id,sem_id))
    table=cursor.fetchall()
    print(table)
    for line in table:
        print("has")
        for wek in range(line[0], line[1] + 1):  # 3-15
            for i in range(line[2],line[3]+1):
                print(wek,line[4],i,(wek-1)*7*11+(line[4]-1)*11+(i-1)*1)
                arr[(wek-1)*7*11+(line[4]-1)*11+(i-1)*1]=1
    # for i in range(0,2001):
    #     if(arr[i]==1):print (i)
    print("----------------")
    print(stu_id,takes_id)
    sql1 = "select se.start_week,se.end_week,se.start_time,se.end_time,se.weekday from sections se inner join takes ta on se.takes_id=ta.takes_id where se.takes_id=%s"
    cursor.execute(sql1,takes_id)
    table1 = cursor.fetchall()
    print(table1)
    for line in table1:
        for wek in range(line[0],line[1]+1):#3-15
            # for wek_d in//对于一个line来说 weekday是不用遍历的
            for i in range(line[2],line[3]+1):#7-9
                print(wek, line[4], i, (wek - 1) * 7 * 11 + (line[4] - 1) * 11 + (i - 1) * 1)
                if(arr[(wek-1)*7*11+(line[4]-1)*11+(i-1)*1]==1):return True
    return False

#学生
@app.route('/choose_course', methods=['GET', "POST"])
def choose_course():
    global user_id
    # login session值
    primary_course = ''
    alternate_course = ''
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''

    #根据是否关闭注册，选择是否允许提交选课
    f1 = open("closeRegisterFlag.txt", encoding="utf-8", mode='r')
    if f1.read()=='0':
        submit_switch = 'submit'  # 未关闭注册，仍允许选课
        print("未关闭注册")
    else:
        submit_switch = ''
        print("已关闭注册")

    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list = "select ta.takes_id,co.name,te.name,max_num,current_num,se.start_week,se.end_week,se.start_time,se.end_time,co.tuition " \
                   "from takes ta inner join sections se inner join courses co inner join teachers te " \
                   "where ta.takes_id=se.takes_id and ta.course_id=co.course_id and ta.teacher_id=te.teacher_id;"
        cursor.execute(sql_list)
        results = cursor.fetchall()

    if flask.request.method == 'POST':
        # 获取输入的学生信息
        # student_id = flask.request.values.get("student_id", "")
        takes_id = flask.request.values.get("takes_id", "")

        try:
            # 信息存入数据库
            sql = "select * from students where student_id=%s"  # 看是否存在此学号的学生
            cursor.execute(sql, user_id)
            Id = cursor.fetchone()
            # print(re)
            sql_0 = "select max_num,current_num from takes where takes_id=%s"  # 看是否存在此课程号或是否满课
            cursor.execute(sql_0, takes_id)
            TakeId = cursor.fetchone()
            #
            sql_4 = "select * from student_takes where student_id=%s and takes_id=%s"  # 看是否已经选过了
            cursor.execute(sql_4, (user_id, takes_id))
            chosen = cursor.fetchone()
            #
            sql_5 = "select count(*) from student_takes where student_id=%s"
            cursor.execute(sql_5, user_id)
            result_5 = cursor.fetchone()
            # print(result_5)
            result_5 = result_5[0]
            print("result_5:")
            print(result_5)
            primary_course = min(result_5, 4)
            alternate_course = max(result_5 - 4, 0)

            conflict = conf(user_id, takes_id)

            if Id == None or TakeId == None:
                insert_result = "学号或课程号不存在"
            elif TakeId[0] == TakeId[1]:
                insert_result = "选课失败，已达最大选课人数"
            elif chosen != None:
                insert_result = "该生已选过该课程"
            elif conflict == True:
                insert_result = "当前课程与已选课程时间冲突"
            elif alternate_course >= 2:
                insert_result = "选课失败，您已经选择了4门首选课程和2门备选课程"
            else:
                sql_1 = "insert into student_takes(student_id,takes_id) values(%s,%s)"
                cursor.execute(sql_1, (user_id, takes_id))
                sql_2 = "update takes set current_num=current_num+1 where takes_id=%s"
                cursor.execute(sql_2, (takes_id))
                insert_result = "选课成功"
                result_5+=1
                primary_course = min(result_5, 4)
                alternate_course = max(result_5 - 4, 0)
            print(insert_result)
        except Exception as err:
            print(err)
            insert_result = "选课信息插入失败"
            print(insert_result)
            pass
        db.commit()
        # POST方法时显示数据
        sql_list = "select ta.takes_id,co.name,te.name,max_num,current_num,se.start_week,se.end_week,se.start_time,se.end_time,co.tuition " \
                   "from takes ta inner join sections se inner join courses co inner join teachers te " \
                   "where ta.takes_id=se.takes_id and ta.course_id=co.course_id and ta.teacher_id=te.teacher_id;"
        cursor.execute(sql_list)
        results = cursor.fetchall()

    return flask.render_template('student/choose_course.html', submit_switch=submit_switch,insert_result=insert_result, user_info=user_info, results=results, primary_course=primary_course, alternate_course=alternate_course)

# @app.route('/choose_course', methods=['GET', "POST"])
# def choose_course():
#     global user_id
#     # login session值
#     if flask.session.get("login", "") == '':
#         # 用户没有登陆
#         print('用户还没有登陆!即将重定向!')
#         return flask.redirect('/')
#     insert_result = ''
#     # 当用户登陆有存储信息时显示用户名,否则为空
#     if users:
#         for user in users:
#             user_info = user
#     else:
#         user_info = ''
#
#     #根据是否关闭注册，选择是否允许提交选课
#     f1 = open("closeRegisterFlag.txt", encoding="utf-8", mode='r')
#     if f1.read()=='0':
#         submit_switch = 'submit'  # 未关闭注册，仍允许选课
#         print("未关闭注册")
#     else:
#         submit_switch = ''
#         print("已关闭注册")
#
#     # 获取显示管理员数据信息(GET方法的时候显示数据)
#     if flask.request.method == 'GET':
#         sql_list = "select ta.takes_id,co.name,te.name,max_num,current_num,se.start_week,se.end_week,se.start_time,se.end_time,co.tuition " \
#                    "from takes ta inner join sections se inner join courses co inner join teachers te " \
#                    "where ta.takes_id=se.takes_id and ta.course_id=co.course_id and ta.teacher_id=te.teacher_id;"
#         cursor.execute(sql_list)
#         results = cursor.fetchall()
#
#     if flask.request.method == 'POST':
#         # 获取输入的学生信息
#         # student_id = flask.request.values.get("student_id", "")
#         takes_id = flask.request.values.get("takes_id", "")
#
#         try:
#             # 信息存入数据库
#             sql = "select * from students where student_id=%s"#看是否存在此学号的学生
#             cursor.execute(sql, user_id)
#             Id = cursor.fetchone()
#             # print(re)
#             sql_0 = "select max_num,current_num from takes where takes_id=%s"#看是否存在此课程号或是否满课
#             cursor.execute(sql_0, takes_id)
#             TakeId = cursor.fetchone()
#             #
#             sql_4="select * from student_takes where student_id=%s and takes_id=%s"#看是否已经选过了
#             cursor.execute(sql_4, (user_id,takes_id))
#             chosen = cursor.fetchone()
#
#             conflict=conf(user_id,takes_id)
#
#             if Id == None or TakeId==None:
#                 insert_result = "学号或课程号不存在"
#             elif TakeId[0]==TakeId[1]:
#                 insert_result = "选课失败，已达最大选课人数"
#             elif chosen!=None:
#                 insert_result = "该生已选过该课程"
#             elif conflict==True:
#                 insert_result="当前课程与已选课程时间冲突"
#             else:
#                 sql_1 = "insert into student_takes(student_id,takes_id) values(%s,%s)"
#                 cursor.execute(sql_1, (user_id, takes_id))
#                 sql_2 = "update takes set current_num=current_num+1 where takes_id=%s"
#                 cursor.execute(sql_2, (takes_id))
#                 insert_result = "成功存入一条学生信息"
#             print(insert_result)
#         except Exception as err:
#             print(err)
#             insert_result = "选课信息插入失败"
#             print(insert_result)
#             pass
#         db.commit()
#         # POST方法时显示数据
#         sql_list = "select ta.takes_id,co.name,te.name,max_num,current_num,se.start_week,se.end_week,se.start_time,se.end_time,co.tuition " \
#                    "from takes ta inner join sections se inner join courses co inner join teachers te " \
#                    "where ta.takes_id=se.takes_id and ta.course_id=co.course_id and ta.teacher_id=te.teacher_id;"
#         cursor.execute(sql_list)
#         results = cursor.fetchall()
#     return flask.render_template('student/choose_course.html', submit_switch=submit_switch,insert_result=insert_result, user_info=user_info, results=results)
@app.route('/change_course', methods=['GET', "POST"])
def change_course():
    global user_id
    print("kkk",user_id)
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''

    # 根据是否关闭注册，选择是否允许提交退课
    f1 = open("closeRegisterFlag.txt", encoding="utf-8", mode='r')
    if f1.read() == '0':
        submit_switch = 'submit'  # 未关闭注册，仍允许选课
        print("未关闭注册")
    else:
        submit_switch = ''
        print("已关闭注册")

    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list_1 = "select stu.takes_id,co.name,te.name,max_num,current_num,se.start_week,se.end_week,se.start_time,se.end_time,co.tuition  " \
                   "from student_takes stu inner join takes ta inner join sections se inner join courses co inner join teachers te " \
                   "where stu.student_id=%s and stu.takes_id=ta.takes_id and ta.takes_id=se.takes_id and ta.course_id=co.course_id and ta.teacher_id=te.teacher_id ;"
        cursor.execute(sql_list_1, user_id)
        results_1 = cursor.fetchall()
        sql_list_2 = "select ta.takes_id,co.name,te.name,max_num,current_num,se.start_week,se.end_week,se.start_time,se.end_time,co.tuition " \
                   "from takes ta inner join sections se inner join courses co inner join teachers te " \
                   "where ta.takes_id=se.takes_id and ta.course_id=co.course_id and ta.teacher_id=te.teacher_id;"
        cursor.execute(sql_list_2)
        results_2 = cursor.fetchall()

    if flask.request.method == 'POST':
        # 获取输入的学生信息
        # student_id = flask.request.values.get("student_id", "")
        choose_takes_id = flask.request.values.get("choose_takes_id", "")
        delete_takes_id = flask.request.values.get("delete_takes_id", "")

        try:
            # 信息存入数据库
            sql = "select * from students where student_id=%s"#看是否存在此学号的学生
            cursor.execute(sql, user_id)
            Id = cursor.fetchone()
            #
            sql_0 = "select max_num,current_num from takes where takes_id=%s"#看是否存在此课程号或是否满课
            cursor.execute(sql_0, choose_takes_id)
            TakeId = cursor.fetchone()
            #
            sql_3 = "select * from student_takes where student_id=%s and takes_id=%s"  # 看是否已经选过了
            cursor.execute(sql_3, (user_id, choose_takes_id))
            chosen_1 = cursor.fetchone()
            #
            sql_4="select * from student_takes where student_id=%s and takes_id=%s"#看是否已经选过了
            cursor.execute(sql_4, (user_id, delete_takes_id))
            chosen_2 = cursor.fetchone()

            conflict = conf(user_id, choose_takes_id)

            if Id == None or TakeId == None:
                insert_result = "换课失败，学号或课程号不存在"
            elif TakeId[0]==TakeId[1]:
                insert_result = "换课失败，已达最大选课人数"
            elif chosen_2==None:
                insert_result = "换课失败，该生未选过该课程"
            elif chosen_1!=None:
                insert_result = "换课失败，该生已选过该课程"
            elif conflict==True:
                insert_result="换课失败，当前课程与已选课程时间冲突"
            else:
                # sql_1 = "insert into student_takes(student_id,takes_id) values(%s,%s)"
                sql_1="delete from student_takes where student_id=%s and takes_id=%s"
                cursor.execute(sql_1, (user_id, delete_takes_id))

                sql_2 = "update takes set current_num=current_num-1 where takes_id=%s"
                cursor.execute(sql_2, (delete_takes_id))

                sql_3 = "insert into student_takes(student_id,takes_id) values(%s,%s)"
                cursor.execute(sql_3, (user_id, choose_takes_id))
                sql_4 = "update takes set current_num=current_num+1 where takes_id=%s"
                cursor.execute(sql_4, (choose_takes_id))

                insert_result = "换课成功"
            print(insert_result)
        except Exception as err:
            print(err)
            insert_result = "换课失败"
            print(insert_result)
            pass
        db.commit()
        # POST方法时显示数据
        sql_list_1 = "select stu.takes_id,co.name,te.name,max_num,current_num,se.start_week,se.end_week,se.start_time,se.end_time,co.tuition  " \
                   "from student_takes stu inner join takes ta inner join sections se inner join courses co inner join teachers te " \
                   "where stu.student_id=%s and stu.takes_id=ta.takes_id and ta.takes_id=se.takes_id and ta.course_id=co.course_id and ta.teacher_id=te.teacher_id ;"
        cursor.execute(sql_list_1, user_id)
        results_1 = cursor.fetchall()

        sql_list_2 = "select ta.takes_id,co.name,te.name,max_num,current_num,se.start_week,se.end_week,se.start_time,se.end_time,co.tuition " \
                   "from takes ta inner join sections se inner join courses co inner join teachers te " \
                   "where ta.takes_id=se.takes_id and ta.course_id=co.course_id and ta.teacher_id=te.teacher_id;"
        cursor.execute(sql_list_2)
        results_2 = cursor.fetchall()

    return flask.render_template('student/change_course.html', submit_switch=submit_switch, insert_result=insert_result, user_info=user_info, results_1=results_1, results_2=results_2)

@app.route('/drop_course', methods=['GET', "POST"])
def drop_course():
    global user_id
    print("kkk",user_id)
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''

    # 根据是否关闭注册，选择是否允许提交退课
    f1 = open("closeRegisterFlag.txt", encoding="utf-8", mode='r')
    if f1.read() == '0':
        submit_switch = 'submit'  # 未关闭注册，仍允许选课
        print("未关闭注册")
    else:
        submit_switch = ''
        print("已关闭注册")

    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list = "select stu.takes_id,co.name,te.name,max_num,current_num,se.start_week,se.end_week,se.start_time,se.end_time,co.tuition  from student_takes stu inner join takes ta inner join sections se inner join courses co inner join teachers te where stu.student_id=%s and stu.takes_id=ta.takes_id and ta.takes_id=se.takes_id and ta.course_id=co.course_id and ta.teacher_id=te.teacher_id ;"
        cursor.execute(sql_list,user_id)
        results = cursor.fetchall()

    if flask.request.method == 'POST':
        # 获取输入的学生信息
        # student_id = flask.request.values.get("student_id", "")
        takes_id = flask.request.values.get("takes_id", "")

        try:
            # 信息存入数据库
            sql = "select * from students where student_id=%s"#看是否存在此学号的学生
            cursor.execute(sql, user_id)
            Id = cursor.fetchone()
            #
            # sql_0 = "select max_num,current_num from takes where takes_id=%s"#看是否存在此课程号或是否满课
            # cursor.execute(sql_0, takes_id)
            # TakeId = cursor.fetchone()
            #
            sql_4="select * from student_takes where student_id=%s and takes_id=%s"#看是否已经选过了
            cursor.execute(sql_4, (user_id,takes_id))
            chosen = cursor.fetchone()

            if Id == None :
                insert_result = "学号不存在"
            # elif TakeId[0]==TakeId[1]:
            #     insert_result = "选课失败，已达最大选课人数"
            elif chosen==None:
                insert_result = "退课失败，该生未选过该课程"
            else:
                # sql_1 = "insert into student_takes(student_id,takes_id) values(%s,%s)"
                sql_1="delete from student_takes where student_id=%s and takes_id=%s"
                cursor.execute(sql_1, (user_id, takes_id))

                sql_2 = "update takes set current_num=current_num-1 where takes_id=%s"
                cursor.execute(sql_2, (takes_id))
                insert_result = "成功删除选课记录"
            print(insert_result)
        except Exception as err:
            print(err)
            insert_result = "选课记录删除失败"
            print(insert_result)
            pass
        db.commit()
        # POST方法时显示数据
        sql_list = "select stu.takes_id,co.name,te.name,max_num,current_num,se.start_week,se.end_week,se.start_time,se.end_time,co.tuition  from student_takes stu inner join takes ta inner join sections se inner join courses co inner join teachers te where stu.student_id=%s and stu.takes_id=ta.takes_id and ta.takes_id=se.takes_id and ta.course_id=co.course_id and ta.teacher_id=te.teacher_id ;"
        cursor.execute(sql_list, user_id)
        results = cursor.fetchall()
    return flask.render_template('student/drop_course.html', submit_switch=submit_switch, insert_result=insert_result, user_info=user_info, results=results)

@app.route('/find_grades', methods=['GET', 'POST'])
def find_grades():
    global user_id
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    query_result = ''
    results = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''

    sql="select semester_id,school_year,season from semesters";
    cursor.execute(sql)
    choses = cursor.fetchall()
    print(choses)

    # 获取下拉框的数据
    if flask.request.method == 'POST':
        select = flask.request.form.get('selected_one')
        query = flask.request.values.get('query')
        # print(select, query)
        # 判断不同输入对数据表进行不同的处理
        try:
            print(select)
            sql = "select student_id,s.takes_id,score from student_takes s inner join takes t on s.takes_id=t.takes_id where student_id = %s and t.semester_id=%s; "
            cursor.execute(sql, (user_id,select))
            results = cursor.fetchall()

            print(user_id,select,results)
            if results:
                query_result = '查询成功!'
            else:
                query_result = '当前学期没有成绩记录!'
        except Exception as err:
            print(err)
            pass
    return flask.render_template('student/find_grades.html', query_result=query_result, user_info=user_info, results=results,choses=choses)

@app.route('/find_schedule', methods=['GET', "POST"])
def find_schedule():
    global user_id
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    query_result = ''
    results = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''

    sql = "select semester_id,school_year,season from semesters";
    cursor.execute(sql)
    choses = cursor.fetchall()
    print(choses)
    arr = {}
    if flask.request.method == 'POST':
        select = flask.request.form.get('selected_one')
        query = flask.request.values.get('query')
        # print(select, query)
        # 判断不同输入对数据表进行不同的处理
        try:
            sql = "select weekday,  start_time,  end_time,  course_id,  start_week  ,end_week,  classroom_id,teacher_id from stutake_sec_takes where student_id=%s and semester_id=%s;"
            cursor.execute(sql, (user_id,select))
            init_record = cursor.fetchall()  #


            for i in range(1, 78):
                arr[i] = []
            for line in init_record:
                record = []
                print(record)
                sql = "select name from courses where course_id=%s"
                cursor.execute(sql, line[3])
                cor_name = cursor.fetchall()
                cor_name = cor_name[0][0]
                record.append(cor_name)

                sql = "select name from classrooms where classroom_id=%s"
                cursor.execute(sql, line[6])
                room_name = cursor.fetchall()
                room_name = room_name[0][0]
                record.append(room_name)

                sql = "select name from teachers where teacher_id=%s"
                cursor.execute(sql, line[7])
                tea_name = cursor.fetchall()
                tea_name = tea_name[0][0]
                record.append(tea_name)

                str1=str(line[4])+"—"+str(line[5])+"周"
                record.append(str1)
                # record.append(line[4])
                # record.append(line[5])

                for i in range(line[1], line[2] + 1):
                    print("k")
                    print((line[0] - 1) * 11 + i)
                    arr[(line[0] - 1) * 11 + i] = record

            if init_record:
                query_result = '查询成功!'
            else:
                query_result = '当前学期没有课程记录!'
        except Exception as err:
            print(err)
            pass
    return flask.render_template('student/find_schedule.html', query_result=query_result, user_info=user_info, results=results,choses=choses,arr=arr)

@app.route('/find_available', methods=['GET', 'POST'])
def find_available():
    global user_id
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    query_result = ''
    results = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''

    sql="select semester_id from semesters";
    cursor.execute(sql)
    choses = cursor.fetchall()

    choses_two = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']

    choses_three = ['1','2','3','4','5','6','7']
    choses_four = ['1','2','3','4','5','6','7','8','9','10','11']
    choses_five = ['1','2','3','4','5','6','7','8','9','10','11']
    # 获取下拉框的数据
    if flask.request.method == 'POST':
        select_one = flask.request.form.get('selected_one')
        select_two = flask.request.form.get('selected_two')
        select_three = flask.request.form.get('selected_three')
        select_four = flask.request.form.get('selected_four')
        select_five = flask.request.form.get('selected_five')
        query = flask.request.values.get('query')
        # print(select, query)
        # 判断不同输入对数据表进行不同的处理
        try:
            pos = avi_conf(select_one, select_two, select_three, select_four, select_five)
            print(pos)
            # print(user_id,select,results)
            if(select_four>select_five) :query_result = '要求:开始节数≤结束结束!'
            elif len(pos)!=0:
                results=pos
                query_result = '查询成功!'
            else:
                query_result = '当前时段没有空教室!'
        except Exception as err:
            print(err)
            pass
    return flask.render_template('student/find_available.html', query_result=query_result, user_info=user_info, results=results,choses=choses,choses_two=choses_two,choses_three=choses_three,choses_four=choses_four,choses_five=choses_five)

#教师
@app.route('/teacher', methods=['GET', "POST"])
def teacher():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    teacher_id = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for u in users:
            print(u)
            teacher_id = u
        sql_name = "select name from teachers where teacher_id=%s"
        cursor.execute(sql_name % teacher_id)
        result = cursor.fetchall()
        user_info = result[0][0]
        print(user_info)
    else:
        user_info = ''
    # POST显示数据
    sql_list = "select * from teachers where teacher_id=(%s);"
    cursor.execute(sql_list, teacher_id)
    results = cursor.fetchall()
    sql_schedule = "call get_schedule(%s);"
    cursor.execute(sql_schedule, teacher_id)
    schedule = cursor.fetchall()
    return flask.render_template('teacher/teacher.html', user_info=user_info, results=results, schedule=schedule)

@app.route('/course', methods=['GET', "POST"])
def course():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    teacher_id = ''
    if users:
        for u in users:
            print(u)
            teacher_id = u
        sql_name = "select name from teachers where teacher_id=%s"
        cursor.execute(sql_name % teacher_id)
        result = cursor.fetchall()
        user_info = result[0][0]
        print(user_info)
    else:
        user_info = ''
    #results = []

    sql_name = "select course_id from teachers as t1,takes as t2 where t1.teacher_id=t2.teacher_id and t1.teacher_id=%s;"
    cursor.execute(sql_name,teacher_id)
    all_courses_id = cursor.fetchall()
    print(all_courses_id)#此教师教的所有课程号
    # POST显示数据
    results = ()
    for each in all_courses_id:
        sql_list = "select c.course_id, c.name, buildings.name, classrooms.name, max_num, classrooms.classroom_id, capacity\
                    from courses as c, classrooms, buildings, sections as s, takes as t\
                    where classrooms.building_id=buildings.building_id and t.course_id=c.course_id and c.course_id=%s and t.teacher_id=%s and s.takes_id=t.takes_id and classrooms.classroom_id=s.classroom_id;  "
        cursor.execute(sql_list, (each[0], teacher_id))#传递课程号和老师工号
        temp = cursor.fetchall()
        results = results + temp
    print(results)#所有所教课程的信息

    if flask.request.method == 'POST':
        # 获取输入的学生选课信息
        course_id = flask.request.values.get("course_id", "")
        classroom_id = flask.request.values.get("classroom_id", "")
        max_num = flask.request.values.get("max_num", "")
        print(course_id, classroom_id, max_num)
        try:
            # 信息存入数据库
            sql = "call update_course(%s, %s, %s, %s);"
            cursor.execute(sql, (course_id, teacher_id, max_num, classroom_id))
            insert_res = cursor.fetchone()
            insert_result = insert_res[0]
            print(insert_result)
        except Exception as err:
            insert_result = "修改信息失败"
            pass
        if insert_result != "成功修改课程信息":
            return flask.render_template('teacher/course.html', insert_result=insert_result, user_info=user_info,
                                         results=results)
        db.commit()

        # POST显示数据
        results=()
        for each in all_courses_id:
            sql_list = "select c.course_id, c.name, buildings.name, classrooms.name, max_num, classrooms.classroom_id, capacity\
                        from courses as c, classrooms, buildings, sections as s, takes as t\
                        where classrooms.building_id=buildings.building_id and t.course_id=c.course_id and c.course_id=%s and t.teacher_id=%s and s.takes_id=t.takes_id and classrooms.classroom_id=s.classroom_id;  "
            cursor.execute(sql_list, (each[0], teacher_id))
            temp=cursor.fetchall()
            results=results+temp
        print(results)
    return flask.render_template('teacher/course.html', insert_result=insert_result, user_info=user_info, results=results)

@app.route('/grade', methods=['GET', "POST"])
def grade():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    teacher_id = ''
    if users:
        for u in users:
            print(u)
            teacher_id = u
        sql_name = "select name from teachers where teacher_id=%s"
        cursor.execute(sql_name % teacher_id)
        result = cursor.fetchall()
        user_info = result[0][0]
        print(user_info)
    else:
        user_info = ''
    results = []

    sql_list = "call get_stu_scores(%s);"
    cursor.execute(sql_list, teacher_id)
    results = cursor.fetchall()

    if flask.request.method == 'POST':
        # 获取输入的学生成绩信息
        student_id = flask.request.values.get("student_id", "")
        course_id = flask.request.values.get("course_id", "")
        grade = flask.request.values.get("grade", "")
        print(student_id, course_id, grade)
        # 信息存入数据库
        try:
            sql = "call update_score(%s, %s, %s, %s)"
            cursor.execute(sql, (student_id, teacher_id, course_id, grade))
            insert_res = cursor.fetchone()
            insert_result = insert_res[0]
        except Exception as err:
            insert_result = "学生成绩录入失败"
            pass
        if insert_result != "成功录入学生成绩":
            return flask.render_template('teacher/grade.html', insert_result=insert_result, user_info=user_info, results=results)
        db.commit()
        # POST获取数据
        sql_list = "call get_stu_scores(%s);"
        cursor.execute(sql_list, teacher_id)
        results = cursor.fetchall()
    return flask.render_template('teacher/grade.html', insert_result=insert_result, user_info=user_info, results=results)

@app.route('/choose_teach_course', methods=['GET', 'POST'])
def choose_teach_course():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    sem_id = '00002'
    insert_result = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for u in users:
            print(u)
            teacher_id = u
        sql_name = "select name from teachers where teacher_id=%s"
        cursor.execute(sql_name % teacher_id)
        result = cursor.fetchall()
        user_info = result[0][0]
        print(user_info)
    else:
        user_info = ''

    results1 = []
    results2 = []

    sql2 = "select course_id,name,hours from courses"
    cursor.execute(sql2)
    results2 = cursor.fetchall()

    sql3 = "select courses.name\
            from teachers,teacher_teaches,courses\
            where teachers.teacher_id=teacher_teaches.teacher_id and teacher_teaches.course_id=courses.course_id and teachers.teacher_id=%s;"
    cursor.execute(sql3,teacher_id)
    results3 = cursor.fetchall()

    if flask.request.method == 'POST':
        # 获取输入的课程号信息
        course_id = flask.request.values.get("week", "")
        print("course_id=",course_id)
        # 信息存入数据库
        try:
            sql1 = "insert into teacher_teaches(teacher_id,course_id) values (%s,%s);"
            cursor.execute(sql1, (teacher_id,course_id))
            results1 = cursor.fetchall()

            print("results1=", results1)
            insert_result = "插入成功"
        except Exception as err:
            insert_result = "插入失败"
            print(err)
            pass
    return flask.render_template('teacher/choose_teach_course.html', insert_result=insert_result, user_info=user_info, results=results2, results_course=results3)

@app.route('/delete_teach_course', methods=['GET', 'POST'])#不加的话，会显示“Not Found The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.”
def delete_teach_course():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    sem_id = '00002'
    insert_result = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for u in users:
            print(u)
            teacher_id = u
        sql_name = "select name from teachers where teacher_id=%s"
        cursor.execute(sql_name % teacher_id)
        result = cursor.fetchall()
        user_info = result[0][0]
        print(user_info)
    else:
        user_info = ''

    results1 = []
    results2 = []

    sql2 = "select course_id,name,hours from courses"
    cursor.execute(sql2)
    results2 = cursor.fetchall()

    sql3 = "select courses.name\
            from teachers,teacher_teaches,courses\
            where teachers.teacher_id=teacher_teaches.teacher_id and teacher_teaches.course_id=courses.course_id and teachers.teacher_id=%s;"
    cursor.execute(sql3,teacher_id)
    results3 = cursor.fetchall()

    if flask.request.method == 'POST':
        # 获取输入的课程号信息
        course_id = flask.request.values.get("week", "")
        print("course_id=",course_id)
        # 信息存入数据库
        try:
            sql1 = "delete from teacher_teaches where teacher_id=%s and course_id=%s;"
            cursor.execute(sql1, (teacher_id,course_id))
            results1 = cursor.fetchall()

            print("results1=", results1)
            insert_result = "删除成功"
        except Exception as err:
            insert_result = "删除失败"
            print(err)
            pass
    return flask.render_template('teacher/delete_teach_course.html', insert_result=insert_result, user_info=user_info, results=results2, results_course=results3)

#管理员
@app.route('/add_professor', methods=['GET', "POST"])
def add_professor():
     # return flask.render_template('administrator/add_professor.html')
     search_result=''
     insert_result=''
     results = []
     if flask.request.method == 'POST':

         # teacher_id = flask.request.values.get("teacher_id", "")
         teacher_name = flask.request.values.get("teacher_name", "")
         gender= flask.request.values.get("gender", "")
         birthday = flask.request.values.get("birthday", "")
         phone = flask.request.values.get("phone", "")
         email = flask.request.values.get("email", "")
         # social_security_number = flask.request.values.get("social_security_number", "")
         status = flask.request.values.get("status", "")
         department = flask.request.values.get("department", "")


         # print("teacher_id:", teacher_id, "phone : ", phone, "email: ", email)  # 打印出这三个输入的信息
         # print("teacher_id=",teacher_id,"phone=",phone,"email=",email)
         # print("wxh1 : ",teacher_id)
         print(teacher_name,gender,birthday,phone,email,status,department)
         # print(teacher_name, gender)
        #当查询第一行的时候
         if  teacher_name =='' and gender=='' and birthday == ''  and phone == '' and email == ''  and status=='' and department=='':
             # print("查询，teacher_id=",teacher_id)
             # sql_list = "select * from teachers where teacher_id=(%s);"
             sql_list = "select * from teachers;"
             # cursor.execute(sql_list, teacher_id)  # 执行相应的sql语句
             cursor.execute(sql_list)
             results = cursor.fetchall()
             # print("results=",results)
             if len(results) != 0:
                 search_result = "查询成功！"
             else:
                 search_result = "查询失败！"
         elif teacher_name!='' and gender!='' and birthday!='' and phone!='' and email!=''  and status !='' and department!='':
             # print("修改，teacher_id=",teacher_id,"phone=",phone,"email=",email)
             print('牛逼！')
             if gender not in ['男','女','其他']:
                 insert_result+="性别有误、"
             len_bir=len(birthday)
             if len_bir !=10:
                 insert_result += "出生日期格式有误、"
             else:
                 for i in range(len_bir):
                     if i >= 0 and i <= 3:
                         if birthday[i]> '9' or birthday[i] < '0':
                             insert_result += "出生日期格式有误、"
                             break
                     elif i==4:
                         if birthday[i]!='-':
                             insert_result+="出生日期格式有误、"
                     elif i<=6:
                         if birthday[i]> '9' or birthday[i] < '0':
                             insert_result += "出生日期格式有误、"
                             break
                     elif i==7:
                         if birthday[i]!='-':
                             insert_result+="出生日期格式有误、"
                     else:
                         if birthday[i]> '9' or birthday[i] < '0':
                             insert_result += "出生日期格式有误、"
                             break
             for p in phone:
                 if p > '9' or p < '0':
                     insert_result += "电话号码格式有误、"
                     break
             if '@' not in email:
                 insert_result += "邮箱格式有误"
             if insert_result != '':
                 # return flask.render_template('update_professor.html', insert_result=insert_result)
                 return flask.render_template('administrator/add_professor.html', search_result=search_result,
                                              insert_result=insert_result, results=results)
             print("你好啊")
             try:
                 # 信息存入数据库
                 # sql = "call update_info(%s, %s, %s);"
                 sql = " call addTeacher((%s),(%s),(%s), (%s), (%s), (%s), (%s));"
                 cursor.execute(sql, (teacher_name, gender, birthday,phone,email,status,department))
                 print("再见")
                 # cursor.execute(sql, (teacher_id, phone, email))
                 results = cursor.fetchall()
                 print("results=", results)
                 insert_result = "添加教授成功"
             except Exception as err:
                 insert_result = "添加教授失败"
                 pass
             db.commit()
             # POST显示数据
             # sql_list = "select * from teachers where teacher_id=(%s);"
             # cursor.execute(sql_list, teacher_id)
             # results = cursor.fetchall()
             # print(results)
         else:
             insert_result = "信息不完整，添加教授失败"

     return flask.render_template('administrator/add_professor.html',search_result=search_result, insert_result=insert_result,results=results)

@app.route('/update_professor', methods=['GET', "POST"])
def update_professor():
    search_result = ''
    insert_result = ''
    results=[]
    if flask.request.method == 'POST':
        teacher_id = flask.request.values.get("teacher_id", "")
        phone = flask.request.values.get("phone", "")
        email = flask.request.values.get("email", "")
        print("teacher_id:",teacher_id,"phone : ",phone,"email: ",email)  #打印出这三个输入的信息
        #print("teacher_id=",teacher_id,"phone=",phone,"email=",email)
        if teacher_id!='' and phone=='' and email=='':
            #print("查询，teacher_id=",teacher_id)
            sql_list = "select * from teachers where teacher_id=(%s);"
            cursor.execute(sql_list, teacher_id)#执行相应的sql语句
            results = cursor.fetchall()
            # print("results=",results)
            if len(results)!=0:
                search_result="查询成功！"
            else:
                search_result="查询失败！"
        else:
            #print("修改，teacher_id=",teacher_id,"phone=",phone,"email=",email)
            for p in phone:
                if p > '9' or p < '0':
                    insert_result += "电话号码格式有误、"
                    break
            if '@' not in email:
                insert_result += "邮箱格式有误"
            if insert_result != '':
                # return flask.render_template('update_professor.html', insert_result=insert_result)
                return flask.render_template('administrator/update_professor.html', search_result=search_result,
                                             insert_result=insert_result, results=results)
            try:
                # 信息存入数据库
                # sql = "call update_info(%s, %s, %s);"
                print("你好啊")
                sql = "update teachers set phone=(%s), mail=(%s) where teacher_id=(%s);"
                cursor.execute(sql, (phone, email,teacher_id))
                print("再见")
                # cursor.execute(sql, (teacher_id, phone, email))
                results = cursor.fetchall()
                print("results=", results)
                insert_result = "修改信息成功"
            except Exception as err:
                insert_result = "修改信息失败"
                pass
            db.commit()
            # POST显示数据
            sql_list = "select * from teachers where teacher_id=(%s);"
            cursor.execute(sql_list, teacher_id)
            results = cursor.fetchall()
            #print(results)

    return flask.render_template('administrator/update_professor.html',search_result=search_result,insert_result=insert_result,results=results)

@app.route('/delete_professor', methods=['GET', "POST"])
def delete_professor():
    search_result = ''
    insert_result = ''
    results = []
    if flask.request.method == 'POST':
        teacher_id = flask.request.values.get("teacher_id", "")
        phone = flask.request.values.get("phone", "")
        email = flask.request.values.get("email", "")
        print("teacher_id:", teacher_id, "phone : ", phone, "email: ", email)  # 打印出这三个输入的信息
        # print("teacher_id=",teacher_id,"phone=",phone,"email=",email)
        if teacher_id != '' and phone == '' and email == '':  # 选择第一行
            # print("查询，teacher_id=",teacher_id)
            sql_list = "select * from teachers where teacher_id=(%s);"
            cursor.execute(sql_list, teacher_id)  # 执行相应的sql语句
            results = cursor.fetchall()
            # print("results=",results)
            if len(results) != 0:
                search_result = "查询成功！"
            else:  # 选择第二行
                search_result = "查询失败！"
        else:
            # print("修改，teacher_id=",teacher_id,"phone=",phone,"email=",email)
            for p in phone:
                if p > '9' or p < '0':
                    insert_result += "电话号码格式有误、"
                    break
            if '@' not in email:
                insert_result += "邮箱格式有误"
            if insert_result != '':
                # return flask.render_template('update_professor.html', insert_result=insert_result)
                return flask.render_template('administrator/delete_professor.html', search_result=search_result,
                                             insert_result=insert_result, results=results)
            try:
                # 信息存入数据库
                # sql = "call update_info(%s, %s, %s);"
                sql = "delete from teachers where teacher_id=(%s) and phone=(%s) and mail=(%s);"  #需要考虑级联删除的问题
                cursor.execute(sql, (teacher_id, phone, email))
                # cursor.execute(sql, (teacher_id, phone, email))
                results = cursor.fetchall()
                print("results=", results)
                insert_result = "删除成功"
            except Exception as err:
                insert_result = "删除失败"
                pass
            db.commit()
            # POST显示数据
            sql_list = "select * from teachers where teacher_id=(%s);"
            cursor.execute(sql_list, teacher_id)
            results = cursor.fetchall()
            # print(results)
    return flask.render_template('administrator/delete_professor.html', search_result=search_result,
                                 insert_result=insert_result, results=results)

@app.route('/add_student', methods=['GET', "POST"])
def add_student():
    search_result = ''
    insert_result = ''
    results = []
    if flask.request.method == 'POST':

        # teacher_id = flask.request.values.get("teacher_id", "")
        student_id = flask.request.values.get("student_id", "")
        name = flask.request.values.get("name", "")
        state = flask.request.values.get("state", "")
        class_id = flask.request.values.get("class_id", "")
        gender = flask.request.values.get("gender", "")
        birthday = flask.request.values.get("birthday", "")
        phone = flask.request.values.get("phone", "")
        email = flask.request.values.get("email", "")
        status = flask.request.values.get("status", "")
        gra_date = flask.request.values.get("gra_date", "")

        # print("teacher_id:", teacher_id, "phone : ", phone, "email: ", email)  # 打印出这三个输入的信息
        # print("teacher_id=",teacher_id,"phone=",phone,"email=",email)
        # print("wxh1 : ",teacher_id)
        # print(teacher_name, gender, birthday, phone, email, status, department)
        # 当查询第一行的时候
        if student_id == '' and name == '' and state == '' and class_id== '' and gender == '' and birthday == '' and phone == '' and email == '' and status == '' and gra_date== '':
            # print("查询，teacher_id=",teacher_id)
            # sql_list = "select * from teachers where teacher_id=(%s);"
            sql_list = "select * from students;"
            # cursor.execute(sql_list, teacher_id)  # 执行相应的sql语句
            cursor.execute(sql_list)
            results = cursor.fetchall()
            # print("results=",results)
            if len(results) != 0:
                search_result = "查询成功！"
            else:
                search_result = "查询失败！"
        elif student_id != '' and name != '' and state != '' and class_id != '' and gender != '' and birthday != '' and phone != '' and email != '' and status != '' and gra_date != '':
            # print("修改，teacher_id=",teacher_id,"phone=",phone,"email=",email)
            if len(student_id) != 8:
                insert_result += "student_id格式有误、"
            else:
                temp=student_id[:6]
                sql_list2 = "select * from classes where class_id=(%s);"
                # cursor.execute(sql_list, teacher_id)  # 执行相应的sql语句
                cursor.execute(sql_list2, temp)
                results = cursor.fetchall()
                # print("results=",results)
                if len(results) == 0:
                    insert_result += "该student_id中未含class_id！"
                else:
                    for p in student_id:
                        if p > '9' or p < '0':
                            insert_result += "student格式有误、"
                            break

            for p in state:
                if p > '9' or p < '0':
                    insert_result += "state格式有误、"
                    break

            #class_id是外键，必须要确认该class_id是存在的
            sql_list3 = "select * from students where class_id=(%s);"
            # cursor.execute(sql_list, teacher_id)  # 执行相应的sql语句
            cursor.execute(sql_list3,class_id)
            results = cursor.fetchall()
            # print("results=",results)
            if len(results) == 0:
                insert_result += "该class_id不存在！"


            if gender not in ['男', '女', '其他']:
                insert_result += "性别有误、"
            len_bir = len(birthday)
            if len_bir != 10:
                insert_result += "出生日期格式有误、"
            else:
                for i in range(len_bir):
                    if i >= 0 and i <= 3:
                        if birthday[i] > '9' or birthday[i] < '0':
                            insert_result += "出生日期格式有误、"
                            break
                    elif i == 4:
                        if birthday[i] != '-':
                            insert_result += "出生日期格式有误、"
                    elif i <= 6:
                        if birthday[i] > '9' or birthday[i] < '0':
                            insert_result += "出生日期格式有误、"
                            break
                    elif i == 7:
                        if birthday[i] != '-':
                            insert_result += "出生日期格式有误、"
                    else:
                        if birthday[i] > '9' or birthday[i] < '0':
                            insert_result += "出生日期格式有误、"
                            break
            for p in phone:
                if p > '9' or p < '0':
                    insert_result += "电话号码格式有误、"
                    break
            if '@' not in email:
                insert_result += "邮箱格式有误、"

            #检测毕业日期
            len_gra = len(gra_date)
            if len_gra != 10:
                insert_result += "毕业日期格式有误、"
            else:
                for i in range(len_gra):
                    if i >= 0 and i <= 3:
                        if gra_date[i] > '9' or gra_date[i] < '0':
                            insert_result += "毕业日期格式有误、"
                            break
                    elif i == 4:
                        if gra_date[i] != '-':
                            insert_result += "毕业日期格式有误、"
                    elif i <= 6:
                        if gra_date[i] > '9' or gra_date[i] < '0':
                            insert_result += "毕业日期格式有误、"
                            break
                    elif i == 7:
                        if gra_date[i] != '-':
                            insert_result += "毕业日期格式有误、"
                    else:
                        if gra_date[i] > '9' or gra_date[i] < '0':
                            insert_result += "毕业日期格式有误、"
                            break
            if insert_result != '':
                # return flask.render_template('update_professor.html', insert_result=insert_result)
                return flask.render_template('administrator/add_student.html', search_result=search_result,
                                             insert_result=insert_result, results=results)

            try:
                # 信息存入数据库
                # sql = "call update_info(%s, %s, %s);"
                sql = "insert into students value((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s));"
                cursor.execute(sql, (student_id, name,state,class_id, gender, birthday, phone, email,student_id, status, gra_date))
                # cursor.execute(sql, (teacher_id, phone, email))
                results = cursor.fetchall()
                print("results=", results)
                insert_result = "添加学生成功"
            except Exception as err:
                insert_result = "添加学生失败"
                pass
            db.commit()
            # POST显示数据
            # sql_list = "select * from teachers where teacher_id=(%s);"
            # cursor.execute(sql_list, teacher_id)
            # results = cursor.fetchall()
            # print(results)
        else:
            insert_result = "信息不完整，添加学生失败"

    return flask.render_template('administrator/add_student.html', search_result=search_result,
                                 insert_result=insert_result, results=results)

@app.route('/update_student', methods=['GET', "POST"])
def update_student():
    search_result = ''
    insert_result = ''
    results = []
    if flask.request.method == 'POST':
        student_id = flask.request.values.get("student_id", "")
        phone = flask.request.values.get("phone", "")
        email = flask.request.values.get("email", "")
        status = flask.request.values.get("status", "")

        # print("teacher_id=",teacher_id,"phone=",phone,"email=",email)
        if student_id != '' and phone == '' and email == '' and status == '':
            # print("查询，teacher_id=",teacher_id)
            sql_list = "select * from students where student_id=(%s);"
            cursor.execute(sql_list, student_id)  # 执行相应的sql语句
            results = cursor.fetchall()
            # print("results=",results)
            if len(results) != 0:
                search_result = "查询成功！"
            else:
                search_result = "查询失败！"
        else:
            # print("修改，teacher_id=",teacher_id,"phone=",phone,"email=",email)
            for p in phone:
                if p > '9' or p < '0':
                    insert_result += "电话号码格式有误、"
                    break
            if '@' not in email:
                insert_result += "邮箱格式有误、"
            for p in status:
                if p < 'a' or p > 'z':
                    insert_result += "状态格式有误"
                    break
            if insert_result != '':
                # return flask.render_template('update_professor.html', insert_result=insert_result)
                return flask.render_template('administrator/update_student.html', search_result=search_result,
                                             insert_result=insert_result, results=results)
            try:
                # 信息存入数据库
                # sql = "call update_info(%s, %s, %s);"
                sql = "update students set phone=(%s), mail=(%s) ,status=(%s) where student_id=(%s);"
                cursor.execute(sql, (phone, email,status, student_id))
                print("再见")
                # cursor.execute(sql, (teacher_id, phone, email))
                results = cursor.fetchall()
                print("results=", results)
                insert_result = "修改信息成功"
            except Exception as err:
                insert_result = "修改信息失败"
                pass
            db.commit()
            # POST显示数据
            sql_list = "select * from students where student_id=(%s);"
            cursor.execute(sql_list, student_id)
            results = cursor.fetchall()
            # print(results)

    return flask.render_template('administrator/update_student.html', search_result=search_result,
                                 insert_result=insert_result, results=results)

@app.route('/delete_student', methods=['GET', "POST"])
def delete_student():
    search_result = ''
    insert_result = ''
    results = []
    if flask.request.method == 'POST':
        student_id = flask.request.values.get("student_id", "")
        class_id = flask.request.values.get("class_id", "")
        # print("teacher_id:", teacher_id, "phone : ", phone, "email: ", email)  # 打印出这三个输入的信息
        # print("teacher_id=",teacher_id,"phone=",phone,"email=",email)
        if student_id != '' and class_id == '':  # 选择第一行
            # print("查询，teacher_id=",teacher_id)
            sql_list = "select * from students where student_id=(%s);"
            cursor.execute(sql_list, student_id)  # 执行相应的sql语句
            results = cursor.fetchall()
            # print("results=",results)
            if len(results) != 0:
                search_result = "查询成功！"
            else:  # 选择第二行
                search_result = "查询失败！"
        else:
            # print("修改，teacher_id=",teacher_id,"phone=",phone,"email=",email)
            for p in student_id:
                if p > '9' or p < '0':
                    insert_result += "学号格式有误、"
                    break
            for p in class_id:
                if p > '9' or p < '0':
                    insert_result += "班级号格式有误、"
                    break
            if insert_result != '':
                # return flask.render_template('update_professor.html', insert_result=insert_result)
                return flask.render_template('administrator/delete_student.html', search_result=search_result,
                                             insert_result=insert_result, results=results)
            try:
                # 信息存入数据库
                # sql = "call update_info(%s, %s, %s);"
                sql = "delete from students where student_id=(%s) and class_id=(%s);"  # 需要考虑级联删除的问题
                cursor.execute(sql, (student_id, class_id))
                # cursor.execute(sql, (teacher_id, phone, email))
                results = cursor.fetchall()
                print("results=", results)
                insert_result = "删除成功"
            except Exception as err:
                insert_result = "删除失败"
                pass
            db.commit()
            # POST显示数据
            sql_list = "select * from teachers where teacher_id=(%s);"
            cursor.execute(sql_list, student_id)
            results = cursor.fetchall()
            # print(results)
    return flask.render_template('administrator/delete_student.html', search_result=search_result,
                                 insert_result=insert_result, results=results)

@app.route('/close_register', methods=['GET', "POST"]) #关闭注册，这个很有意思
def close_register():#关闭注册，首先得禁止学生进行选课，，这个体现在学生那一部分
    search_result = '' #记录查询结果
    results = [] #记录表单
    results2= []
    if flask.request.method == 'POST':
            try:
                # 信息存入数据库
                # sql = "call update_info(%s, %s, %s);"
                sql1 = "select a.student_id,a.name,sum(tuition) from students as a,student_takes as b,takes as c,courses as d where a.student_id=b.student_id and b.takes_id=c.takes_id and c.course_id = d.course_id group by student_id;"
                cursor.execute(sql1)
                # cursor.execute(sql, (teacher_id, phone, email))
                results = cursor.fetchall()
                sql2="select a.student_id,a.name,c.takes_id,c.course_id,c.semester_id,c.teacher_id,d.name as '课程名',d.tuition from students as a,student_takes as b,takes as c,courses as d where a.student_id=b.student_id and b.takes_id=c.takes_id and c.course_id = d.course_id;"
                cursor.execute(sql2)
                results2=cursor.fetchall()
                search_result = "关闭注册成功,并显示各个学生应当提交的金额！已禁止学生端的选课、退课功能"

                f2 = open("closeRegisterFlag.txt", encoding="utf-8", mode='r+')
                f2.write("1")

            except Exception as err:
                search_result = "关闭注册失败"
                pass
            db.commit()
            # POST显示数据
            # sql_list = "select * from teachers where teacher_id=(%s);"
            # cursor.execute(sql_list, teacher_id)
            # results = cursor.fetchall()
            # print(results)

    return flask.render_template('administrator/close_register.html', search_result=search_result, results=results,results2=results2)

#访问不存在的网页地址时显示错误信息
@app.errorhandler(404)
def not_found(e):
    return flask.render_template('404.html')

#出现异常，代码崩溃时显示精简信息
@app.errorhandler(500)
def internal_server_error(e):
    return flask.render_template('500.html')

# 启动服务器
app.debug = True
# 增加session会话保护(任意字符串,用来对session进行加密)
app.secret_key = 'carson'
try:
    app.run()
except Exception as err:
    print(err)
    db.close()  # 关闭数据库连接
