use student;
CREATE TABLE info (
  department VARCHAR(30) DEFAULT NULL,
  student_id VARCHAR(15) DEFAULT NULL,
  identity VARCHAR(10) DEFAULT NULL,
  last_used DATETIME DEFAULT NULL,
  name VARCHAR(70) DEFAULT NULL,
  line_id VARCHAR(50) NOT NULL,
  mode VARCHAR(50) DEFAULT NULL,
  nationality VARCHAR(10) DEFAULT NULL,
  PRIMARY KEY (line_id)
);



