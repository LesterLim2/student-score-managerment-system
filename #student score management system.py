#student score management system
#to do list: 1. password system(easy) 2. learn gui like tkinter or pygame(probably tkinter)(id'k how to tkinter) 3. export to csv functionality(easy, butn ew thing as well)
#4. actual database like sqlite(hard,needs to restructure entire code like tkinter + new thing) 
#important lists/dictionaries
available_courses = {1 : "Civil engineering", 2 : "Environmental engineering"}
year_classification = {1 : "freshman", 2 : "sophomore", 3 : "junior", 4 : "senior"}
staff_ids = ["1"] #change to dictionary please!
student_list = {"U2323911F" : ["Lester Lim","Y1Sem2"]}
password = {"U2323911F" : "1234"}


def user_identification():
    staff_or_student = int(input("are you a 1. student or 2. staff"))
    while True:
        if staff_or_student not in (1,2):
            print('enter a valid thing')
            user_identification()
        id_check = input('what is your id').upper()
        if staff_or_student == 1 and id_check in student_list:
            print("welcome")
            main_menu_student(id_check)
            gpa_all(id_check)
            break
        elif staff_or_student == 2 and id_check in staff_ids:
            print("welcome")
            main_menu_teacher()
            break
        else:
            print("incorrect user id")
            continue

def main_menu_student(id_check):
    while True:
        print("YOURE AT THE MAIN MENU FOR STUDENTS")
        print("1. check current + past gpa")
        print("2. check specifc components")
        print("3. export details")
        print("4. quit the program")
        student_menu = int(input("what do you want to do? "))
        if student_menu == 1:
            gpa_menu(id_check)
            break
        elif student_menu == 2:
            print("not implemented yet")
            continue
        elif student_menu == 3:
            print("not implmented yet")
            continue
        elif student_menu == 4:
            print("thank for using this program")
            return False
        else:
            print("please type a correct input")
            continue
        

#here is the place to put all things related to student mods/grades

grade_to_value = {"A+": 5.0, "A": 5.0, "A-": 4.5, "B+": 4.0, "B": 3.5, "B-": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}
mod_to_au = {"MH1810": 3, "PH1012": 4, "MH1811" : 3, "CV1014" : 3}
gpa_to_classification = {1 : "have failed", 2 : "have failed", 3 : "have failed", 4 : "have passed", 5 : "have passed", 6 : "are third class", 7 : "are second class lower", 8 : "are second class upper", 9 : "are first class honors", 10 :"are first class honors"}
student_record = {"U2323911F" : [
                                    [["MH1810","PH1012"],["A","B"]],
                                    [["CV1014","MH1811"],["A","A"]]
                                ]
                                    }
sem_track_to_year = {1 : "Y1S1", 2 : "Y1S2"}
def gpa_menu(id_check):
    while True:
        all_or_sem = int(input("1. check current sem gpa, 2. check previous semester gpa, 0.return to main menu"))
        if all_or_sem == 1:
            if student_record[id_check][0][1][0] == "EMPTY":
                print("you have no grades yet")
                main_menu_student(id_check)
                break
            else:
                total_gpa,total_length = gpa_all(id_check)
                total_gpa = round((total_gpa / total_length),2)
                year_checker = int(input("3 or 4 year program"))
                gpa_print_final(total_gpa,year_checker)
                break
        elif all_or_sem == 2:
            semester_tracker = int(input("which sem? 1. Y1S1"))
            total_au ,total_grade, grades_allocated = gpa_semester(id_check,semester_tracker)
            if grades_allocated:
                total_gpa = round((total_grade / total_au),2)
                year_checker = int(input("3 or 4 year program"))
                gpa_print_final(total_gpa,year_checker)
                break
            else:
                print("no grades allocated")
                continue
        if all_or_sem == 0:
            print("quit")
            
def gpa_print_final(total_gpa,year_checker):
    gpa_classification =int(total_gpa // 0.5) 
    if year_checker == 3:
        gpa_to_classification[6] = "have passed with merit"   
    print(f"your gpa is {total_gpa} and you {gpa_to_classification[gpa_classification]}")

def gpa_semester(id_check,semester_tracker):
    total_grade = 0
    total_au = 0
    temp = student_record[id_check][semester_tracker - 1]
    modules,grades = temp
    grades_allocated = True
    for module in range(len(modules)):
        if grades[module] != "EMPTY":
            current_grade = grade_to_value[grades[module]]
            current_au = mod_to_au[modules[module]]
            total_grade += current_au * current_grade
            total_au += current_au
        else:
            grades_allocated = False
    return total_au,total_grade,grades_allocated

def gpa_all(id_check):
    total_au = 0
    total_grade = 0
    total_gpa = 0
    total_length = 0
    for i in range(len(student_record[id_check])):
        total_au,total_grade,grades_allocated = gpa_semester(id_check, i + 1)
        if grades_allocated:
            total_gpa += (total_grade / total_au)
            total_length += 1
        else:
            break
    return total_gpa,total_length


def main_menu_teacher():
    print("YOURE AT THE MAIN MENU FOR TEACHERS ONLY")
    print("1. add/remove student from ciriculum")
    print("2. check student list")
    print("0. quit the program")
    while True:
        teacher_menu = int(input("what do you want to do"))
        if teacher_menu == 1:
            add_remove_student()
        if teacher_menu == 2:
            print(student_list)
            main_menu_student()
        elif teacher_menu == 0:
            print("thank you for using this program")
            return False
        else:
            print("please type a valid input")
def add_remove_student():
    print('ADD,REMOVE OR EDIT STUDENTS HERE')
    print("1. add student")
    print("2. remove student")
    print("3. check student list")
    print("4. edit student information")
    print("5.return to main_menu")
    print("6. exit the program")
    student_menu = int(input("what do you want to do"))
    if student_menu == 1:
        id1 = input("enter student ID")
        name = input("enter the student's name")
        print(f'here are the available courses {available_courses}')
        while True: 
            course_name = input("enter course name: ")
            if course_name.isdigit():
                course_name = int(course_name)
            if course_name in available_courses:
                course_name = available_courses[course_name]
                break
            else:
                input1 = int(input("invalid input. do you want to 1. continue or 2. quit"))
                if input1 == 1:
                    continue
                else:
                    main_menu_teacher()
        while True:
            Semester_tracker = int(input("is the student a new student 1. Yes 2. No")) 
            if Semester_tracker in (2,1):
                if Semester_tracker == 1:
                    Semester_tracker = year_classification[1]
                else:
                    Semester_tracker = int(input("what year are is he in"))
                    Semester_tracker = year_classification(Semester_tracker)
                final_check_add_student(id1,name,course_name,Semester_tracker)
    if student_menu == 2:
        remove_student = input("enter the id of the student you want to remove").upper()
    if remove_student in student_list:
        student_list.pop(remove_student)
        print("done")
        add_remove_student()
    elif remove_student not in student_list:
            print("please select a valid id number")
            add_remove_student()
    if student_menu == 3:
        print(student_list)
    if student_menu == 5:
        main_menu_teacher()
    if student_menu == 6:
        print("thank you for using this program")
        return False
    else:
        print("invalid stuff")
        add_remove_student()    
        
def final_check_add_student(id1,name,course_name,Semester_tracker):
    while True:
        print(f"is the details of the student correct? id: {id1}, name {name}, course name {course_name} and semester {Semester_tracker}")
        Final_check = int(input("1. Yes, 2. No"))
        student_list.update({id1: [name, course_name,Semester_tracker]})
        if Final_check == 1:
            print('thank you for using')
            add_remove_student()
            break
        elif Final_check == 2:
            Final_check = int(input("do you want to 1. exit or 2. edit"))
            if Final_check == 1:
                main_menu_teacher()
                break
            elif Final_check == 2:
                final_check_add_student_2(id1)
                break
        else:
            print("select a valid input")
            continue
           
def final_check_add_student_2(id1):
    while True:
        print("what do you want to edit")
        print(f"current details is {id1} : {student_list[id1]}")
        Final_check = int(input("1.id 2. name 3. course name 4. semester tracker 5.finished editting"))
        if Final_check in (2,3,4):
            if Final_check == 3:
                Edit = int(input('enter the new thing'))
                Edit = available_courses[Edit]
            else:
                Edit = input("enter the new thing")
            student_list[id1][Final_check - 2] = Edit
            continue
        elif Final_check == 1: 
            temp = student_list[id1]
            student_list.pop(id1)
            Edit = input("enter your new id")
            id1 = Edit
            student_list.update({Edit : temp})
        elif Final_check == 5:
            print("thank you for editting")
            add_remove_student()
            break
        else: 
            print("enter a valid number")
user_identification()      