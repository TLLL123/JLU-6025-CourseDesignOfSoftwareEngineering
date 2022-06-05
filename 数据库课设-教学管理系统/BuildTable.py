buildTable={
    "course": '''
CREATE TABLE course (
course_id varchar(50) NOT NULL,
title varchar(50) DEFAULT NULL,
dept_name varchar(50) DEFAULT NULL,
credits varchar(50) DEFAULT NULL,
PRIMARY KEY (course_id)
);
''',

    "section":'''
CREATE TABLE section (
course_id varchar(50) NOT NULL,
sec_id varchar(50) NOT NULL,
semester varchar(50) NOT NULL,
year varchar(50) NOT NULL,
building varchar(50) DEFAULT NULL,
room_number varchar(50) DEFAULT NULL,
time_slot_id varchar(50) DEFAULT NULL,
PRIMARY KEY (course_id,sec_id,semester,year),
FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE ON UPDATE CASCADE
)''',

    "instructor":'''
CREATE TABLE instructor (
ID varchar(50) NOT NULL,
name varchar(50) DEFAULT NULL,
dept_name varchar(50) DEFAULT NULL,
salary varchar(50) DEFAULT NULL,
PRIMARY KEY (ID)
)''',

    "teaches":'''
CREATE TABLE teaches (
ID varchar(50) NOT NULL,
course_id varchar(50) NOT NULL,
sec_id varchar(50) NOT NULL,
semester varchar(50) NOT NULL,
year varchar(50) NOT NULL,
PRIMARY KEY (ID,course_id,sec_id,semester,year),
FOREIGN KEY (ID) REFERENCES instructor (ID) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (course_id,sec_id,semester,year) REFERENCES section (course_id,sec_id,semester,year) ON DELETE CASCADE ON UPDATE CASCADE
)''',

    "student":'''
CREATE TABLE student (
ID varchar(50) NOT NULL,
name varchar(50) DEFAULT NULL,
dept_name varchar(50) DEFAULT NULL,
tot_cred varchar(50) DEFAULT NULL,
PRIMARY KEY (ID)
)''',

    "takes":'''
CREATE TABLE takes (
ID varchar(50) NOT NULL,
course_id varchar(50) NOT NULL,
sec_id varchar(50) NOT NULL,
semester varchar(50) NOT NULL,
year varchar(50) NOT NULL,
grade varchar(50) DEFAULT NULL,
PRIMARY KEY (ID,course_id,sec_id,semester,year),
FOREIGN KEY (ID) REFERENCES student (ID) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (course_id,sec_id,semester,year) REFERENCES section (course_id,sec_id,semester,year) ON DELETE CASCADE ON UPDATE CASCADE
);''',
    
    "studentAccount":'''
CREATE TABLE studentAccount (
ID varchar(50) NOT NULL,
password varchar(50) DEFAULT NULL,
PRIMARY KEY (ID),
FOREIGN KEY (ID) REFERENCES student(ID)
)''',

    "instructorAccount":'''
CREATE TABLE instructorAccount (
ID varchar(50) NOT NULL,
password varchar(50) DEFAULT NULL,
PRIMARY KEY (ID),
FOREIGN KEY (ID) REFERENCES instructor(ID)
)'''
}