import streamlit as st
import sqlite3
from faker import Faker
import random
import pandas as pd
import time as t

st.title("Placement Eligibility Application")
st.sidebar.image("assets/guvi.PNG")

# Spinner
with st.spinner("Just Wait"):
    t.sleep(2)

#Initialize Faker and database
fake = Faker()
conn = sqlite3.connect("placement.db")

def main():
    choice = st.sidebar.selectbox("Select Students", ["All Students", "Top Students in All Languages", "Eligible Students","Minimum Programmings Solved","Batch Average Score","Average Batch Score","Placement Ready Students","Placement Not Ready Students","Latest Project Score", "Highest Package"])

    if choice == "All Students":
        st.title("All Students")
        all_data = get_all_students_data()
        st.dataframe(all_data,hide_index=True)
        st.download_button("Download as CSV", all_data.to_csv(index=False),"All Students.csv","text/csv")
    elif choice == "Top Students in All Languages":
        st.title("Top Students in All Languages")
        number_of_students = st.sidebar.text_input("Number of Top Students in All Languages",value=5)
        type(number_of_students)
        top_data = get_top_students_data(number_of_students)
        st.dataframe(top_data,hide_index=True)
        st.download_button("Download as CSV", top_data.to_csv(index=False), "Top Students in All Languages.csv", "text/csv")
    elif choice == "Eligible Students":
        st.title("Eligible Students")
        problem_solved = st.sidebar.selectbox("Problem Solved",[">=25",">=50",">=100",">=150",">=200",">=250"])
        soft_skills = st.sidebar.selectbox("Soft Skills Solved", [">=25",">=50",">=100",">=150",">=200",">=250"])
        problem_solved_val = int(problem_solved.replace(">=",""))
        soft_skills_val = int(soft_skills.replace(">=",""))
        ps_data = get_soft_skills_problem_solved_data(problem_solved_val,soft_skills_val)
        st.dataframe(ps_data,hide_index=True)
        st.download_button("Download as CSV", ps_data.to_csv(index=False), "Eligible Students.csv", "text/csv")
    elif choice == "Minimum Programmings Solved":
        st.title("Minimum Programmings Solved")
        min_data = get_min_programming_solved() 
        st.dataframe(min_data,hide_index=True)
        st.download_button("Download as CSV", min_data.to_csv(index=False), "Minimum Programmings.csv", "text/csv")
    elif choice == "Batch Average Score":
        st.title("Batch Average Score")
        avg_data = get_avg_batch_data()
        st.dataframe(avg_data, hide_index=True)
        st.download_button("Download as CSV", avg_data.to_csv(index=False), "Batch Average Score.csv", "text/csv")
    elif choice == "Average Batch Score":
        st.title("Average Batch Score")
        batch_name = st.sidebar.text_input("Enter Batch Name",value="B1")
        batch_data = get_batch_avg_data(batch_name)
        st.dataframe(batch_data, hide_index=True)
        st.download_button("Download as CSV", batch_data.to_csv(index=False), "Average Batch Score.csv", "text/csv")
    elif choice == "Placement Ready Students":
        st.title("Placement Ready Students")
        placement_ready_data = placement_ready_students_with_package()
        st.dataframe(placement_ready_data, hide_index=True)
        st.download_button("Download as CSV", placement_ready_data.to_csv(index=False), "Placement Ready Students.csv", "text/csv")
    elif choice == "Placement Not Ready Students":
        st.title("Placement Not Ready Students")
        placement_not_ready_data = placement_not_ready_students_with_package()
        st.dataframe(placement_not_ready_data, hide_index=True)
        st.download_button("Download as CSV", placement_not_ready_data.to_csv(index=False), "Placement Not Ready Students.csv", "text/csv")
    elif choice == "Latest Project Score":
        st.title("Latest Project Score")
        choice = st.sidebar.selectbox("Select Language", ["Python", "Data Science", "Java", "AI/ML"])
        latest_project_data = get_latest_project_score(choice)
        st.dataframe(latest_project_data, hide_index=True)
        st.download_button("Download as CSV", latest_project_data.to_csv(index=False), "Latest Project Score.csv", "text/csv")
    else:
        st.title("Highest Package")
        package_data = get_highest_package()
        st.dataframe(package_data, hide_index=True)
        st.download_button("Download as CSV", package_data.to_csv(index=False), "Latest Project Score.csv", "text/csv")
    st.markdown("---", unsafe_allow_html=True)

def get_all_students_data():
    query = """SELECT s.student_id,s.name,s.age,s.gender,s.email,s.phone,s.enrollment_year,s.course_batch,s.graduation_year,s.city FROM Students s"""
    return pd.read_sql(query, con=sqlite3.connect("placement.db"))

def get_top_students_data(number_of_students):
    number_of_students = int(number_of_students)
    query = """ SELECT s.student_id,s.name,p.problems_solved, p.assessments_completed, p.mini_projects, p.certifications_earned FROM Students s JOIN Programming p ON s.student_id = p.student_id ORDER BY p.problems_solved DESC LIMIT ? """
    return pd.read_sql(query, con=sqlite3.connect("placement.db"),params=(number_of_students,))

def get_soft_skills_problem_solved_data(problem_solved_val, soft_skills_val):
    query = """
                    SELECT s.student_id,s.name,p.problems_solved, ss.communication from Students s JOIN Programming p ON s.student_id = p.student_id join SoftSkills ss ON ss.student_id = s.student_id WHERE p.problems_solved >= ? and ss.communication >= ?
                    """
    return pd.read_sql(query, con=sqlite3.connect("placement.db"),params=(problem_solved_val, soft_skills_val))

def get_min_programming_solved():
    query = """ SELECT s.student_id,s.name, p.problems_solved  
    from Students s JOIN Programming p ON s.student_id = p.student_id ORDER BY p.problems_solved ASC LIMIT 5"""
    return pd.read_sql(query, con=sqlite3.connect("placement.db"))

def get_avg_batch_data():
    query = """ SELECT s.course_batch, AVG(p.problems_solved + p.assessments_completed + p.mini_projects + p.certifications_earned + p.latest_project_score) AS avg_score FROM Students s JOIN Programming p ON s.student_id = p.student_id GROUP BY s.course_batch ORDER BY avg_score"""
    return pd.read_sql(query,con=sqlite3.connect("placement.db"))

def get_batch_avg_data(batch_name):
    query = """ SELECT s.course_batch, AVG(p.problems_solved) AS Problems_Solved, AVG(p.assessments_completed) AS Assessments_Completed, AVG(p.mini_projects) AS Mini_Projects,
    AVG(p.certifications_earned) AS Certifications_Earned,AVG(p.latest_project_score) AS Latest_Project_Score FROM students s JOIN Programming p ON s.student_id = p.student_id where s.course_batch = ?"""
    return pd.read_sql(query,con=sqlite3.connect("placement.db"),params=(batch_name,))

def placement_ready_students_with_package():
    query = """ SELECT s.student_id, s.name, p.placement_package, p.placement_status from Students s JOIN Placements p ON s.student_id = p.student_id where p.placement_status = 'Ready' """
    return pd.read_sql(query,con=sqlite3.connect("placement.db"))

def placement_not_ready_students_with_package():
    query = """ SELECT s.student_id, s.name, p.placement_package, p.placement_status from Students s JOIN Placements p ON s.student_id = p.student_id where p.placement_status = 'Not Ready' """
    return pd.read_sql(query,con=sqlite3.connect("placement.db"))

def get_latest_project_score(choice):
    query = """ SELECT s.student_id, s.name, p.language, p.latest_project_score from Students s JOIN Programming p ON s.student_id = p.student_id where p.language = ? """
    return pd.read_sql(query, con=sqlite3.connect("placement.db"), params=(choice,))

def get_highest_package():
    query = """
    SELECT * FROM (SELECT s.student_id, s.name, s.gender, p.company_name, p.placement_package FROM Students s
    JOIN Placements p ON s.student_id = p.student_id WHERE s.gender = 'Male' ORDER BY CAST(p.placement_package AS INTEGER) DESC LIMIT 1)
    UNION ALL
    SELECT * FROM (SELECT s.student_id, s.name, s.gender, p.company_name, p.placement_package FROM Students s JOIN Placements p ON 
    s.student_id = p.student_id WHERE s.gender = 'Female' ORDER BY CAST(p.placement_package AS INTEGER) DESC LIMIT 1)
    UNION ALL
    SELECT * FROM (SELECT s.student_id, s.name, s.gender, p.company_name, p.placement_package FROM Students s
    JOIN Placements p ON s.student_id = p.student_id WHERE s.gender = 'Others' ORDER BY CAST(p.placement_package AS INTEGER) DESC LIMIT 1)
    """
    return pd.read_sql(query, con=sqlite3.connect("placement.db"))

#Generate Fake Student Data
def generate_students(num_records=50):
    data = []
    for i in range(num_records):
        record = {
        "student_id" : random.randint(1,50),
        "name" : fake.name(),
        "age" : random.randint(18, 25),
        "gender" : random.choice(["Male", "Female", "Others"]),
        "email" : fake.email(),
        "phone" : fake.phone_number(),
        "enrollment_year" : random.randint(2020, 2025),
        "course_batch" : "B" + str(random.randint(1, 20)),
        "city" : fake.city(),
        "graduation_year" : random.randint(2015, 2020)
        }
        data.append(record)
    return pd.DataFrame(data)



#Generate Fake Programming Performance Data
def generate_programming_performance(num_records=50):
    data = []
    for i in range(num_records):
        record = {
        "language" : random.choice(["Python", "Data Science", "Java", "AI/ML"]),
        "problems_solved" : random.randint(0, 250),
        "assessments_completed" : random.randint(0, 10),
        "mini_projects" : random.randint(0, 10),
        "certifications_earned" : random.randint(0, 10),
        "latest_project_score" : random.randint(0, 10),
        "student_id": random.randint(1, 50)
        }
        data.append(record)
    return pd.DataFrame(data)


#Generate Fake Soft Skills Data
def generate_soft_skills(num_records=50):
    data = []
    for i in range(num_records):
        records = {
        "communication" : random.randint(1, 100),
        "teamwork" : random.randint(1, 100),
        "presentation" : random.randint(1, 100),
        "leadership" : random.randint(1, 100),
        "critical_thinking" : random.randint(1, 100),
        "interpersonal_skills" : random.randint(0, 100),
        "student_id": random.randint(1, 50)
        }
        data.append(records)
    return pd.DataFrame(data)


#Generate Fake Placements Data
def generate_placements(num_records=50):
    data = []
    for i in range(num_records):
        record = {
        "mock_interview_score" : random.randint(1,100),
        "internships_completed" : random.randint(1,100),
        "placement_status" : random.choice(["Ready","Not Ready"]),
        "company_name" : fake.name(),
        "placement_package" : str(random.randint(1,10)) + " LPA",
        "interview_rounds_cleared" : random.randint(1, 10),
        "placement_date" : fake.date(),
        "student_id": random.randint(1, 50)
        }
        data.append(record)
    return pd.DataFrame(data)



#Calling methods
students_df = generate_students()
programming_df = generate_programming_performance()
soft_skills_df = generate_soft_skills()
placements_df = generate_placements()



#st.dataframe(placements_df)

students_df.to_sql("Students", conn, if_exists="replace", index=True)
programming_df.to_sql("Programming", conn, if_exists="replace", index=True)
soft_skills_df.to_sql("SoftSkills", conn, if_exists="replace", index=True)
placements_df.to_sql("Placements", conn, if_exists="replace", index=True)

main()




