#Make a connection to sqlite
import sqlite3

conn = sqlite3.connect("placement.db")
cursor = conn.cursor()



#Drop Tables if already exists
cursor.executescript("""
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Programming;
DROP TABLE IF EXISTS SoftSkills;
DROP TABLE IF EXISTS Placements;
""")

#This table stores basic information about students enrolled in the course.

cursor.execute("""
CREATE TABLE Students (
student_id INTEGER PRIMARY KEY,
name TEXT,
age INTEGER,
gender TEXT,
email TEXT,
phone INTEGER,
enrollment_year INTEGER,
course_batch TEXT,
city TEXT,
graduation_year INTEGER)
""")

#This table stores details of students' programming performance in the course.

cursor.execute("""
CREATE TABLE Programming (
programming_id  INTEGER PRIMARY KEY,
student_id INTEGER,
language TEXT,
problems_solved INTEGER,
assessments_completed INTEGER,
mini_projects INTEGER,
certifications_earned INTEGER,
latest_project_score INTEGER,
FOREIGN KEY (student_id) REFERENCES Students(student_id))
""")

cursor.execute("""
CREATE TABLE SoftSkills (
soft_skill_id  INTEGER PRIMARY KEY,
student_id INTEGER,
communication INTEGER,
teamwork INTEGER,
presentation INTEGER,
leadership INTEGER,
critical_thinking INTEGER,
interpersonal_skills INTEGER,
FOREIGN KEY (student_id) REFERENCES Students(student_id))
""")

#Create Placements Table
cursor.execute("""
CREATE TABLE Placements (
placement_id INTEGER PRIMARY KEY,
student_id INTEGER,
mock_interview_score INTEGER,
internships_completed INTEGER,
placement_status TEXT,
company_name TEXT,
placement_package TEXT,
interview_rounds_cleared INTEGER,
placement_date INTEGER,
FOREIGN KEY (student_id) REFERENCES Students(student_id))
""")

conn.commit()
conn.close()