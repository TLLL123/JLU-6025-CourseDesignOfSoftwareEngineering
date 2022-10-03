import pymysql  # 连接数据库
import random

db = pymysql.connect(host='47.95.148.117', port=3306, charset='utf8', database="course_registration_system",
                     user='root', password='Jlu123456')
cursor = db.cursor()
first_name = ["王", "李", "张", "刘", "赵", "蒋", "孟", "陈", "徐", "杨", "沈", "马", "高", "殷", "上官", "钟", "常", "谢"]

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

def addStudent(num):
    # 随机名字
    name = random.choice(first_name)
    for i in range(num):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xfe)
        val = f'{head:x} {body:x}'
        str = bytes.fromhex(val).decode('gb2312')
        name += str

# addCampus()
# addMajorClass()