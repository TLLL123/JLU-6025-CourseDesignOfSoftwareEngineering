import pymysql  # 连接数据库
import random
import radar

db = pymysql.connect(host='47.95.148.117', port=3306, charset='utf8', database="course_registration_system",
                     user='root', password='Jlu123456')
cursor = db.cursor()
first_name = ["王", "李", "张", "刘", "赵", "蒋", "孟", "陈", "徐", "杨", "沈", "马", "高", "殷", "上官", "钟", "常", "谢"]
gend = ['男', '女']
last_mail = ['@163.com', '@qq.com', '@gmail.com', '@yeah.net']

def addCampus():
    sql = "insert into campus(campus_id,name) values(%s,%s)"
    college1 = ['哲学社会学院', '文学院', '考古学院', '体育学院', '医学院', '经济学院']
    for i in range(6):
        id = str(0) + str(i+3)
        name = college1[i]
        cursor.execute(sql, (id, name))
        db.commit()
    college2 = ['法学院', '行政学院', '商学院', '马克思主义学院', '东北亚学院', '公共外交学院', '数学学院', '物理学院', '化学学院', '生命科学学院']
    for i in range(10):
        id = str(1) + str(i)
        name = college2[i]
        cursor.execute(sql, (id, name))
        db.commit()
    college3 = ['机械与航空航天工程学院', '汽车工程学院', '材料科学与工程学院', '交通学院', '生物与农业工程学院', '食品科学与工程学院', '电子科学与工程学院', '通信工程学院', '软件学院']
    cursor.execute(sql, ('20', college3[0]))
    db.commit()
    for i in range(8):
        id = str(2) + str(i+2)
        name = college3[i+1]
        cursor.execute(sql, (id, name))
        db.commit()
    print('学院添加完毕！')

def getMajor():
    arr = []
    with open("major.txt", encoding="utf_8") as file:
        lines = file.readlines()
        for line in lines:  # 得到left和right
            line = str(line).replace("\n", "")
            pos = line.split(" ", 10)
            arr.append(pos)
    # print(arr)
    return arr


def addMajorClass():
    sql = "insert into majors(major_id,name,campus_id,optional_course_credis,require_course_credis) values(%s,%s,%s,%s,%s)"
    sql_1 = "insert into classes(class_id,major_id) values(%s,%s)"
    major1 = getMajor()
    num = 7
    for i in range(3):
        for j in range(10):
            if i==0 and j ==0:
                continue
            c_id = str(i)
            c_id += str(j)
            nu={19:0,20:0,21:0}
            for k in major1[i*10+j-1]:
                m_id = '00'
                if num < 10:
                    m_id += '00' + str(num)
                elif num < 100:
                    m_id += '0' + str(num)
                else:
                    m_id += str(num)
                num += 1
                cursor.execute(sql, (m_id, k, c_id, '30', '50'))
                db.commit()
                for l in range(3):
                    cl = c_id + str(l+19)
                    if cl=='2121' or cl=='0120' or cl=='0121' or cl=='0120' or cl=='0221' or cl=='0919':
                        continue
                    for m in range(2):
                        nu[l+19]+=1
                        if nu[l+19]<10:
                            cl_id = cl + '0' + str(nu[l+19])
                        else:
                            cl_id = cl + str(nu[l + 19])
                        cursor.execute(sql_1, (cl_id, m_id))
                        db.commit()
    print('专业班级添加完毕！')

def addCourse():
    num = 11
    mCourse = []
    gCourse = ['微积分A2', '近代史', '思想政治', '微积分A3', '军事理论']
    tuition1 = ['1500', '2100', '2400', '3600', '1200']
    sql = "insert into courses(course_id,name,credit,hours,type,tuition) values(%s,%s,%s,%s,%s,%s)"
    sql_1 = "insert into majors_courses(major_id,course_id,grade) values(%s,%s,%s)"
    with open("course.txt", encoding="utf_8") as file:
        lines = file.readlines()
        for line in lines:  # 得到left和right
            line = str(line).replace("\n", "")
            pos = line.split(" ", 10)
            mCourse.append(pos)
    for i in mCourse:
        for j in i:
            co_id = '000'
            m_id = '00'
            if num-4 < 10:
                m_id += '00' + str(num-4)
            elif num-4 < 100:
                m_id += '0' + str(num-4)
            else:
                m_id += str(num-4)
            if num < 100:
                co_id += '0' + str(num)
            else:
                co_id += str(num)
            num+=1
            cursor.execute(sql, (co_id, j, '3', '32', '必修课', random.choice(tuition1)))
            db.commit()
            cursor.execute(sql_1, (m_id, co_id, '1'))
            db.commit()
    for i in gCourse:
        co_id = '000' + str(num)
        num+=1
        cursor.execute(sql, (co_id, i, '3', '32', '必修课', random.choice(tuition1)))
        db.commit()
        for j in range(98):
            m_id = '00'
            if j+7 < 10:
                m_id += '00' + str(j+7)
            elif j+7 < 100:
                m_id += '0' + str(j+7)
            else:
                m_id += str(j+7)
            cursor.execute(sql_1, (m_id, co_id, '1'))
            db.commit()
    print('课程添加完毕！')

def addSem():
    sql = "insert into semesters(semester_id,school_year,start_date,total_weeks,season) values(%s,%s,%s,%s,%s)"
    num = 4
    s_id = '0000'
    s_year = ['2019','2020','2020','2021']
    s_date = ['09-01','03-01']
    season = ['秋季', '春季']
    for i in range(4):
        s_id1 = s_id + str(num)
        num += 1
        s_date1 = s_year[i] + '-' + s_date[i%2]
        cursor.execute(sql, (s_id1, s_year[i], s_date1, '20', season[i%2]))
        db.commit()
    print("学期添加成功！")

def addClassroom():
    sql = "insert into classrooms(classroom_id,name,building_id,type,capacity) values(%s,%s,%s,%s,%s)"
    build = ['00001','00002','00003','00004','00005']
    c_id1 = '0001'
    name1 = '10'
    for i in range(9):
        c_id = c_id1 + str(i+1)
        name = name1 + str(i+1)
        cursor.execute(sql, (c_id, name, random.choice(build), '小教室', '10'))
        db.commit()
    print('教室添加完毕！')

def create_phone():
	#第二位数
	second = [3, 4, 5, 7, 8, 9][random.randint(0, 5)]
	#第三位数
	third = {
		3: random.randint(0, 9),
		4: [5, 7, 9][random.randint(0, 2)],
		5: [i for i in range(10) if i != 4][random.randint(0, 8)],
		7: [i for i in range(10) if i not in [4, 9]][random.randint(0,7)],
		8: random.randint(0, 9),
		9: random.randint(0, 9)
	}[second]
	#最后8位数
	suffix = random.randint(9999999, 100000000)
	#拼接手机号
	return "1{}{}{}".format(second, third, suffix)

def addStudent(class_id,num,name_num):
    sql = "insert into students(student_id,name,state,class_id,gender,birthday,phone,mail,social_security_number,status,graduation_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # 随机名字
    birth = radar.random_date("2000-01-01", "2003-01-01")
    phone = create_phone()
    mail = phone + random.choice(last_mail)
    g_date = '20' + str(int(class_id[2:4]) + 4) + '-06-01'
    if num < 10:
        s_id = class_id + '0' + str(num)
    else:
        s_id = class_id + str(num)
    name = random.choice(first_name)
    for i in range(name_num):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xfe)
        val = f'{head:x} {body:x}'
        str_1 = bytes.fromhex(val).decode('gb2312')
        name += str_1
    cursor.execute(sql, (s_id, name, 1, class_id, random.choice(gend), birth, phone, mail, s_id, 'undergraduate', g_date))
    db.commit()

def addTeacher(num, name_num):
    sql = "insert into teachers(teacher_id,name,gender,birthday,phone,mail,social_security_number,status,department) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    birth = radar.random_date("1960-01-01", "1990-01-01")
    depart = ['Biology', 'Comp.Sci', 'Elec.Eng.', 'Finance', 'History', 'Music', 'Physics']
    status1 = ['emeritus professor', 'associate professor', 'professor']
    phone = create_phone()
    mail = phone + random.choice(last_mail)
    name = random.choice(first_name)
    if num < 10:
        t_id = '00000' + str(num)
    elif num < 100:
        t_id = '0000' + str(num)
    elif num < 1000:
        t_id = '000' + str(num)
    else:
        t_id = '00' + str(num)
    for i in range(name_num):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xfe)
        val = f'{head:x} {body:x}'
        str_1 = bytes.fromhex(val).decode('gb2312')
        name += str_1
    cursor.execute(sql, (t_id, name, random.choice(gend), birth, phone, mail, t_id, random.choice(status1), random.choice(depart)))
    db.commit()

# addCampus()
# addMajorClass()
# addCourse()
# addSem()
# addClassroom()