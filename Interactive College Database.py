import sqlite3
import random

#initialize sqlite
conn = sqlite3.connect('student.db')
cursor = conn.cursor()

#function to create the 3 tables
def createTables():
    studentTable ="CREATE TABLE STUDENT(UID VARCHAR(9) PRIMARY KEY NOT NULL, FIRST_NAME VARCHAR(255) NOT NULL, LAST_NAME VARCHAR(255) NOT NULL, MAJOR VARCHAR(255), CLASS INT, TYPE VARCHAR(255) NOT NULL);"
    cursor.execute(studentTable)

    studentClassTable ="CREATE TABLE STUDENT_COURSES(CRN INT NOT NULL, UID VARCHAR(9) NOT NULL, GRADE VARCHAR(255), CONSTRAINT comp_pk PRIMARY KEY(CRN, UID));" #composite PK
    cursor.execute(studentClassTable)

    ClassTable ="CREATE TABLE COURSES(CRN INT PRIMARY KEY NOT NULL, COURSEID VARCHAR(8) NOT NULL, TITLE VARCHAR(255) NOT NULL, TERM VARCHAR(255) NOT NULL, LEVEL VARCHAR(2) NOT NULL, CREDIT_HOURS INT NOT NULL, CAMPUS VARCHAR(255) NOT NULL);"
    cursor.execute(ClassTable)

    print("Tables STUDENT, STUDENT_COURSES, and COURSES were successfully created.\n")


#function to INSERT records into STUDENT table
def addStudent(uid, fname, lname, major, grade, type):
    try:
        #attempt to add the student to the DB
        cursor.execute("INSERT INTO STUDENT VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(uid, fname, lname, major, grade, type))
        conn.commit()
        print(uid + "'s data was successfully inserted into the STUDENT table. \n") #display success message

    except sqlite3.Error as error: #catch errors
        print(uid + "'s data was not inserted into the STUDENT table: ", error) #display error message


#function to INSERT records into STUDENT_COURSES table
def addStudentClass(crn, uid, grade):
    try:
        #attempt to add the class to the DB
        cursor.execute("INSERT INTO STUDENT_COURSES VALUES ('{}', '{}', '{}')".format(crn, uid, grade))
        conn.commit()
        print(uid +"'s class " + str(crn) + " was successfully added to the STUDENT_COURSES table.\n") #display success message

    except sqlite3.Error as error: #catch errors
        print(uid +"'s class " + str(crn) + " was not added to the STUDENT_COURSES table: ", error) #display error message


#function to INSERT records into COURSES table
def addClass(crn, courseID, title, term, level, credit_hours, campus):
    try:
        #attempt to add the class to the DB
        cursor.execute("INSERT INTO COURSES VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(crn, courseID, title, term, level, credit_hours, campus))
        conn.commit()
        print(courseID + "'s data was successfully inserted into the COURSES table. \n") #display success message

    except sqlite3.Error as error: #catch errors
        print(courseID + "'s data was not inserted into the COURSES table: ", error) #display error message


#function to print all records in a given table (for debugging/checking)
def printTable(table):
    try:
        #print the table
        print("\n" + table + ":")
        data = cursor.execute("SELECT * FROM " + table) #select all the rows in the given table
        for row in data: #iterate over them all
            print(row) #print row

    except sqlite3.Error as error: #catch errors for selection
        print("Table '"+ table +"' does not exist.\n") #display error message

#inserts a new student into the DB
def insertStudent():
    majors = ['Computer Science', 'Computer Engineering'] #array of valid majors

    print("Please enter the following information.")
    print("First Name: ", end=" ") #get first name
    fname = input()
    print("Last Name: ", end=" ") #get last name
    lname = input()

    while(True): #continue looping until a major is givin (valid must be in majors array)
        print("Major: ", end=" ") #get major

        maj = input()
        if((maj in majors) == False): #if the major is invalid
            print("Invalid Major, try again.\n")
            continue
        break

    while(True): #continue looping until a valid graduation year is givin (valid cant be past year)
        print("Expected Graduation Year: ", end=" ") #get grad year
        try:
            gyear = int(input())
            if(gyear < 2022): #if grad year is in the past, reprompt user
                print("Invalid Graduation Year, try again.\n")
                continue
        except:
                print("Invalid graduation year, try again.\n") #if grad year is not a valid int display error message
                continue #reprompt user
        break
    
    while(True): #continue looping until a valid student type is given (valid = GR or UG)
        print("Student Type (GR or UG): ", end=" ")
        type = input()

        if(type == 'GR' or type == 'UG'): #if UG or GR is given then break
            break
        
        print("Invalid student type, try again.\n") #else, invalid input try again
        continue
    
    stringuid = getUID() #get a new unused UID from the getUID function

    addStudent(stringuid, fname, lname, maj, gyear, type)
    return

#returns true if used UID, false otherwise
def checkUID(uid):
    uids = cursor.execute("SELECT UID FROM STUDENT") #get all the currently used UID's

    for rows in uids: #search through all UID's to see if the current one is used already
        if uid in rows:
            return True #if used, return true
    return False #if valid/not used return false

#function used for getting a random valid UID for a new student
def getUID():
    #loop until an unused/valid uid is found
    while(True):
        newuid = random.randint(10000000, 99999999) #get a random uid value
        stringuid = 'U' + str(newuid) #add a U to the begging of the randomly generated int

        if(checkUID(stringuid)): #check if the random uid is used
            continue #if used, get a new one
        else:
            return stringuid #else, it is not used so return it

#returns true if CRN exists, false otherwise
def checkStudentCRN(crn, uid):
    crns = cursor.execute("SELECT CRN FROM STUDENT_COURSES WHERE UID='" + uid + "'") #get all CRN's currently in DB
    crns = cursor.fetchall()

    for rows in crns: #check every CRN to see if it is already in use
        if crn in rows:
            return True #if it is currently being used return true
    return False #CRN is free so return false

#removes an existing class from an existing student
def removeStudentClass():
    while(True): #continues looping until valid UID (existing student) is given
        print("Please enter the following information.")
        print("Enter UID: ", end=" ") #get UID
        userUID = input()

        if(checkUID(userUID) == False): #check if UID exists
            print("UID not found. Please enter a valid UID.")
            continue #if not continue to reprompt user
        
        print("Student found!\n") #else UID exists and student was found
        
        while(True): #continue looping until valid CRN (existing class) is given
            try:
                print("Please Enter the CRN: ", end=" ") #get CRN to remove from user
                userCRN = input()
                crn = int(userCRN)
            except:
                print("Enter a valid CRN. Please try again.\n") #if an invalid CRN is given (like a string) display error message
                continue #continue to reprompt user

            if(checkStudentCRN(crn, userUID)): #check if student is assigned to that CRN
                try:
                    cursor.execute("DELETE FROM STUDENT_COURSES WHERE CRN='" + str(crn) + "'" "AND UID='" +userUID+"'") #if so, delete the class
                    conn.commit()

                    cursor.execute("SELECT TITLE FROM COURSES WHERE CRN='" + str(crn) +"'") #get the class that was removed
                    title = cursor.fetchone()
                    print("'" +title[0] + "' removed from "+ userUID) #print success message
                    print()
                    return
                except:
                    print("Course removal failed. Try again\n")
                    return

            else: #the entered UID (student) is not registered for the given CRN
                print(userUID + " is not registered for that class.\n") #display error message
                continue #reprompt user

#returns true if crn exists in courses table, false otherwise
def checkClassCRN(crn):
    crns = cursor.execute("SELECT CRN FROM COURSES") #select all the current crns in the courses DB
    crns = cursor.fetchall()
    for rows in crns: #check every CRN to see if the given one exists
        if crn in rows:
            return True #if it exists, return true
    return False #if it doesnt exists return false
    
#assigns an existing class to an existing student
def assignStudentClass():
    valid_grades = ['A', 'B', 'C', 'D', 'F', 'PROG', 'REG'] #array of valid grade input
    
    while(True): #continues looping until valid UID is given of an existing student
        print("Please enter the following information.")
        print("Enter UID: ", end=" ") #get UID
        userUID = input()

        if(checkUID(userUID) == False): #check if UID exists
            print("UID not found. Please enter a valid UID. \n") #if not, display error message
            continue #reprompt user
        
        print("Student found!\n") #else student is found

        while(True): #loop until valid CRN is given of an existing class
            try:
                print("Please Enter the CRN: ", end=" ") #get CRN
                userCRN = input()
                crn = int(userCRN)
            except:
                print("Enter a valid CRN. Please try again.\n") #CRN doesnt exist error message
                continue

            #check if the given crn exists
            if(checkClassCRN(crn)): #if CRN exists get the grade from user
                
                while(True): #loop until a valid grade is given ('A', 'B', 'C', 'D', 'F', 'PROG', 'REG')
                    print("Please enter the student's grade for this course ('A', 'B', 'C', 'D', 'F', 'PROG', 'REG'): ", end=" ")
                    userGrade = input()

                    if((userGrade in valid_grades) == False): #if given value isnt in the valid_grades array, reprompt user
                        print("Invalid grade. Please try again.") #display error message
                        print("Valid Grades are 'A', 'B', 'C', 'D', 'F', 'PROG', 'REG'.\n")
                        continue #reprompt user
                    else:
                        break #else, valid grade given so break

                try:
                    cursor.execute("INSERT INTO STUDENT_COURSES VALUES ('{}', '{}', '{}')".format(crn, userUID, userGrade)) #execute the insertion of the given info into the DB
                    conn.commit()
                except:
                    print(userUID + " is already registered for that class!\n") #display error message if issue with DB insertion
                    return

                cursor.execute("SELECT TITLE FROM COURSES WHERE CRN='" + str(crn) +"'") #execute select statement to retreive the added class
                title = cursor.fetchone()
                print("'" +title[0] + "' added to "+ userUID) #display success message
                print()
                return

            else:
                print(str(crn) + " is not an existing class! Please try again.\n") #print error message
                continue #reprompt user


############################################# MAIN #############################################

# ################################ FOR DB CREATION & Initialization ################################
# print("Initializing Database...\n")

# try:
#     print("Creating Tables...")
#     createTables() #try to create the new tables
# except sqlite3.Error as error:
#     print("Tables already created!: ", error) #if the tables already exist, print a message and continue
#     print()

# #add students
# print("Adding Students...")
# addStudent('U00804617', 'Ashton', 'Williams', 'Computer Science', 2022, 'GR')
# addStudent('U05617503', 'John', 'Smith', 'Computer Engineering', 2026, 'UG')
# print()

# #add classes
# print("Adding Classes...")

# #[crn, courseID, title, term, level, credit_hours, campus]
# classesArray = [[1, "CHM1210", 'General Chemistry I', 'F2018', 'UG', 3, 'Dayton'], [2, "CHM1210L", 'General Chemistry Lab I', 'F2018', 'UG', 2, 'Dayton'], [3, 'CS1180', 'Computer Science I', 'S2019', 'UG', 4, 'Dayton'], 
# [4, 'CS2200', 'Discrete Struc Algorithm', 'S2019', 'UG', 4, 'Dayton'], [5, 'CS1181', 'Computer Science II', 'F2019', 'UG', 4, 'Dayton'], [6, 'MTH2300', 'Calculus I', 'F2019', 'UG', 4, 'Dayton'],
# [7, 'MTH2310', 'Calculus II', 'S2020', 'UG', 4, 'Dayton'], [8, 'CEG3310', 'Computer Organization', 'S2020', 'UG', 4, 'Dayton'], [9, 'PHY2400', 'General Physics I', 'S2020', 'UG', 4, 'Dayton'], 
# [10, 'PHY2400L', 'General Physics I Lab', 'S2020', 'UG', 1, 'Dayton'], [11, 'CS3900', 'Game Programming', 'R2020', 'UG', 3, 'Dayton'], [12, 'CS3100', 'Data Struc & Algorithms', 'F2020', 'UG', 3, 'Dayton'], 
# [13, 'MTH2530', 'Elementary Linear Alg', 'F2020', 'UG', 3, 'Dayton'], [14, 'CEG4350', 'OS Internals and Design', 'S2021', 'UG', 3, 'Dayton'], [15, 'CEG4110', 'Intro to Software EGR', 'F2021', 'UG', 3, 'Dayton'], 
# [16, 'CEG4980', 'Team Projects I', 'F2021', 'UG', 3, 'Dayton'], [17, 'CEG4981', 'Team Projects II', 'S2022', 'UG', 3, 'Dayton'], 
# [18, 'CS3180', 'Comparative Languages', 'S2022', 'UG', 3, 'Dayton'], [19, 'CS7700', 'Adv. Database Systems', 'R2022', 'GR', 3, 'Dayton'], [20, 'CS7920', 'Independent Study in CS', 'R2022', 'GR', 3, 'Dayton'], 
# [21, 'CS7950', 'MSCS Thesis Research', 'R2022', 'GR', 3, 'Dayton'], [22, 'CS7100', 'Adv. Prog. Languages', 'F2022', 'GR', 3, 'Dayton'], [23, 'MTH2300', 'Calculus I', 'F2022', 'UG', 4, 'Dayton'], 
# [24, 'PHY2400', 'General Physics I', 'F2022', 'UG', 4, 'Dayton'], [25, 'PHY2400L', 'General Physics I Lab', 'F2022', 'UG', 1, 'Dayton'], [26, 'CS1180', 'Computer Science I', 'F2022', 'UG', 4, 'Dayton']]

# #add the classes to the Classes table
# for course in classesArray:
#     addClass(course[0], course[1], course[2], course[3], course[4], course[5], course[6])
# print()

# #assign classes
# print("Assigning classes to students...")
# #addStudentClasses(uid, courseID, term, grade)

# #ashton's classes
# ashClasses = [[1, 'U00889239', 'A'], [2, 'U00889239', 'A'], [3, 'U00889239', 'B'], 
# [4, 'U00889239', 'A'], [5, 'U00889239', 'A'], [6, 'U00889239', 'B'],
# [7, 'U00889239', 'A'], [8, 'U00889239', 'A'], [9, 'U00889239', 'A'], [10, 'U00889239', 'A'],
# [11, 'U00889239', 'A'], [12, 'U00889239', 'A'], [13, 'U00889239', 'A'],
# [14, 'U00889239', 'A'], [15, 'U00889239', 'A'], [16, 'U00889239', 'A'], 
# [17, 'U00889239', 'A'], [18, 'U00889239', 'A'], 
# [19, 'U00889239', 'PROG'], [20, 'U00889239', 'PROG'], [21, 'U00889239', 'PROG'], 
# [22, 'U00889239', 'REG']]

# for course in ashClasses:
#     addStudentClass(course[0], course[1], course[2])

# #John's classes
# addStudentClass(23, 'U05617503', 'REG')
# addStudentClass(24, 'U05617503', 'REG')
# addStudentClass(25, 'U05617503', 'REG')
# addStudentClass(26, 'U05617503', 'REG')

# print()
# print("Database created!\n")


################################ FOR DB TRANSACTIONS ################################

#loops until user selects quit
while(True): #menu that loops until 4 is entered
    print("What would you like to do? (Enter 1, 2, 3, or 4)")
    print("1: Add a Student.")
    print("2: Assign an existing class to a student.")
    print("3: Remove an existing class from a student.")
    print("4: Quit\n")

    userInput = input()
    print()

    #add a student
    if userInput == '1': 
        insertStudent() #call function to insert student
        
    #assign class to a student
    elif userInput == '2': 
        assignStudentClass() #call function to assigne a new student class

    #remove student class
    elif userInput == '3': 
        removeStudentClass() #call function to remove a student class

    #break the loop and quit
    elif userInput == '4': 
        print("Quitting...")
        break #break out of the loop and quit

    #invalid input
    else:
        print(userInput + " is not a valid input. Try Again.\n") #display error message
        continue #restart loop/reprompt the user


# printTable("STUDENT")
# printTable("STUDENT_COURSES")
# printTable("COURSES")
conn.close()
