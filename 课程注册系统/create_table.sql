/*
Navicat MySQL Data Transfer

Source Server         : python_manage_database
Source Server Version : 50561
Source Host           : localhost:3306
Source Database       : course_registration_system

Target Server Type    : MYSQL
Target Server Version : 50561
File Encoding         : 65001

Date: 2022-09-14 14:00:43
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for buildings
-- ----------------------------
DROP TABLE IF EXISTS `buildings`;
CREATE TABLE `buildings` (
  `building_id` char(5) NOT NULL,
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`building_id`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of buildings
-- ----------------------------
INSERT INTO `buildings` VALUES ('00004', '三教');
INSERT INTO `buildings` VALUES ('00002', '李四光楼');
INSERT INTO `buildings` VALUES ('00005', '萃文楼');
INSERT INTO `buildings` VALUES ('00001', '逸夫楼');
INSERT INTO `buildings` VALUES ('00003', '鼎新楼');

-- ----------------------------
-- Table structure for campus
-- ----------------------------
DROP TABLE IF EXISTS `campus`;
CREATE TABLE `campus` (
  `campus_id` char(2) NOT NULL,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`campus_id`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of campus
-- ----------------------------
INSERT INTO `campus` VALUES ('02', '外国语学院');
INSERT INTO `campus` VALUES ('09', '管理学院');
INSERT INTO `campus` VALUES ('01', '艺术学院');
INSERT INTO `campus` VALUES ('21', '计算机学院');

-- ----------------------------
-- Table structure for classes
-- ----------------------------
DROP TABLE IF EXISTS `classes`;
CREATE TABLE `classes` (
  `class_id` char(6) NOT NULL,
  `major_id` char(5) DEFAULT NULL,
  PRIMARY KEY (`class_id`),
  KEY `classes_ibfk_1` (`major_id`),
  CONSTRAINT `classes_ibfk_1` FOREIGN KEY (`major_id`) REFERENCES `majors` (`major_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of classes
-- ----------------------------
INSERT INTO `classes` VALUES ('212101', '00001');
INSERT INTO `classes` VALUES ('212102', '00001');
INSERT INTO `classes` VALUES ('022101', '00002');
INSERT INTO `classes` VALUES ('012001', '00003');
INSERT INTO `classes` VALUES ('012101', '00003');
INSERT INTO `classes` VALUES ('022102', '00003');
INSERT INTO `classes` VALUES ('091907', '00006');

-- ----------------------------
-- Table structure for classrooms
-- ----------------------------
DROP TABLE IF EXISTS `classrooms`;
CREATE TABLE `classrooms` (
  `classroom_id` char(5) NOT NULL,
  `name` varchar(30) NOT NULL,
  `building_id` char(5) DEFAULT NULL,
  `type` varchar(20) NOT NULL,
  `capacity` smallint(6) NOT NULL,
  PRIMARY KEY (`classroom_id`),
  KEY `building_id` (`building_id`),
  CONSTRAINT `classrooms_ibfk_1` FOREIGN KEY (`building_id`) REFERENCES `buildings` (`building_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of classrooms
-- ----------------------------
INSERT INTO `classrooms` VALUES ('00001', '逸夫一阶', '00001', '阶梯教室', '100');
INSERT INTO `classrooms` VALUES ('00002', '逸夫101', '00001', '小教室', '40');
INSERT INTO `classrooms` VALUES ('00003', '李四光一阶', '00002', '阶梯教室', '120');
INSERT INTO `classrooms` VALUES ('00004', '鼎新201', '00003', '会议室', '10');
INSERT INTO `classrooms` VALUES ('00005', '鼎新502', '00003', '研讨室', '5');
INSERT INTO `classrooms` VALUES ('00006', '李四光13阶', '00002', '阶梯教室', '110');
INSERT INTO `classrooms` VALUES ('00007', '三教306', '00004', '小教室', '50');
INSERT INTO `classrooms` VALUES ('00008', '三教428', '00004', '中型教室', '80');
INSERT INTO `classrooms` VALUES ('00009', '萃文9阶', '00005', '阶梯教室', '130');
INSERT INTO `classrooms` VALUES ('00010', '萃文108', '00005', '小教室', '50');

-- ----------------------------
-- Table structure for courses
-- ----------------------------
DROP TABLE IF EXISTS `courses`;
CREATE TABLE `courses` (
  `course_id` char(6) NOT NULL,
  `name` varchar(30) NOT NULL,
  `credit` tinyint(1) NOT NULL,
  `hours` smallint(6) NOT NULL,
  `type` varchar(10) NOT NULL,
  `tuition` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of courses
-- ----------------------------
INSERT INTO `courses` VALUES ('000001', '微积分A1', '4', '48', '必修课', '2000');
INSERT INTO `courses` VALUES ('000002', '思想道德理论', '2', '50', '必修课', '1500');
INSERT INTO `courses` VALUES ('000003', 'Java入门到入土', '2', '24', '选修课', '1300');
INSERT INTO `courses` VALUES ('000004', '数据库原理', '3', '36', '必修课', '1800');
INSERT INTO `courses` VALUES ('000005', '马克思原理', '3', '56', '必修课', '2300');
INSERT INTO `courses` VALUES ('000006', '毛泽东概论', '5', '44', '必修课', '2200');
INSERT INTO `courses` VALUES ('000007', '离散数学A1', '3', '48', '必修课', '2500');
INSERT INTO `courses` VALUES ('000008', 'web程序设计', '2', '40', '选修课', '1600');
INSERT INTO `courses` VALUES ('000009', '程序设计基础', '3', '56', '必修课', '2800');
INSERT INTO `courses` VALUES ('000010', '组合数学', '2', '48', '选修课', '2000');

-- ----------------------------
-- Table structure for login
-- ----------------------------
DROP TABLE IF EXISTS `login`;
CREATE TABLE `login` (
  `name` varchar(20) NOT NULL,
  `passwd` varchar(128) NOT NULL,
  `identity` tinyint(1) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of login
-- ----------------------------
INSERT INTO `login` VALUES ('000001', '123456', '2');
INSERT INTO `login` VALUES ('000002', '123456', '2');
INSERT INTO `login` VALUES ('01210101', '123456', '3');
INSERT INTO `login` VALUES ('02210101', '123456', '3');
INSERT INTO `login` VALUES ('02210201', '123456', '3');
INSERT INTO `login` VALUES ('09190717', '123456', '3');
INSERT INTO `login` VALUES ('21210101', '123456', '3');
INSERT INTO `login` VALUES ('21210201', '123456', '3');
INSERT INTO `login` VALUES ('21210202', '123456', '3');
INSERT INTO `login` VALUES ('21210203', '123456', '3');
INSERT INTO `login` VALUES ('admin', 'admin', '1');

-- ----------------------------
-- Table structure for majors
-- ----------------------------
DROP TABLE IF EXISTS `majors`;
CREATE TABLE `majors` (
  `major_id` char(5) NOT NULL,
  `name` varchar(20) NOT NULL,
  `campus_id` char(2) NOT NULL,
  `optional_course_credis` smallint(6) NOT NULL,
  `require_course_credis` smallint(6) NOT NULL,
  PRIMARY KEY (`major_id`),
  KEY `majors_ibfk_1` (`campus_id`),
  CONSTRAINT `majors_ibfk_1` FOREIGN KEY (`campus_id`) REFERENCES `campus` (`campus_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of majors
-- ----------------------------
INSERT INTO `majors` VALUES ('00001', '计算机科学与技术', '21', '30', '60');
INSERT INTO `majors` VALUES ('00002', '网络空间安全', '21', '20', '56');
INSERT INTO `majors` VALUES ('00003', '英语', '02', '20', '48');
INSERT INTO `majors` VALUES ('00004', '日语', '02', '20', '40');
INSERT INTO `majors` VALUES ('00005', '播音主持', '01', '16', '30');
INSERT INTO `majors` VALUES ('00006', '管理', '09', '40', '55');

-- ----------------------------
-- Table structure for majors_courses
-- ----------------------------
DROP TABLE IF EXISTS `majors_courses`;
CREATE TABLE `majors_courses` (
  `major_id` char(5) NOT NULL,
  `course_id` char(6) NOT NULL,
  `grade` tinyint(1) NOT NULL,
  PRIMARY KEY (`major_id`,`course_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `majors_courses_ibfk_1` FOREIGN KEY (`major_id`) REFERENCES `majors` (`major_id`),
  CONSTRAINT `majors_courses_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of majors_courses
-- ----------------------------
INSERT INTO `majors_courses` VALUES ('00001', '000001', '1');
INSERT INTO `majors_courses` VALUES ('00001', '000002', '1');
INSERT INTO `majors_courses` VALUES ('00001', '000003', '2');
INSERT INTO `majors_courses` VALUES ('00001', '000004', '3');
INSERT INTO `majors_courses` VALUES ('00002', '000001', '1');
INSERT INTO `majors_courses` VALUES ('00002', '000002', '1');
INSERT INTO `majors_courses` VALUES ('00002', '000004', '2');
INSERT INTO `majors_courses` VALUES ('00003', '000002', '1');
INSERT INTO `majors_courses` VALUES ('00004', '000002', '1');
INSERT INTO `majors_courses` VALUES ('00005', '000002', '1');

-- ----------------------------
-- Table structure for sections
-- ----------------------------
DROP TABLE IF EXISTS `sections`;
CREATE TABLE `sections` (
  `section_id` char(10) NOT NULL,
  `start_week` tinyint(4) NOT NULL,
  `end_week` tinyint(4) NOT NULL,
  `start_time` tinyint(4) NOT NULL,
  `end_time` tinyint(4) NOT NULL,
  `weekday` tinyint(1) NOT NULL,
  `teacher_id` char(6) DEFAULT NULL,
  `takes_id` char(8) NOT NULL,
  `classroom_id` char(5) DEFAULT NULL,
  PRIMARY KEY (`section_id`),
  KEY `teacher_id` (`teacher_id`),
  KEY `takes_id` (`takes_id`),
  KEY `classroom_id` (`classroom_id`),
  CONSTRAINT `sections_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`teacher_id`),
  CONSTRAINT `sections_ibfk_2` FOREIGN KEY (`takes_id`) REFERENCES `takes` (`takes_id`),
  CONSTRAINT `sections_ibfk_3` FOREIGN KEY (`classroom_id`) REFERENCES `classrooms` (`classroom_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sections
-- ----------------------------
INSERT INTO `sections` VALUES ('0000000001', '2', '16', '9', '11', '3', '000001', '00000001', '00001');
INSERT INTO `sections` VALUES ('0000000002', '3', '14', '7', '8', '5', '000002', '00000002', '00002');
INSERT INTO `sections` VALUES ('0000000003', '4', '10', '7', '9', '5', '000001', '00000003', '00003');
INSERT INTO `sections` VALUES ('0000000004', '4', '15', '5', '6', '4', '000005', '00000004', '00003');
INSERT INTO `sections` VALUES ('0000000005', '3', '4', '3', '4', '4', '000003', '00102002', '00001');
INSERT INTO `sections` VALUES ('0000000006', '13', '17', '9', '11', '2', '000004', '00102001', '00001');
INSERT INTO `sections` VALUES ('0000000007', '3', '17', '1', '4', '5', '000007', '00102000', '00008');
INSERT INTO `sections` VALUES ('0000000008', '13', '16', '5', '8', '1', '000002', '00001020', '00009');
INSERT INTO `sections` VALUES ('0000000009', '7', '14', '1', '2', '3', '000008', '00001022', '00009');
INSERT INTO `sections` VALUES ('0000000010', '10', '15', '7', '8', '4', '000001', '00001023', '00006');
INSERT INTO `sections` VALUES ('0000000011', '6', '14', '5', '6', '5', '000007', '00102003', '00002');
INSERT INTO `sections` VALUES ('0000000012', '1', '6', '3', '4', '2', '000008', '00000005', '00006');
INSERT INTO `sections` VALUES ('0000000013', '1', '15', '9', '11', '5', '000002', '00000011', '00008');
INSERT INTO `sections` VALUES ('0000000014', '8', '13', '1', '2', '4', '000007', '00000009', '00009');
INSERT INTO `sections` VALUES ('0000000015', '5', '12', '3', '4', '2', '000004', '00102001', '00009');
INSERT INTO `sections` VALUES ('0000000016', '2', '20', '6', '7', '3', '000006', '00001024', '00001');
INSERT INTO `sections` VALUES ('0000000017', '6', '9', '4', '18', '1', '000005', '00102002', '00003');
INSERT INTO `sections` VALUES ('0000000018', '1', '17', '1', '2', '1', '000005', '00102005', '00005');
INSERT INTO `sections` VALUES ('0000000019', '13', '17', '2', '3', '4', '000003', '00102006', '00002');
INSERT INTO `sections` VALUES ('0000000020', '1', '14', '6', '7', '3', '000007', '00102007', '00003');
INSERT INTO `sections` VALUES ('0000000021', '13', '17', '2', '3', '4', '000005', '00100200', '00006');

-- ----------------------------
-- Table structure for semesters
-- ----------------------------
DROP TABLE IF EXISTS `semesters`;
CREATE TABLE `semesters` (
  `semester_id` char(5) NOT NULL,
  `school_year` smallint(6) NOT NULL,
  `start_date` date NOT NULL,
  `total_weeks` tinyint(4) NOT NULL,
  `season` enum('秋季','春季') NOT NULL,
  PRIMARY KEY (`semester_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of semesters
-- ----------------------------
INSERT INTO `semesters` VALUES ('00001', '2021', '2021-09-01', '20', '秋季');
INSERT INTO `semesters` VALUES ('00002', '2022', '2022-03-01', '20', '春季');
INSERT INTO `semesters` VALUES ('00003', '2022', '2022-08-27', '22', '秋季');

-- ----------------------------
-- Table structure for students
-- ----------------------------
DROP TABLE IF EXISTS `students`;
CREATE TABLE `students` (
  `student_id` char(8) NOT NULL,
  `name` varchar(30) NOT NULL,
  `state` tinyint(1) NOT NULL,
  `class_id` char(6) DEFAULT NULL,
  `gender` varchar(6) NOT NULL,
  `birthday` date NOT NULL,
  `phone` char(11) DEFAULT NULL,
  `mail` varchar(30) DEFAULT NULL,
  `social_security_number` varchar(30) DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `graduation_date` date DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  KEY `idx_name` (`name`) USING BTREE,
  KEY `students_ibfk_1` (`class_id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of students
-- ----------------------------
INSERT INTO `students` VALUES ('01210101', '李诗情', '1', '012101', '女', '2000-08-09', '1796257974', '1796257974@qq.com', '01210101', 'undergraduate', '2023-06-01');
INSERT INTO `students` VALUES ('02210101', '肖鹤云', '1', '022101', '男', '2001-04-04', '18033334444', '1803333444@qq.com', '02210101', 'Master student', '2024-06-01');
INSERT INTO `students` VALUES ('02210201', '谷雯', '1', '022102', '女', '2001-04-04', '18955556666', null, '02210201', 'Doctoral student', '2023-06-01');
INSERT INTO `students` VALUES ('09190717', '邓秋怡', '1', '091907', '女', '2002-02-20', '18011112222', '18011112222@qq.com', '09190717', 'undergraduate', '2024-06-01');
INSERT INTO `students` VALUES ('21210101', '于哲', '1', '212101', '男', '2000-01-02', '18977778888', '7788@163.com', '21210101', 'undergraduate', '2023-06-01');
INSERT INTO `students` VALUES ('21210201', '周涵易', '1', '212102', '女', '2001-04-05', '18355559999', '18355559999@qq.com', '21210201', 'Doctoral student', '2024-06-01');
INSERT INTO `students` VALUES ('21210202', '陆宏伟', '1', '212102', '男', '2002-08-10', null, null, '21210202', 'Master student', '2023-06-01');
INSERT INTO `students` VALUES ('21210203', '魏翰林', '1', '212102', '男', '2002-02-20', '18022228888', '2288@163.com', '21210203', 'undergraduate', '2024-06-01');

-- ----------------------------
-- Table structure for student_takes
-- ----------------------------
DROP TABLE IF EXISTS `student_takes`;
CREATE TABLE `student_takes` (
  `student_id` char(8) NOT NULL,
  `takes_id` char(8) NOT NULL,
  `score` float(4,1) DEFAULT NULL,
  PRIMARY KEY (`student_id`,`takes_id`),
  KEY `takes_id` (`takes_id`),
  CONSTRAINT `student_takes_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `student_takes_ibfk_2` FOREIGN KEY (`takes_id`) REFERENCES `takes` (`takes_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of student_takes
-- ----------------------------
INSERT INTO `student_takes` VALUES ('01210101', '00000002', '91.0');
INSERT INTO `student_takes` VALUES ('02210101', '00000003', null);
INSERT INTO `student_takes` VALUES ('02210101', '00100200', null);
INSERT INTO `student_takes` VALUES ('09190717', '00000003', null);
INSERT INTO `student_takes` VALUES ('09190717', '00000004', null);
INSERT INTO `student_takes` VALUES ('09190717', '00000010', '89.0');
INSERT INTO `student_takes` VALUES ('09190717', '00102002', null);
INSERT INTO `student_takes` VALUES ('09190717', '00102005', null);
INSERT INTO `student_takes` VALUES ('09190717', '00102006', null);
INSERT INTO `student_takes` VALUES ('21210101', '00000001', '90.0');
INSERT INTO `student_takes` VALUES ('21210101', '00000004', null);
INSERT INTO `student_takes` VALUES ('21210101', '00001020', null);
INSERT INTO `student_takes` VALUES ('21210101', '00001022', null);
INSERT INTO `student_takes` VALUES ('21210101', '00102000', null);
INSERT INTO `student_takes` VALUES ('21210101', '00102001', null);
INSERT INTO `student_takes` VALUES ('21210101', '00102002', null);
INSERT INTO `student_takes` VALUES ('21210201', '00000001', '87.0');
INSERT INTO `student_takes` VALUES ('21210203', '00000002', '92.0');
INSERT INTO `student_takes` VALUES ('21210203', '00000011', '91.0');
INSERT INTO `student_takes` VALUES ('21210203', '00001023', null);

-- ----------------------------
-- Table structure for takes
-- ----------------------------
DROP TABLE IF EXISTS `takes`;
CREATE TABLE `takes` (
  `takes_id` char(8) NOT NULL,
  `course_id` char(6) NOT NULL,
  `semester_id` char(5) NOT NULL,
  `teacher_id` char(6) DEFAULT NULL,
  `max_num` smallint(6) NOT NULL,
  `current_num` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`takes_id`),
  KEY `course_id` (`course_id`),
  KEY `semester_id` (`semester_id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `takes_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`),
  CONSTRAINT `takes_ibfk_2` FOREIGN KEY (`semester_id`) REFERENCES `semesters` (`semester_id`),
  CONSTRAINT `takes_ibfk_3` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of takes
-- ----------------------------
INSERT INTO `takes` VALUES ('00000001', '000001', '00001', '000001', '80', '69');
INSERT INTO `takes` VALUES ('00000002', '000002', '00003', '000002', '31', '23');
INSERT INTO `takes` VALUES ('00000003', '000004', '00002', '000001', '110', '101');
INSERT INTO `takes` VALUES ('00000004', '000003', '00002', '000005', '100', '96');
INSERT INTO `takes` VALUES ('00000005', '000001', '00001', '000008', '80', '80');
INSERT INTO `takes` VALUES ('00000006', '000005', '00002', '000003', '35', '30');
INSERT INTO `takes` VALUES ('00000007', '000006', '00002', '000005', '80', '75');
INSERT INTO `takes` VALUES ('00000008', '000007', '00002', '000004', '90', '90');
INSERT INTO `takes` VALUES ('00000009', '000008', '00002', '000007', '100', '100');
INSERT INTO `takes` VALUES ('00000010', '000003', '00002', '000006', '80', '1');
INSERT INTO `takes` VALUES ('00000011', '000006', '00002', '000002', '76', '0');
INSERT INTO `takes` VALUES ('00001020', '000002', '00002', '000008', '40', '40');
INSERT INTO `takes` VALUES ('00001021', '000008', '00002', '000004', '90', '90');
INSERT INTO `takes` VALUES ('00001022', '000007', '00002', '000008', '100', '98');
INSERT INTO `takes` VALUES ('00001023', '000009', '00002', '000001', '95', '91');
INSERT INTO `takes` VALUES ('00001024', '000004', '00002', '000006', '100', '90');
INSERT INTO `takes` VALUES ('00100200', '000010', '00002', '000005', '60', '58');
INSERT INTO `takes` VALUES ('00102000', '000009', '00002', '000007', '110', '100');
INSERT INTO `takes` VALUES ('00102001', '000007', '00002', '000004', '80', '0');
INSERT INTO `takes` VALUES ('00102002', '000008', '00002', '000005', '70', '1');
INSERT INTO `takes` VALUES ('00102003', '000005', '00002', '000007', '15', '0');
INSERT INTO `takes` VALUES ('00102004', '000010', '00002', null, '3', '0');
INSERT INTO `takes` VALUES ('00102005', '000001', '00002', '000005', '3', '1');
INSERT INTO `takes` VALUES ('00102006', '000003', '00002', '000003', '23', '1');
INSERT INTO `takes` VALUES ('00102007', '000008', '00002', '000007', '70', '0');

-- ----------------------------
-- Table structure for teachers
-- ----------------------------
DROP TABLE IF EXISTS `teachers`;
CREATE TABLE `teachers` (
  `teacher_id` char(6) NOT NULL,
  `name` varchar(32) NOT NULL,
  `gender` varchar(6) NOT NULL,
  `birthday` date NOT NULL,
  `phone` char(11) DEFAULT NULL,
  `mail` varchar(30) DEFAULT NULL,
  `social_security_number` varchar(30) DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `department` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`teacher_id`),
  KEY `idx_tname` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of teachers
-- ----------------------------
INSERT INTO `teachers` VALUES ('000001', '梅长苏', '男', '1980-03-04', '18045621789', '1846@qq.com', '000001', 'emeritus professor', 'Biology');
INSERT INTO `teachers` VALUES ('000002', '铁心兰', '女', '1981-06-05', '12345678904', '123455@qq.com', '000002', 'associate professor', 'Comp.Sci.');
INSERT INTO `teachers` VALUES ('000003', '花无缺', '男', '1980-07-10', '16287359841', '1598@qq.com', '000003', 'professor', 'Elec.Eng.');
INSERT INTO `teachers` VALUES ('000004', '纪晓岚', '男', '1976-02-19', '18012341234', '1801@qq.com', '000004', 'emeritus professor', 'Finance');
INSERT INTO `teachers` VALUES ('000005', '唐伯虎', '男', '1974-10-01', '18056785678', '5678@qq.com', '000005', 'associate professor', 'History');
INSERT INTO `teachers` VALUES ('000006', '白素贞', '女', '1983-05-26', '18978907890', '1891@qq.com', '000006', 'professor', 'Music');
INSERT INTO `teachers` VALUES ('000007', '赵敏', '女', '1985-03-23', '18912341234', '1892@qq.com', '000007', 'emeritus professor', 'Physics');
INSERT INTO `teachers` VALUES ('000008', '黄蓉', '女', '1979-06-12', '13734563456', '3456@qq.com', '000008', 'associate professor', 'Comp.Sci.');

-- ----------------------------
-- Table structure for teacher_teaches
-- ----------------------------
DROP TABLE IF EXISTS `teacher_teaches`;
CREATE TABLE `teacher_teaches` (
  `teacher_id` char(6) NOT NULL,
  `course_id` char(6) NOT NULL,
  PRIMARY KEY (`teacher_id`,`course_id`),
  KEY `teacher_teaches_ibfk_2` (`course_id`),
  CONSTRAINT `teacher_teaches_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`teacher_id`),
  CONSTRAINT `teacher_teaches_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of teacher_teaches
-- ----------------------------
INSERT INTO `teacher_teaches` VALUES ('000001', '000001');
INSERT INTO `teacher_teaches` VALUES ('000002', '000001');
INSERT INTO `teacher_teaches` VALUES ('000005', '000001');
INSERT INTO `teacher_teaches` VALUES ('000008', '000001');
INSERT INTO `teacher_teaches` VALUES ('000002', '000002');
INSERT INTO `teacher_teaches` VALUES ('000008', '000002');
INSERT INTO `teacher_teaches` VALUES ('000003', '000003');
INSERT INTO `teacher_teaches` VALUES ('000005', '000003');
INSERT INTO `teacher_teaches` VALUES ('000006', '000003');
INSERT INTO `teacher_teaches` VALUES ('000001', '000004');
INSERT INTO `teacher_teaches` VALUES ('000006', '000004');
INSERT INTO `teacher_teaches` VALUES ('000003', '000005');
INSERT INTO `teacher_teaches` VALUES ('000007', '000005');
INSERT INTO `teacher_teaches` VALUES ('000002', '000006');
INSERT INTO `teacher_teaches` VALUES ('000005', '000006');
INSERT INTO `teacher_teaches` VALUES ('000004', '000007');
INSERT INTO `teacher_teaches` VALUES ('000008', '000007');
INSERT INTO `teacher_teaches` VALUES ('000002', '000008');
INSERT INTO `teacher_teaches` VALUES ('000004', '000008');
INSERT INTO `teacher_teaches` VALUES ('000005', '000008');
INSERT INTO `teacher_teaches` VALUES ('000007', '000008');
INSERT INTO `teacher_teaches` VALUES ('000001', '000009');
INSERT INTO `teacher_teaches` VALUES ('000007', '000009');
INSERT INTO `teacher_teaches` VALUES ('000002', '000010');
INSERT INTO `teacher_teaches` VALUES ('000005', '000010');

-- ----------------------------
-- View structure for stutake_sec_takes
-- ----------------------------
DROP VIEW IF EXISTS `stutake_sec_takes`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `stutake_sec_takes` AS select `st`.`student_id` AS `student_id`,`st`.`takes_id` AS `takes_id`,`ta`.`course_id` AS `course_id`,`ta`.`semester_id` AS `semester_id`,`se`.`teacher_id` AS `teacher_id`,`se`.`classroom_id` AS `classroom_id`,`se`.`start_week` AS `start_week`,`se`.`end_week` AS `end_week`,`se`.`weekday` AS `weekday`,`se`.`start_time` AS `start_time`,`se`.`end_time` AS `end_time` from ((`student_takes` `st` join `sections` `se`) join `takes` `ta`) where ((`st`.`takes_id` = `se`.`takes_id`) and (`se`.`takes_id` = `ta`.`takes_id`)) ;

-- ----------------------------
-- View structure for takes_sections
-- ----------------------------
DROP VIEW IF EXISTS `takes_sections`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `takes_sections` AS select `t`.`takes_id` AS `ta1_id`,`t`.`course_id` AS `course_id`,`t`.`semester_id` AS `semester_id`,`t`.`teacher_id` AS `t1_id`,`s`.`teacher_id` AS `t2_id`,`t`.`max_num` AS `max_num`,`s`.`section_id` AS `section_id`,`s`.`start_week` AS `start_week`,`s`.`end_week` AS `end_week`,`s`.`start_time` AS `start_time`,`s`.`end_time` AS `end_time`,`s`.`weekday` AS `weekday`,`s`.`takes_id` AS `ta2_id`,`s`.`classroom_id` AS `classroom_id` from (`takes` `t` left join `sections` `s` on((`s`.`takes_id` = `t`.`takes_id`))) ;

-- ----------------------------
-- View structure for v_classrooms_buildings
-- ----------------------------
DROP VIEW IF EXISTS `v_classrooms_buildings`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `v_classrooms_buildings` AS select `c`.`building_id` AS `building_id`,`b`.`name` AS `building_name`,`c`.`classroom_id` AS `classroom_id`,`c`.`name` AS `classroom_name`,`c`.`type` AS `type`,`c`.`capacity` AS `capacity` from (`classrooms` `c` join `buildings` `b`) where (`c`.`building_id` = `b`.`building_id`) ;

-- ----------------------------
-- Procedure structure for addCourse
-- ----------------------------
DROP PROCEDURE IF EXISTS `addCourse`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `addCourse`(in name varchar(30),in credit tinyint,in hours smallint,type varchar(10))
begin
declare id char(6);
set @val=(select course_id from courses ORDER BY course_id desc LIMIT 0,1);
set id=(select addOne(@val,6));
if credit<10 and hours<100 then
insert into courses values(id,name,credit,hours,type);
else
select '学分或学时输入有误';
end if;
end
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for addSections
-- ----------------------------
DROP PROCEDURE IF EXISTS `addSections`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `addSections`(in t_id char(8),in s_week int,in e_week int,in s_time int,in e_time int,in weekday int)
begin
declare s_id char(10);
set @val=(select section_id from sections ORDER BY section_id desc LIMIT 0,1);
set s_id=(select addOne(@val,10));
if s_week<=e_week and s_time<=e_time and weekday<=7 and weekday>0 then
insert into sections values(s_id,s_week,e_week,s_time,e_time,weekday,null,t_id,null);
else
select '最大人数课程时间等信息输入有误';
end if;
end
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for addSem
-- ----------------------------
DROP PROCEDURE IF EXISTS `addSem`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `addSem`(in s_year smallint,in s_date date,in weeks tinyint,in season varchar(10))
begin
declare id char(5);
set @val=(select semester_id from semesters ORDER BY semester_id desc LIMIT 0,1);
set id=(select addOne(@val,5));
if s_year<10000 and s_year>1000 and weeks<100 then
insert into semesters values(id,s_year,s_date,weeks,season);
else
select '学年周数等信息输入有误';
end if;
end
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for addTakes
-- ----------------------------
DROP PROCEDURE IF EXISTS `addTakes`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `addTakes`(in c_name varchar(30),in s_year int,in season1 varchar(10),in max_num int,
                                             in s_week int,in e_week int,in s_time int,in e_time int,in weekday int)
begin
declare t_id char(8);
declare s_id char(10);
declare c_id char(6);
declare se_id char(5);
set @val=(select takes_id from takes ORDER BY takes_id desc LIMIT 0,1);
set t_id=(select addOne(@val,8));
set @val=(select section_id from sections ORDER BY section_id desc LIMIT 0,1);
set s_id=(select addOne(@val,10));
set c_id=(select course_id from courses where name=c_name);
set se_id=(select semester_id from semesters where s_year=school_year and season1=season);
if max_num<1000 and s_week<e_week and s_time<e_time and weekday<7 and weekday>0 then
insert into takes values(t_id,c_id,se_id,null,max_num,0);
insert into sections values(s_id,s_week,e_week,s_time,e_time,weekday,null,t_id,null);
else
select '最大人数课程时间等信息输入有误';
end if;
end
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for addTakes1
-- ----------------------------
DROP PROCEDURE IF EXISTS `addTakes1`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `addTakes1`(in c_name varchar(30),in s_year int,in season1 varchar(10),in max_num int)
begin
declare t_id char(8);
declare c_id char(6);
declare se_id char(5);
set @val=(select takes_id from takes ORDER BY takes_id desc LIMIT 0,1);
set t_id=(select addOne(@val,8));
set c_id=(select course_id from courses where name=c_name);
set se_id=(select semester_id from semesters where s_year=school_year and season1=season);
if max_num<1000 then
insert into takes values(t_id,c_id,se_id,null,max_num,0);
else
select '最大人数课程时间等信息输入有误';
end if;
end
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for available_classrooms
-- ----------------------------
DROP PROCEDURE IF EXISTS `available_classrooms`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `available_classrooms`(IN `in_week` tinyint,IN `in_day` tinyint,IN `in_start` tinyint,IN `in_end` tinyint,IN `in_sem` char(5))
BEGIN
	select * from v_classrooms_buildings
	where classroom_id not in
 (select classroom_id from sections as s, takes as t
	where start_week<=in_week and end_week>=in_week and start_time<=in_end and end_time>=in_start and weekday=in_day and s.takes_id=t.takes_id and semester_id=in_sem);



END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for chooseClass
-- ----------------------------
DROP PROCEDURE IF EXISTS `chooseClass`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `chooseClass`(in section1_id char(10),in class_name varchar(30))
begin
declare c_id char(5);
declare num smallint;
declare s_id char(10);
declare s_week tinyint;
declare e_week tinyint;
declare s_time tinyint;
declare e_time tinyint;
declare weekd tinyint;
declare c_max smallint;
declare t_max smallint;
set c_id=(select classroom_id from classrooms where name=class_name);
set c_max=(select capacity from classrooms where classroom_id=c_id);
set @t_id=(select takes_id from sections where section_id=section1_id);
set t_max=(select max_num from takes where takes_id=@t_id);
CREATE TEMPORARY TABLE if not exists c_sections
as
select section_id,start_week,end_week,start_time,end_time,weekday
from sections s left join classrooms c on s.classroom_id=c.classroom_id
where s.classroom_id=c_id;
set num=(select count(*) from c_sections);
set @judge=0;
outer_label: begin
while num>0 do -- 循环开始
set num = num-1;
set s_id=(select section_id from c_sections ORDER BY section_id desc LIMIT 0,1);
set s_week=(select start_week from c_sections where section_id=s_id);
set e_week=(select end_week from c_sections where section_id=s_id);
set s_time=(select start_time from c_sections where section_id=s_id);
set e_time=(select end_time from c_sections where section_id=s_id);
set weekd=(select weekday from c_sections where section_id=s_id);
set @judge=(select judgeChoose(section1_id,s_week,e_week,s_time,e_time,weekd));
delete from c_sections where section_id=s_id;
if @judge=1 then
leave outer_label;
end if;
end while; -- 循环结束
end outer_label;
if @judge=0 then
if c_max>=t_max then
update sections set classroom_id=c_id where section_id=section1_id;
else
select '教室最大人数少于课程人数';
end if;
else
select '教室该时间段已有课程安排';
end if;
drop table c_sections;
end
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for chooseTeach
-- ----------------------------
DROP PROCEDURE IF EXISTS `chooseTeach`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `chooseTeach`(in section1_id char(10),in t_id char(6))
begin
declare num smallint;
declare s_id char(10);
declare s_week tinyint;
declare e_week tinyint;
declare s_time tinyint;
declare e_time tinyint;
declare weekd tinyint;
CREATE TEMPORARY TABLE if not exists t_sections
as
select section_id,start_week,end_week,start_time,end_time,weekday
from sections s left join teachers t on s.teacher_id=t.teacher_id
where s.teacher_id=t_id;
set num=(select count(*) from t_sections);
set @judge=0;
outer_label: begin
while num>0 do -- 循环开始
set num = num-1;
set s_id=(select section_id from t_sections ORDER BY section_id desc LIMIT 0,1);
set s_week=(select start_week from t_sections where section_id=s_id);
set e_week=(select end_week from t_sections where section_id=s_id);
set s_time=(select start_time from t_sections where section_id=s_id);
set e_time=(select end_time from t_sections where section_id=s_id);
set weekd=(select weekday from t_sections where section_id=s_id);
set @judge=(select judgeChoose(section1_id,s_week,e_week,s_time,e_time,weekd));
delete from t_sections where section_id=s_id;
if @judge=1 then
leave outer_label;
end if;
end while; -- 循环结束
end outer_label;
if @judge=0 then
set @t1_id=(select takes_id from sections where section_id=section1_id);
update sections set teacher_id=t_id where section_id=section1_id;
update takes set teacher_id=t_id where takes_id=@t1_id;
else
select '教师该时间段已有课程安排';
end if;
drop table t_sections;
end
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for get_schedule
-- ----------------------------
DROP PROCEDURE IF EXISTS `get_schedule`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `get_schedule`(IN `in_tid` char(6))
BEGIN
	select name, start_week, end_week, start_time, end_time, weekday
	from courses as c, takes as t, sections as s
	where c.course_id=t.course_id and t.teacher_id=in_tid and s.takes_id=t.takes_id;

END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for get_stu_scores
-- ----------------------------
DROP PROCEDURE IF EXISTS `get_stu_scores`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `get_stu_scores`(IN `in_tid` char(6))
BEGIN
	select s.student_id, s.name, c.name, c.course_id, score
	from students as s, student_takes as st, takes as t, courses as c
	where s.student_id=st.student_id and t.takes_id=st.takes_id and t.teacher_id=in_tid and t.course_id=c.course_id;

END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for update_course
-- ----------------------------
DROP PROCEDURE IF EXISTS `update_course`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `update_course`(IN `in_course` char(6),IN `in_teacher` char(6),IN `in_max` smallint,IN `in_room` char(5))
BEGIN
	declare in_takes char(8);
	declare cur_num smallint;
	declare cap smallint;
	declare crash tinyint;
	declare sem_id char(5);
	declare cur_day tinyint;
	declare cur_start_week tinyint;
	declare cur_end_week tinyint;
	declare cur_start_time tinyint;
	declare cur_end_time tinyint;
	declare course_exist tinyint;
	set course_exist=(select count(*) from takes where teacher_id=in_teacher and course_id=in_course);
	if course_exist=0 then
	select "课程选择有误";
	else
	set in_takes=(select takes_id from takes where teacher_id=in_teacher and course_id=in_course);
	set sem_id=(select semester_id from takes where takes_id=in_takes);
	set cur_day=(select weekday from sections where teacher_id=in_teacher and takes_id=in_takes);
	set cur_start_week=(select start_week from sections where teacher_id=in_teacher and takes_id=in_takes);
	set cur_end_week=(select end_week from sections where teacher_id=in_teacher and takes_id=in_takes);
	set cur_start_time=(select start_time from sections where teacher_id=in_teacher and takes_id=in_takes);
	set cur_end_time=(select end_time from sections where teacher_id=in_teacher and takes_id=in_takes);
	create temporary table if not exists rooms as
	select classroom_id from sections as s, takes as t
	where s.takes_id=t.takes_id and semester_id=sem_id and weekday=cur_day and start_week<=cur_end_week and end_week>=cur_start_week and end_time>=cur_start_time and start_time<=cur_end_time and classroom_id=in_room and s.takes_id!=in_takes;
	set crash=(select count(*) from rooms);
	if crash=0 then
	set cur_num=(select current_num from takes where takes_id=in_takes);
	set cap=(select capacity from classrooms where classroom_id=in_room);
	if in_max<=cap and in_max>=cur_num then
	update takes set max_num=in_max where takes_id=in_takes;
	update sections set classroom_id=in_room where teacher_id=in_teacher and takes_id=in_takes;
	select "成功修改课程信息";
	else select "课程最大人数设置有误";
	end if;
	else select "该教室在该上课时段已被占用";
	end if;
	end if;
	drop table rooms;
END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for update_info
-- ----------------------------
DROP PROCEDURE IF EXISTS `update_info`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `update_info`(IN `in_tid` char(6),IN `in_tel` char(11),IN `in_email` varchar(30))
BEGIN
	update teachers
	set phone=in_tel, mail=in_email
	where teacher_id=in_tid;

END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for update_score
-- ----------------------------
DROP PROCEDURE IF EXISTS `update_score`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `update_score`(IN `in_sid` char(8),IN `in_tid` char(6),IN `in_cid` char(6),IN `in_score` float)
BEGIN
	declare in_takes char(8);
	declare student_exist tinyint;
	set in_takes=(select takes_id from takes where course_id=in_cid and teacher_id=in_tid);
	set student_exist=(select count(*) from student_takes where student_id=in_sid and takes_id=in_takes);
	if student_exist=0 then
	select "学生或课程选择有误";
	else
	if in_score<=100 then
	update student_takes
	set score=in_score
	where student_id=in_sid and takes_id=in_takes;
	select "成功录入学生成绩";
	else select "成绩有误";
	end if;
	end if;
END
;;
DELIMITER ;

-- ----------------------------
-- Function structure for addOne
-- ----------------------------
DROP FUNCTION IF EXISTS `addOne`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` FUNCTION `addOne`(id varchar(12),num smallint) RETURNS varchar(12) CHARSET utf8
    READS SQL DATA
BEGIN
  DECLARE str VARCHAR(12) DEFAULT '';
  set @val=CONVERT(id,SIGNED)+1;
  set str=LPAD(@val,num,'0');
  return str;
END
;;
DELIMITER ;

-- ----------------------------
-- Function structure for judgeChoose
-- ----------------------------
DROP FUNCTION IF EXISTS `judgeChoose`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` FUNCTION `judgeChoose`(s_id char(10),s_week tinyint,e_week tinyint,s_time tinyint,e_time tinyint,weekd tinyint) RETURNS tinyint(4)
    READS SQL DATA
BEGIN
declare s_week1 tinyint;
declare e_week1 tinyint;
declare s_time1 tinyint;
declare e_time1 tinyint;
declare weekd1 tinyint;
declare judge tinyint;
set s_week1=(select start_week from sections where section_id=s_id);
set e_week1=(select end_week from sections where section_id=s_id);
set s_time1=(select start_time from sections where section_id=s_id);
set e_time1=(select end_time from sections where section_id=s_id);
set weekd1=(select weekday from sections where section_id=s_id);
if  weekd1=weekd then
if s_week>e_week1 or e_week<s_week1 then
set judge=0;
else
if s_time>e_time1 or e_time<s_time1 then
set judge=0;
else
set judge=1;
end if;
end if;
else
set judge=0;
end if;
  return judge;
END
;;
DELIMITER ;
