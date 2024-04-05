import sqlite3
import statistics
import PySimpleGUI as sg
import random
#sqlite nomenclature:
#cursor is needed for everthing
#create table cursor.excute(CREATE TABLE *name of table*(table_row_name,datatype,...))
#insert data into table (c.execute("INSERT INTO *table* VALUES*")
#putting things in a tuple before executing is a good idea
#execute many data = c.executemany() execute all data = c.executeall() c.executeone
#types of datatypes NULL(something that dosent exist yet,placeholder)
#update particulars c.execute("""UPDATE (table) SET")
#data types (IMPORTANT)
#integer.numbers
#real(float)
#test(str)
#blob(bytes)
#fetch specific things i.e print entire table based on one input
connection = sqlite3.connect("student_particulars.db")
cursor = connection.cursor()
digit_to_studentyear = {1:"Freshman"}
check_to_info = {1 : "full_name"}
def user_authenthication():
    layout = [
        [sg.Text("Select type"), sg.Radio("Student","staff_or_student",default = True,key = "-student-"), sg.Radio("teacher","staff_or_student", key = "-teacher-")],
        [sg.Text("id"),sg.Input(key = "-id-")],
        [sg.Text("password"),sg.Input(key = "-password-")],
        [sg.Button("Login"), sg.Button("Exit")],
        [sg.Text("", key = 'id_error', text_color = "red")],
        [sg.Text("", key = "authenticated", text_color = "black")]
    ]
    window = sg.Window("User Authentication", layout)
    while True:
        event, value = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        if event == "Login":
            is_student = False
            is_teacher = False
            id_check = value["-id-"]
            password = value["-password-"]
            if value["-student-"]:
                cursor.execute("SELECT id,full_name FROM student_particulars WHERE id = ?",(id_check,))
                is_student = True
            if value["-teacher-"]:
                cursor.execute("SELECT id,name FROM teacher_particulars WHERE id = ?",(id_check,))
                is_teacher = True
            id_data = cursor.fetchone()
            cursor.execute("SELECT id,password FROM password WHERE id = ?",(id_check,))
            pass_check= cursor.fetchone()
            if id_check == "":
                 window["id_error"].update("Please input an id")
            elif id_data is None:
                window["id_error"].update("ERROR id not found in database")
            elif pass_check:
                window["id_error"].update("")
                if id_data[0] == id_check and pass_check[1] == password:
                    window["authenticated"].update(f"Welcome {id_data[1]}")
                    window.close()
                    if is_student:
                        main_menu_student(id_check)
                    break
                elif pass_check[1] is None:
                    popup = sg.popup_ok_cancel("ERROR, no password assigned to id. Do you want to create a new password")
                    if popup == "OK":
                        window.hide()
                        temp = new_pass(id_check)
                        if temp:
                            window.un_hide()
                            window["authenticated"].update(f"please enter your new password")
                else:
                    window["id_error"].update("Incorrect password")

def main_menu_student(id_check):
    cursor.execute("SELECT full_name FROM student_particulars WHERE id = ?",(id_check,))
    name = cursor.fetchone()
    layout = [
        [sg.Text(f"Welcome {name[0]}, You are at the menu meant for students")],
        [sg.Text("1. Check student particulars"),sg.Button("Access",key = 1)],
        [sg.Text("2. Check past and present gpa"),sg.Button("Access", key = 2)],
        [sg.Text("3. Change password"),sg.Button("Access",key = 3)],
        [sg.Button("Logout")]
    ]
    window = sg.Window("Main menu for students",layout)
    while True:
        event, value = window.read()
        if event == "Logout" or event == sg.WINDOW_CLOSED:
            window.close()
            break
        if event == 1:
            window.close()
            check_particulars(id_check)
            break
        if event == 2:
            window.close()
            gpa_menu(id_check)
            break
        if event == 3:
            window.close()
            new_pass(id_check,1)
            break
        

#this is the place where all updating of particulars take place
int_to_class = {1  : "Freshman", 2 : "Freshman", 3 : "Sophomore", 4 : "Sophomore", 5 : "Junior", 6 : "Junior", 7 : "Senior", 8 : "Senior"}
int_to_semester = {1 : "S1", 0 : "S2"}
int_to_year = {0 : "Y1", 1 : "Y1", 2 : "Y2", 3 :"Y3", 4 : "Y4"}

def check_particulars(id_check):
    cursor.execute("SELECT * FROm student_particulars WHERE id = ?",(id_check,))
    particulars= cursor.fetchone()
    year = particulars[2]
    print(year)
    layout = [
        [sg.Text("You are at the menu for checking particulars")],
        [sg.Text("Here are you partciulars")],
        [sg.Text(f"Id {particulars[0]}", text_color = "black")],
        [sg.Text(f" Full Name {particulars[1]}", text_color = "black"), sg.Button("Change",key = "-change_name-")],
        [sg.Text(f"Current student type {int_to_class[year]}",text_color = "black") ],
        [sg.Text(f"Current Year: {int_to_year[year // 2]}{int_to_semester[(year + 2) % 2]}",text_color= "black")],
        [sg.Text("",key = "updater")],
        [sg.Button("Go Back",key = "-go_back-"),sg.Button("Logout",key = "-logout-")]
    ]
    window = sg.Window("Particulars checker",layout)
    while True:
        event,values = window.read()
        if event == "-go_back-" or event == "-logout-" or event == sg.WINDOW_CLOSED:
            window.close()
            if event == "-go_back-":
                main_menu_student(id_check)
            break
        elif event == "-change_name-":
            window.close()
            change_particulars(id_check)
            break

def change_particulars(id_check):
    layout = [
        [sg.Text("Type in your new name"),sg.Input("",key = "-input_field-")],
        [sg.Button("OK",key = "-ok-"),sg.Button("Go Back",key = "-go_back-") ,sg.Button("Logout",key = "-cancel-")],
        [sg.Text("",key = "-updater-",text_color = "red")]
    ]       
    window  = sg.Window("Particulars changer",layout)
    while True:
        event,values = window.read()
        if event == "-cancel-" or event == sg.WINDOW_CLOSED:
            window.close()
            break
        elif event == "-go_back-":
            window.close()
            check_particulars(id_check)
            break
        elif event == "-ok-":
            window["-updater-"].update("")
            if values["-input_field-"] == "":
                window["-updater-"].update("ERROR please input your changed name")
            else: #if possible find out how to change color for specific part of text
                cursor.execute("UPDATE student_particulars SET full_name = ? WHERE id = ?",(values["-input_field-"],id_check))
                temp = sg.popup_ok_cancel(f"your changed name is {values["-input_field-"]} are you fine with your changes",title = "confirmation")
                if temp == "OK":
                    connection.commit()
                    window["-updater-"].update("Changes succesfully implemented",text_color = "black")
                else:
                    connection.rollback()
                    window["-updater-"].update("Changes succesfully reverted",text_color = "black")

value_to_prof = {0 : "Associdate proffesor" ,1 : "Professor",3 : "Head of department"}



#menu for checking gpa, you can check one semester,or your cap. you can filter by grade and (idk if i will implement this) check mean median standard derivation for everything, student accesing of scores is RESTRICTED
#only teachers are able to details for students
select_to_sem = {1 : 'Y1S1', 2 : "Y1S2", 3 : "Y2S1", 4 : "Y2S2", 5 : "Y3S1", 6 : "Y3S2", 7 : "Y4S1", 8 : "Y4S2"}
gpa_to_classification = {1 : "failed", 2 : "failed", 3 : "failed", 4 : "passed", 5 : "passed", 6 : "third class", 7 : "second class lower", 8 : "second class upper", 9 : "first class honors", 10 :"first class honors"}

def gpa_menu(id_check):
    cursor.execute("SELECT Max(semester) FROM student_grades WHERE id = ? AND grade IS NOT NULL",("U2323911F",))
    temp = cursor.fetchall()
    sem_arr = []
    for i in range(temp[0][0]):
        sem_arr.append(f"{int_to_year[(i + 1) // 2]}{int_to_semester[(i + 3) % 2]}")
    layout = [
        [sg.Text("You're at the menu for changing gpa")],
        [sg.Text("Your current gpa (CAP): "),sg.Button("Access", key = "-gpa_all-")],
        [sg.Text("",key = "gpa_all_val")],
        [sg.Text("Check gpa for specific semester"),sg.DropDown(sem_arr, key = "-sem_check-"),sg.Button("Check",key = "-check-")],
        [sg.Text("",key = "-update_sem-",text_color = "red" )],
        [sg.Button("Exit", key = "-exit-")]
    ]
    window = sg.Window("Gpa Menu",layout)
    while True:
        event,values = window.read()
        if event == "-exit-" or event == sg.WINDOW_CLOSED:
            window.close()
            break
        elif event == "-check-":
            window["-update_sem-"].update("")
            if values["-sem_check-"] == "":
                window["-update_sem-"].update("Please input a semester to check")
            else:
                sem_check = values["-sem_check-"]
                sem_value = (int(sem_check[1]) - 1) * 2 + int(sem_check[3])
                gpa_value = gpa_calculator(id_check,sem_value,values["-sem_check-"])
                window["-update_sem-"].update(gpa_value, text_color = "black")
        elif event == "-gpa_all-":
            window["gpa_all_val"].update("")
            temp = gpa_calculator(id_check,0,0)
            window["gpa_all_val"].update(temp,text_color = "black")

def gpa_calculator(id_check,all_or_sem,sem_check): 
    def gpa_message(total_gpa,id_check,message):
        gpa_classification = int(total_gpa // 0.5) 
        cursor.execute("SELECT year_program FROM student_particulars WHERE id =?",(id_check,))
        year_check = cursor.fetchone()
        if year_check[0] == 3:
            gpa_to_classification[6] = "have passed with merit"   
        final_message = f"{message} {total_gpa} Honors rating: {gpa_to_classification[gpa_classification]}"
        return final_message
    if all_or_sem == 0:
        cursor.execute("""SELECT module_to_weightage.au,grade_to_gpa.gpa
                FROM student_grades 
                INNER JOIN module_to_weightage ON student_grades.module = module_to_weightage.module
                INNER JOIN grade_to_gpa ON student_grades.grade = grade_to_gpa.grade
                WHERE id = ? """,(id_check,))
        message = "CGPA value:"
    else:
        cursor.execute("""SELECT module_to_weightage.au,grade_to_gpa.gpa
               FROM student_grades 
               INNER JOIN module_to_weightage ON student_grades.module = module_to_weightage.module
               INNER JOIN grade_to_gpa ON student_grades.grade = grade_to_gpa.grade
               WHERE id = ? AND semester = ?""",(id_check,all_or_sem))
        message = f"Gpa for {sem_check} value:"
    grades = cursor.fetchall() #list of tuples
    grades_final = [list(grade) for grade in grades] #list of lists
    total_au = sum(map(lambda x : x[0],grades_final))
    total_grades = sum(map(lambda x : x[0] * x[1],grades_final))  
    total_gpa = round((total_grades / total_au),2)
    return gpa_message(total_gpa,id_check,message)

#password editor functions(done)
def new_pass(id_check,menu_type):
    layout = [
        [sg.Text("You are now at the menu for creating new passwords")],
        [sg.Text("The requirements are 1.length must be greater then 9 2.password must contain at least one digit 3.password must contain at least one upper case letter")],
        [sg.Text("enter your new password"),sg.Input(key = "-new_pass-")],
        [sg.Text("Reenter your password"),sg.Input(key = "-pass_check-")],
        [sg.Button("Confirm"),sg.Button("Exit")],
        [sg.Text("",key = "-confirm_check-",text_color = "red")]
    ]
    window = sg.Window("new password",layout)
    while True:
        event, value = window.read()
        window["-confirm_check-"].update("", text_color = "red")
        if event == "Exit":
            window.close()
            if menu_type == 0:
                user_authenthication()
            elif menu_type == 1:
                main_menu_student(id_check)
            break
        elif event == sg.WINDOW_CLOSED:
            break
        elif event == "Confirm":
            new_pass = value["-new_pass-"]
            pass_check = value["-pass_check-"]
            if new_pass == "" and pass_check == "":
                window["-confirm_check-"].update("please input something")
            elif new_pass== "":
                window["-confirm_check-"].update("please enter a password")
            elif pass_check == "":
                window["-confirm_check-"].update("please authenticate your password")
            else:
                pass_final = password_checker(new_pass)
                if pass_final[0]:
                    cursor.execute("UPDATE password SET password = ? WHERE id = ?",(new_pass,id_check))
                    popup = sg.popup_ok_cancel("All checks completed, are you sure you want to use this password?")
                    if popup == "OK":
                        connection.commit()
                        window.close()
                    elif popup == "Cancel":
                        connection.rollback()
                        window["-confirm_check-"].update("Password changes reverted", text_color = "black")
                elif pass_final[0] is False:
                    temp = "Error, password failed checks, the following changes you need to make are: "
                    counter = 0
                    for index,element in enumerate(pass_final[1]):
                        if pass_final[1][index] is True:
                            continue
                        else:
                            counter += 1
                            temp += f"{counter}. {element}"
                    window["-confirm_check-"].update(temp, text_color = "black")

def password_checker(password):
    total_check = ["Password must be at least 9 digits ","Password must contain at least one digit","Password must have at least one upper case letter"]
    if len(password) >= 9:
        total_check[0] = True
    digit_check = any(chr.isdigit() for chr in password)
    if digit_check:
        total_check[1] = digit_check
    upper_check = any(chr.isupper() for chr in password)
    if upper_check:
        total_check[2] = True
    if total_check[0] is True and total_check[1] is True and total_check[2] is True:
        return True,total_check
    else:
        return False,total_check
    
#student particulars : id(primary key) full_name semester school major student_or_teacher(0 = teacher 1 = student)
#passwords id(primary key) password
#get records from a specific database select id (primary key) to get specific output datatype in these databses(follow formatting exactly after counter)
#1. student particulars (type 1)
#if parameter id = 0 then everything is printed out
#in parameter datatype here are the options (follow this exactly) 0. print out everything 1. name  2.semester 3.school 4.major 5.student_or_teacher(you most likely wont need this)
#you can either get one value or get many values
    
int_to_database = {1 : "student_particulars"}
def getrecords(database,id,datatype):
    try:
        if datatype > 5 or datatype < 0:
            print("available datatypes  0. print out everything 1. name  2.semester 3.school 4.major 5.student_or_teacher(you most likely wont need this)")
            retry = int(input("select correct datatype or 'stop' to exit program"))
            if retry == 'stop'.upper():
                return False
            else:
                getrecords(database,id,datatype)
        cursor.execute(f"SELECT * FROM {database} WHERE id = ?",(id,))
        result = cursor.fetchone()
        if result is None:
            print("no id exists in database")
            retry = input("select correct id or 'stop' to exit program")
            if retry == "stop".upper():
                return False
            else:
                getrecords(database,retry,datatype)
        else:
            if datatype == 0:
                return result
            else:
                return result[datatype]
    except:
        print("error")
    finally:
        connection.close()

grade_to_value = {"A+": 5.0, "A": 5.0, "A-": 4.5, "B+": 4.0, "B": 3.5, "B-": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}
#developer tools, stream line table editting process
def developer_menu():
    print("you are at the menu for developers only")
    print("1. add new module")
    print("2. add new grade")
    dev_input = int(input("what do you want to do"))
    if dev_input == 1:
        print("module should be in upper case (IMPORTANT) 2. weightage needs to be an integer")
        module = input("type in your new module").upper()
        weightage = int(input("type in your weightage"))
        new_module(module,weightage)
    elif dev_input == 2:
        grade_adder()
        
int_to_moduletype = {1 : "General Engineering", 2 : "Civil Engineering", 3 : "ICC"}
def new_module(module,weightage):
    try:
        cursor.execute("INSERT INTO module_to_weightage VALUES (?,?)",(module,weightage))
    except Exception as e:
        print(e)
        developer_menu()
    finally:
        connection.commit()
        print("data successfully edited")
        connection.close()
    developer_menu()

def grade_adder():
    while True:
        id = input("enter your id")
        cursor.execute("SELECT id FROM student_particulars WHERE id = ?",(id,))
        id_check = cursor.fetchone()
        if id_check is not None:
            if id == id_check[0]:
                print("pog")
                break
        elif id != id_check:
            print("incorrect id")
    while True:
        module = input("input your module")
        cursor.execute("SELECT module FROM module_to_weightage WHERE module = ?",(module,))
        module_check = cursor.fetchone()
        if module_check is None:
            print("module not found in system")
            continue
        if module == module_check[0]:
            cursor.execute("SELECT module FROM student_grades WHERE id = ?",(id,))
            module_check2 = cursor.fetchone()
            if module_check2 is None:
                break
            else:
                print("grade already present in database")
                continue
        elif module != module_check[0]:
            print("module not in database")
        elif module == "stop".upper():
            break
    while True:
        grade = input("what is your grade").upper()
        if grade == "null".upper():
            break
        elif grade == "stop".upper():
            break
        elif grade in grade_to_value:
            print("pog")
            break
        else:
            print("enter correct grade")
    while True:
        semester = input("what is the semester")
        if semester.isdigit():
            semester = int(semester)
            if semester > 8 or semester < 1:
                print("input a value from 1 to 8")
                continue
            else:
                break
        if semester == "stop".upper():
            break
        else:
            print("please enter a digit")
            continue   
    try:
        if grade != 0:
            cursor.execute("INSERT INTO student_grades VALUES (?,?,?,?)",(id,module,grade,semester))
        else:
            cursor.execute("INSERT INTO student_grades VALUES (?,?,?,?)",(id,module,None,semester))
    except Exception as e: 
        print(e)      
    finally:
        connection.commit()
        print("data editted succesfully")

#this is the place for everything related to statistics for STUDENTS ONLY, this includes checking total gpa percentile. checking mean,median and standard derivation
#statistics checker(half done (need gpa))
def statistics_menu(id_check):
    while True:
        print("you are now at the menu for checking statistics")
        print("1. Check gpa percentile")
        print("2 Check specific module by semester")
        stat_input = input("What do you want to do? ")
        if stat_input.isdigit():
            stat_input = int(stat_input)
        if stat_input == 2:
            mod_check(id_check)
            break
        elif stat_input == 3:
            main_menu_student(id_check)
            break

def mod_check(id_check):
     while True:
        sem_input = input("Select which semester you want to check ").upper()
        if sem_input == "STOP":
            main_menu_student(id_check)
            break
        if sem_input.isdigit():
            sem_input = int(sem_input)
            if sem_input > 8 or sem_input < 1:
                print("enter valid semester")
        else:
            print("enter valid input")
        cursor.execute("SELECT module,grade FROM student_grades WHERE id = ? AND semester = ? AND grade IS NOT NULL",(id_check,sem_input))
        modules = cursor.fetchall()
        print(modules)
        break
     while True:
        if modules == []:
            print("Semester has not beem completed yet")
            continue
        else:
            print("here are the available modules")
            for counter,module in enumerate(modules):
                print(f"{counter + 1}. {module[0]}")
            mod_input = int(input("which module do you want to check"))
            if mod_input > len(modules) or mod_input < 1:
                print("invalid module")
            else:
                stat_calc_menu(modules[mod_input][0],id_check)
                break
value_to_grade = {
    0: 'F',  1: 'F',  2: 'D',  3: 'D+',  4: 'C',  5: 'C+', 6: 'B-', 7: 'B',  8: 'B+', 9: 'A-',10: 'A'
                }
print(value_to_grade[3.0 // 0.5])

def stat_calc_menu(id_check):
    cursor.execute("SELECT Max(semester) FROM student_grades WHERE id = ? AND grade IS NOT NULL",("U2323911F",))
    temp = cursor.fetchall()
    sem_arr = []
    for i in range(temp[0][0]):
        sem_arr.append(i + 1)
    layout = [
        [sg.Text("You are at the menu for statistics calculation")],
        [sg.Text("Select the sem you wish to check"),sg.DropDown(sem_arr,key = "-sem_value-"),sg.Button("Access", key = "-mod_access-")],
        [sg.Text("",text_color="red",key = "updater")],
        [sg.Button("Go Back", key = "-go_back-"),sg.Button("Logout",key = "-log_out-")]
    ]
    window = sg.Window("statistics menu",layout)
    while True:
        event,values = window.read()
        if event == "-log_out-" or event == sg.WIN_CLOSED:
            break
        elif event == "-go_back-":
            main_menu_student(id_check)
            break
        elif event == "-mod_access-":
            if values["-sem_value-"] == "":
                window["updater"].update("Please input a semeste")
            else:
                cursor.execute("SELECT module FROM student_grades WHERE semester = ? AND id = ?",(values["-sem_value-"],id_check))
                mod_choices = cursor.fetchall()
                module_all = []
                list(map(lambda x : module_all.append(x[0]),mod_choices))
                window.close()
                stat_calc_2(id_check,module_all,values["-sem_value-"])

def stat_calc_2(id_check,mod_choices,sem_value):
    print(sem_value)
    layout = [
        [sg.Text(f"What module for semester {sem_value} do you want to check?")],
        [sg.DropDown(mod_choices,size = 10,key = "-mod_choices-"),sg.Button("Access")],
        [sg.Text("",key = "-statistics-")],
        [sg.Text("",key = "-percentage-"),sg.Button("Access graphs of selected module",visible= False, key = "-graphs-")],
        [sg.Text("",key = "-updater-", text_color = "red")],
        [sg.Button("Go back to previous page", key = "-back_one-"),sg.Button("Go back to main menu",key = "-back_main-"),sg.Button("Logout")]
    ]   
    window = sg.Window(f"Module selections for semester {sem_value}",layout)
    while True:
        event,values = window.read()
        if event == "Logout" or event == sg.WIN_CLOSED:
            break
        elif event == "-back_one-":
            window.close()
            stat_calc_menu(id_check)
        elif event == "-back_main-":
            window.close()
            main_menu_student(id_check)
        elif event == "Access":
            window["-updater-"].update("")
            if values["-mod_choices-"] == "":
                window["-updater-"].update("Please select a mod.")
            else:
                grades_user,grades_all = fetch_grades(values["-mod_choices-"],id_check)
                mean,percentage = mean_calc(grades_user,grades_all)
                median = median_calc(grades_all)
                stan_dev = sd_calc(grades_all)
                window["-statistics-"].update(f"Mean : {value_to_grade[mean // 0.5]} median: {value_to_grade[median[0] // 0.5]} standard derivation {stan_dev}")
                window["-percentage-"].update(f"You are {percentage[0]}{percentage[1]} then the cohort")
                window["-graphs-"].update(visible = True) 
        elif event == "-graphs-":
            print("pog")
            
def fetch_grades(module,id_check):
    cursor.execute("""SELECT grade_to_gpa.gpa FROM student_grades
                      INNER JOIN grade_to_gpa ON student_grades.grade = grade_to_gpa.grade
                      WHERE module = ?
                      ORDER BY grade_to_gpa.gpa ASC""",(module,))
    grades_temp = cursor.fetchall() #fetching all available user scores for particular module
    grades_all = [list(grade) for grade in grades_temp]
    cursor.execute("""SELECT grade_to_gpa.gpa FROM student_grades
                      INNER JOIN grade_to_gpa ON student_grades.grade = grade_to_gpa.grade
                      WHERE module = ? AND id = ?""",(module,id_check))
    grades_user= cursor.fetchone() #fetching users score
    return grades_user[0],grades_all

def mean_calc(grades_user,grades_all): #list of lists with one index of all grades in module
    mean = round((sum(map(lambda x : x[0],grades_all)) / len(grades_all)),2)
    percentage_temp = round((grades_user / mean),2)
    if percentage_temp > 1:
        percentage = [int((percentage_temp - 1) * 100),"% higher"]
    elif percentage_temp < 1:
        percentage = [int((1 - percentage_temp) * 100),"% lower"]
    else:
        percentage = ["You have the same"," score as the mean"]
    return mean,percentage

def median_calc(grades_all):
    grades_list = []
    list(map(lambda x :grades_list.append(x[0]),grades_all))
    if len(grades_all) // 2 == 1:
        median = grades_all[(len(grades_all) // 2 )]
    else:
        median = round((grades_all[(len(grades_all) // 2 -1)] + grades_all[(len(grades_all) // 2 )]) /  2.2)
    return median

def sd_calc(grades_all):
    grades_list = []
    list(map(lambda x : grades_list.append(x[0]),grades_all))
    stan_dev = round(statistics.stdev(grades_list),2)
    return stan_dev

#this is the place for everything related to teachers
#adding and removing students should only be done in their respective schools, i.e only CEE teachers can edit CEE students and vice versa
#detailed preview of all grades should be done here, students only have restricted access
#table teacher_particulars (id,name text school(you will use this for filters when sorting) text,field_of_expertise integer (0-associate proffesor,1-proffesor,2-head of departmnet),student or teacher integer(as a check if you somehow manage to get in))
#test teacher(use this to check teacher functionality) id:123 name :test name school : CEE field_of_expertise Civil Engineering professor type
value_to_postion = {0 : "Associate proffessor", 1 : "Professor", 2 : "HOD" }


def main_menu_teacher(id_check):
    cursor.execute("SELECT id,professor_type FROM teacher_particulars WHERE id = ?",(id_check,))
    id,prof_type = cursor.fetchone()
    layout = [
        [sg.Text(f"You are at the main menu for teachers, Welcome {value_to_prof[prof_type]} {id}")],
        [sg.Text("1. Add students"),sg.Button("Access", key = "-add_student-")],
        [sg.Text("2. Remove students"),sg.Button("Access", key = "-remove_student-")],
        [sg.Button("Logout")]
    ]
    window = sg.Window("Professor menu",layout)
    while True:
        event,values = window.read()
        if event == "Logout" or event == sg.WIN_CLOSED:
            break
        elif event == "-add_student-":
            window.close()
            add_student(id_check)
        elif event == "-remove_student-":
            window.close()
            remove_student(id_check)

gender_list = ["M","F","Other"]
program_list = [3,4]
error_to_string = { 0 : "You have not selected a degree", 1 : "You have not selected a name", 2 : "You have no selected a gender", 3 : "You have no selected the program type"}
error_to_string = ["You have not selected a degree", "You have not selected a name", "You have no selected a gender", "You have no selected the program type"]
school_to_degree = {"CEE" : ["Civil Engineering","Enviromental Engineering","Maritime Studies"]}
def add_student(id_check):
    cursor.execute("SELECT school FROM teacher_particulars WHERE id = ?",(id_check,))
    school_type = cursor.fetchone()
    if school_type is None:
        sg.popup("You do not have permission to enter this menu")
        return False
    school_pool = school_to_degree[school_type[0]]
    layout = [
        [sg.Text("You are at the menu for adding students")],
        [sg.Text("Select the major that the new student will be in (limited to your school)"),sg.DropDown(school_pool,key = "-selected_degree-",size = 20)],
        [sg.Text("Input the new student's name"),sg.Input(key = "-new_name-",size = 15)],
        [sg.Text("Input the student's gender"),sg.DropDown(gender_list, key = "-gender-"),sg.Text("Input the type of program"),sg.DropDown(program_list, key = "-program_type-")],
        [sg.Text("",text_color= "red", key = "updater")],
        [sg.Button("Complete"),sg.Button("Go back to previous menu", key = "-go_back-"),sg.Button("Logout")]     
    ]
    window = sg.Window("add students menu",layout)
    while True:
        event,values = window.read()
        if event == "Logout" or event == sg.WINDOW_CLOSED:
            break
        elif event == "-go_back-":
            window.close()
            main_menu_teacher(id_check)
        elif event == "Complete":
            values_arr = [values["-selected_degree-"],values["-new_name-"],values["-gender-"],values["-program_type-"]]
            string_error = ""
            window["updater"].update("")
            counter = 1
            for index,value in enumerate(values_arr):
                if value == "":
                    string_error += f"{counter}. {error_to_string[index]} "
                    counter += 1
                else:
                    pass
            window["updater"].update(string_error)

            if string_error == "":
                new_id = "U" + str(random.randint(1000000,9999999)) + chr(random.randint(ord("A"),ord("Z")))
                popup = sg.popup_ok_cancel(f"Here are the particulars of the new student \n id: {new_id} name {values["-new_name-"]} gender {values["-gender-"]} \n school {school_type[0]}, major {values["-selected_degree-"]}, year programe {values["-program_type-"]}")
                cursor.execute("INSERT INTO student_particulars VALUES (?,?,?,?,?,?,?,?)",(new_id,values["-new_name-"],1,school_type[0],values["-selected_degree-"],0,values["-program_type-"],values["-gender-"]))
                if popup == "OK":
                    connection.commit()
                    window["updater"].update("Data successfully inserted, press go back to access other functions",text_color = "black")
                else:
                    connection.rollback()
                    window["updater"].update("Data succesfully reverted",text_color = "black")  

def remove_student(id_check):
    layout = [
        [sg.Button("Go back",key = "-go_back-"),sg.Button("Logout",key = "-logout-")],
    ]
    window = sg.Window("Remove students menu",layout)
    while True:
        event, value = window.read()
        if event == "-logout-" or event == sg.WIN_CLOSED:
            break
        elif event == "-go_back-":
            window.close()
stat_calc_menu("CV1011","U2323911F")

    

