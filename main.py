import random

import mysql.connector
import os



def adminLogin(cnx):
    while(True):
        
        # Create a cursor object
        admin_username = input("\n Enter your username: ")
        admin_password = input("\n Enter your password: ")
        cursor = cnx.cursor()
        args = ((admin_username), admin_password,None)

        # Call the SQL procedure
        result_args = cursor.callproc('validate_admin_login_credentials', [admin_username,admin_password,None])
        
        # Get the output parameter value
        valid_admin_login = result_args[2]
        
        if valid_admin_login:
            print("\n Login Successful \n")
            break
        else:
            print("\n Invalid username or password \n")

            print("\n Do you want to return to the previous page ? \n")
            selection = str(input("Y/N :"))
            if((selection == 'Y') or (selection == 'y')):
                logout = 1
                return logout
            elif((selection == 'N') or (selection == 'n')):
                continue
            elif((selection != 'Y') or (selection != 'y') or (selection != 'N') or (selection != 'n')):
                print("\n Invalid Input \n \n Re-enter credentials \n")
                continue
    
    if valid_admin_login == True:
        while(True):
            admin_operation = adminOperations(admin_username,cnx)
            if (admin_operation == 3):
                logout = 1
                return logout
                        
    # Close the cursor and database connection
    cursor.close()
    
def adminOperations(admin_username,cnx):
    
    while(True):
        cursor = cnx.cursor()

        cursor.execute("SELECT employer_id FROM employer WHERE user_name =%s", (admin_username,))
        emp_ids=[]
        for row in cursor:
            emp_ids.append(row)

        emp_id = emp_ids[0][0]


        print("\n Welcome " + admin_username + "! \n" )
        print("\n 1. Create Applications \n")
        print("\n 2. Update Application status \n")
        print("\n 3. Logout \n")
        admin_operation = int(input("Enter a number from the above menu : "))
        if(admin_operation == 1):
           flag = createJob(admin_username,cnx)
           if(flag == 1):
               continue
        
        elif(admin_operation == 2):
           updateJob(admin_username,cnx)
        
        elif(admin_operation == 3):
           return admin_operation

        elif((admin_operation!=1)or(admin_operation!=2)or(admin_operation!=3)):
            print("\n Invalid input \n \n Re enter number \n")
            continue
       
    cursor.commit()
    cursor.close()
    
def createJob(admin_username,cnx):
    job_lvls={"I":"Level 1 Salary Range $10-$15","II":"Level 2 Salary Range $12-$16","III":"level 3 Salary Range $15-$20","IV":"level 4 Salary Range $18-$25"
              ,"V":"Level 5 Salary Range $20-$30"}
    cursor = cnx.cursor()
    cursor.execute("SELECT employer_id FROM employer WHERE user_name =%s", (admin_username,))
    emp_ids = []
    for row in cursor:
        emp_ids.append(row)

    emp_id = emp_ids[0][0]

    cursor2 = cnx.cursor()
    cursor2.execute("SELECT team_id FROM employer WHERE user_name =%s", (admin_username,))
    team_ids=[]
    for row in cursor2:
        team_ids.append(row)
    team_id = team_ids[0][0]
    
    
    while(True):
       print("\n Enter Job Details: \n")
       job_id = int(input("\n Enter job id: "))
       result_args = cursor.callproc('check_job_exists', [job_id,None])
       result = result_args[1]
       if(result==True):
           print("\n Job Id already exists, enter a different job id \n")
           continue
       job_name = str(input("\n Enter job name: "))
       job_description = str(input("\n Enter the job description: "))
       
       while(True):
           job_lvl = str(input("\n Enter job level (I,II,III,IV or V): "))
           if (job_lvl == 'I'):
               job_level_desc = job_lvls["I"]
               break
           elif(job_lvl == 'II'):
               job_level_desc = job_lvls["II"]
               break
           elif(job_lvl == 'III'):
               job_level_desc = job_lvls["III"]
               break
           elif(job_lvl == 'IV'):
               job_level_desc = job_lvls["IV"]
               break
           elif(job_lvl == 'V'):
               job_level_desc = job_lvls["V"]
               break
           else:
               print("\n Job level invalid, select a level from I,II,III and IV \n")
       
       while(True):
           job_category = str(input("\n Enter whether the job is for graduate or undergraduate students : "))
           
           if((job_category=='Graduate') or (job_category == 'Undergraduate') or (job_category=='graduate') or (job_category=='undergraduate')):
               break
           else:
               print("\n Enter a valid input \n")
               
       
       job_status = "Open"
               
       location = str(input("\n Enter the location of the job: "))
       skills = str(input("\n Enter the skills required for the job: "))
       
       
       while(True):
           mode_of_work = str(input("\n Enter the mode: "))
           if((mode_of_work=='Online') or (mode_of_work == 'Offline') or (mode_of_work=='online') or (mode_of_work=='offline') or (mode_of_work == 'remote') or
              (mode_of_work == 'in person') or (mode_of_work == 'In person')):
               break
           else:
               print("\n Enter a valid input \n")
     
       created_by = emp_id
       salary = int(input("\n Enter the hourly salary of the job in $ : "))
       contract_period = int(input("\n Enter the contract period of this job in months : "))
       working_hrs = int(input("\n Enter the number of working hours per week in hrs : "))

       
       submit = int(input("\n Do you want to submit \n 1. Submit \n 2. Recreate job application \n 3. Return to Previous menu \n Selection:"))
       if submit == 1:
           cursor.callproc("create_job",[job_id,job_name,job_description,job_lvl,job_level_desc,job_category,job_status,location,skills,mode_of_work,created_by,salary,contract_period,working_hrs,team_id])
           print("\n Job successfully created \n")
           cnx.commit()
           selection = int(input("\n Press 1 to return to previous menu or any other number to create another application: "))
           if (selection == 1):
               return 1
       elif submit == 2:
           continue
       elif submit == 3:
           return 1

    cursor.close()
    cursor2.close()
    
def updateJob(admin_username,cnx):
    cursor = cnx.cursor()
    job_id =int(input("\n Enter the job_id to change status: "))

    # Check if job_id exists in db
    cursor.callproc("update_job_status",[job_id,"Closed"])
    cnx.commit()
    print("\n Job status has been successfully updated \n")
    cursor.close()
    

def login(cnx):
    while(True):
        # Create a cursor object
        username = input("\n Enter your username: ")
        password = input("\n Enter your password: ")
        cursor = cnx.cursor()


        result_args = cursor.callproc('validate_login_credentials', [username,password,None])

        # Get the output parameter value
        valid_login = result_args[2]

        # Check if the login credentials are valid
        if valid_login:
            print("\n Login successful! \n")
            break
        else:
            print("\n Invalid username or password. \n")
            print("\n Do you want to return to the previous page ? \n")
            selection = str(input("Y/N :"))
            if ((selection == 'Y') or (selection == 'y')):
                logout = 1
                return logout

    if valid_login == True:
        while(True):
            student_operation = first_page(username,cnx)
            if (student_operation == 3):
                logout = 1
                return logout
    # Close the cursor
    cursor.close()
    
def first_page(username,cnx):
    while(True):
        cursor = cnx.cursor()
        cursor.execute("SELECT nuid FROM employmentseekers WHERE user_name =%s", (username,))
        nuids = []
        for row in cursor:
            nuids.append(row)
        nuid=nuids[0][0]
        print("\n Welcome " + username + "!")
        print("\n 1. View Listings")
        print("\n 2. Withdraw your Applications")
        print("\n 3. logout")
        application_option = int(input("\n Enter an option: "))
        if application_option == 1:
            flag = listings(cnx)
            if (flag == 1):
                continue
        elif (application_option == 2):
            flag = viewing_applications(nuid,cnx)
            if (flag == 1):
                continue
        elif (application_option == 3):
            return application_option
        elif ((application_option!=1)or(application_option!=2)or(application_option!=3)):
            print("\n Invalid Input \n \n Re-enter option: ")
            continue

    cursor.commit()
    cursor.close



def viewing_applications(nuid,cnx):
    while(True):
        cursor = cnx.cursor()
        cursor2 = cnx.cursor()
        cursor.callproc("view_applications",(nuid,))
        for result in cursor.stored_results():
            app = result.fetchall()
        print("\n Active Applications \n")
        print("\n Job_id, NUID, Application id, School, Degree, GPA, Company, Post, Months of Exp, Role Description, Project title, Project Description")
        for apps in app:
            print("\n")
            print(apps)
            print("\n")
        withdraw_option = int(input("\n 1. Withdraw any applications\n 2. Go Back \n Selection: "))
        if (withdraw_option == 1):
            args_2 = int(input("\n Enter the application ID to Withdraw : "))
            cursor2.callproc('delete_application',[args_2])
            cnx.commit()
            cursor2.close()
            print("\n Application Withdrawn successsfully \n")
        elif (withdraw_option == 2):
            flag = 1
            return flag
        elif((withdraw_option!=1) or (withdraw_option!=2)):
            print("\n Invalid input \n")
            continue
    cursor.close()

def listings(cnx):
    while(True):
        # create a cursor object
        cursor = cnx.cursor()

        # Display Job ID and Job Description
        display_query = "SELECT job_id, job_name FROM job_posting"
        cursor.execute(display_query)
        rows = []
        for row in cursor:
            rows.append(row)
        for r in rows:
            print(r)

        # Prompt user to enter a job ID
        job_id = int(input("\n Enter a job ID to view details OR Enter 0 to go back: "))
        if job_id == 0:
            flag = 1
            return flag
        else :
            flag2 = job_details(job_id,cnx)
            if flag2 == 1:
                continue

        # Close the cursor and database connection
        cursor.close()
    
def job_details(job_id,cnx):
    # create cursor object
    cursor = cnx.cursor()

    # Execute SELECT query to retrieve job details for the entered ID
    select_query = ("SELECT * FROM job_posting WHERE job_id = %s",(job_id,))
    data = (job_id,)
    cursor.execute("SELECT * FROM job_posting WHERE job_id = %s",(job_id,))
    result = cursor.fetchone()

    # Display job ID and job description
    if result:
        print("\n Job ID:", result[0])
        print("\n Job Name:", result[1])
        print("\n Job Description:", result[2])
        print("\n Job Level:", result[3])
        print("\n Job Level Description: ", result[4])
        print("\n Job Category", result[5])
        print("\n Job Status:", result[6])
        print("\n Job Location:", result[7])
        print("\n Job Skills:", result[8])
        print("\n Mode of Work", result[9])
        print("\n Posted by", result[10])
        print("\n Salary", result[11])
        print("\n Contract Period in months: ", result[12])
        print("\n Working hours", result[13])
        print("\n Contact team_id:", result[14])
        print("\n ")
        option = int(input("\n Would you like to \n 1.Apply \n 2.Go Back \n Option:"))
        if option == 1:
            flag1 = application(result[0],cnx)
            if (flag1 == 1):
                return flag1
        elif option == 2:
            flag2 = 1
            return flag2

    else:
        print("\n No job found with the entered ID. \n")
        flag2 = 1
        return flag2

    # Close the cursor and database connection
    cursor.close() 

def application(job_id,cnx):
    cursor = cnx.cursor()
    username = str(input("\n Enter your username : "))
    cursor.execute("SELECT nuid from employmentseekers WHERE user_name = %s", (username,))
    temp_ids = []
    for row in cursor:
        temp_ids.append(row)
    nuid = temp_ids[0][0]
    #cursor2 = cnx.cursor()
    #result_args = cursor2.callproc("job_statuses", (job_id,None))
    #print(cursor2.fetchall())
    while (True):
        print("\n Enter your education details \n")
        application_id = random.randint(0, 1000)
        school = str(input("\n School Name : "))
        degree = str(input("\n Degree :"))
        gpa = str(input("\n GPA : "))
        print("\n Enter your Work experience")
        company = str(input("\n Company Name : "))
        role = str(input("\n Role : "))
        months_of_exp = int(input("\n Experience in Months(in numbers) : "))
        role_desription = str(input("\n Give short description of your role : "))
        print("\n Enter your projects")
        project_title = str(input("\n title of project : "))
        project_description = str(input("\n Description of Project : "))

        print("\n Review your responses : ")
        print("\n Application ID:", application_id)
        print("\n Job ID:", job_id)
        print("\n NUID:", nuid)
        print("\n School:", school)
        print("\n Degree:", degree)
        print("\n GPA: ", gpa)
        print("\n")
        print("\n Company: ", company)
        print("\n Role:", role)
        print("\n Months of Experience:", months_of_exp)
        print("\n Role Description: ", role_desription)
        print("\n")
        print("\n Projects")
        print("\n Project title", project_title)
        print("\n Project description", project_description)

        submit = int(input("\n Do you want to submit \n 1. Submit \n 2. Go Back \n Option:"))
        if submit == 1:
            cursor2 = cnx.cursor()
            cursor2.callproc("apply_job",
                             [job_id, nuid, application_id, school, degree, gpa, company, role, months_of_exp,
                              role_desription, project_title, project_description])
            cnx.commit()
            print("\n Submitted successfully.\n")
            selection = int(input("\n Press any key to return to previous menu : "))
            if (selection == 1):
                return 1
        elif (submit == 2):
            return 1
        elif ((submit != 1) or (submit != 2)):
            print("\n Invalid input \n \n Re apply \n")
            continue

def main():
    username = input("\n Enter your MySQL username: ")
    password = input("\n Enter your MySQL password: ")
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host='localhost',
                                      database='oncampus')
        print("Connection successful! \n")


        while(True):
                print ("\n Hello User! \n")
                print("\n Press 1 for student login \n")
                print("\n Press 2 for admin login \n")
                print("\n Press 3 for exit \n")
                login_selection = int(input("\n Enter a number: "))
                if (login_selection == 1):
                    while(True):
                      logout = login(cnx)
                      if (logout == 1):
                          print("\n Thank you \n")
                          break
                elif(login_selection == 2):
                    while(True):
                        logout = adminLogin(cnx)
                        if (logout == 1):
                            print("\n Thank you \n")
                            break
                elif(login_selection == 3):
                    print("\n Thank you \n")
                    break
                elif((login_selection!=1) or (login_selection!=2) or (login_selection!=3)):
                    print("\n Invalid Input \n \n Re-enter number")
                    continue

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
    
if __name__ == "__main__":
    main()
   
    
