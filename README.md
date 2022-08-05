# Interactive-College-Database
An interactive college database I made in python for a class in college.

The database is for a student to register for classes. The user can interact with the database using the 3 options below:

1.	Add a student:
  a.	Functionality - Allows the user to add a new student to the DB.
  b.	Input - All the information for the student shown above (First_Name, Last_Name, etc.). An available UID will be provided for them.
  c.	Output – The new student will be added to the STUDENT table with a message upon successful completion. If the student already exists or insertion fails, display a message.

2.	Assign an existing class to a student (register):
  a.	Functionality - Allows the user to add an existing class to an existing student. 
  b.	Input - The UID of the existing student, the existing class CRN if the student was found, and a valid grade if the CRN was found (valid grade = A, B, C, D, F, REG, PROG). 
  c.	Output - The new class will be added to the STUDENT_COURSES table with a message notifying the user. If the student or class is not found, a message will display.

3.	Remove an existing class from a student (withdrawal from a class):
  a.	Functionality - Allows the user to remove an existing class from an existing student. 
  b.	Input - The UID of the existing student, then input the existing class’s CRN to remove.
  c.	Output - If the student is found and registered for that class, remove the class from the STUDENT_COURSES table with a message if completed. If failed, display a message.



Student DB Project Schema:
![CS 7700 Project Schema](https://user-images.githubusercontent.com/98552891/182987221-6a68d6ee-e98b-47ed-996e-83fe959198bc.jpg)


Student DB Relational Schema:
![CS 7700 Project Relational Schema](https://user-images.githubusercontent.com/98552891/182987256-2382870d-276f-4625-aebd-206857e7a55e.jpg)


Student DB ER Model:
![CS 7700 Project ER Model](https://user-images.githubusercontent.com/98552891/182987167-de75c53e-3339-4b6c-a8ac-7eb84bd6c892.jpg)

