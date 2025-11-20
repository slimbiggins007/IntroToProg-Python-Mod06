# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions with structured error handling
#       and implements the separation of concerns pattern using classes
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Jett Magnuson,11/19/2025,Created Script
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course
    2. Show current data  
    3. Save data to a file
    4. Exit the program
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
menu_choice: str = ''
students: list = []


class FileProcessor:
    """A collection of processing layer functions that work with JSON files"""

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """Reads data from a JSON file and loads it into a list of dictionary rows"""
        file = None
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages("Text file must exist before running this script!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error when reading the file!", e)
        finally:
            if file and not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """Writes data to a JSON file from a list of dictionary rows"""
        file = None
        try:
            file = open(file_name, "w")
            json.dump(student_data, file)
            file.close()
            IO.output_student_courses(student_data)
        except Exception as e:
            if file and not file.closed:
                file.close()
            IO.output_error_messages("There was a problem writing to the file!", e)


class IO:
    """A collection of presentation layer functions that manage user input and output"""

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """Displays a custom error message to the user"""
        print(message)
        if error:
            print("-- Technical Error Message -- ")
            print(error.__doc__)
            print(error.__str__())

    @staticmethod
    def output_menu(menu: str):
        """Displays the menu of choices to the user"""
        print(menu)

    @staticmethod
    def input_menu_choice():
        """Gets the menu choice from the user"""
        choice = input("What would you like to do: ")
        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """Displays the student course data to the user"""
        print("-" * 50)
        for student in student_data:
            print(f'Student {student["FirstName"]} '
                  f'{student["LastName"]} is enrolled in {student["CourseName"]}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """Gets student first name, last name, and course name from the user"""
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")

            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")

            course_name = input("Please enter the name of the course: ")

            student = {"FirstName": student_first_name,
                       "LastName": student_last_name,
                       "CourseName": course_name}
            student_data.append(student)

            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages("That value is not the correct type of data!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error when adding student data!", e)

        return student_data


# Main Body of Script
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

while True:
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":
        students = IO.input_student_data(student_data=students)
        continue

    elif menu_choice == "2":
        IO.output_student_courses(student_data=students)
        continue

    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    elif menu_choice == "4":
        break

    else:
        print("Please only choose option 1, 2, 3, or 4")

print("Program Ended")