import sqlite3
import statistics
import PySimpleGUI as sg
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

def check_id():
    while True:
        id_check = input("what is your id")
        cursor.execute("SELECT * FROM student_particulars WHERE Id = ?",(id_check,))
        particulars = cursor.fetchone()
        if particulars:
            print(f"your particulars are: id {particulars[0]} Full name {particulars[1]} email {particulars[2]} student year {particulars[3]}")
            break
        else:
            print("nothing here")

def update_particulars(id_check):
    while True:
        cursor.execute("SELECT * FROM student_particulars WHERE Id = ?",(id_check,))
        edit_version = cursor.fetchone()
        if edit_version:
            edit_version = list(edit_version)
            update_particulars_2(edit_version,id_check)

def update_particulars_2(edit_version,id_check): #needs to be editted
    while True:
        print(f"your particulars are: id {edit_version[0]} Full name {edit_version[1]} email {edit_version[2]} student year {edit_version[3]}")
        edit_checker = int(input("what do you want to change 1.name, 5. stop editing"))
        if edit_checker != 5:
            update_info = input(f"enter your new {check_to_info[edit_checker]}")
        if 0 < edit_checker < 4:
            edit_version[edit_checker] = update_info
        if edit_checker == 5:
            print(f"here are your final details {edit_version}")
            final_check = int(input("are you fine with the changes? 1. Yes, 2. No "))
            if final_check == 2:
                continue
            elif final_check == 1:
                break
    cursor.execute("UPDATE student_particulars SET full_name = ? WHERE Id = ?",(edit_version[1],id_check))
    connection.commit()
    print("Changes successfully executed")
    main_menu_student(id_check)
    return False

value_to_prof = {0 : "Associdate proffesor" ,1 : "Professor",3 : "Head of department"}
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
                if id_data[0] == id_check and pass_check[0] == password:
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
        [sg.Text("2. Check past and present gpa"),sg.Button("Access")],
        [sg.Button("Logout")]
    ]
    window = sg.Window("Main menu for students",layout)
    while True:
        event, value = window.read()
        if event == "Logout" or sg.WINDOW_CLOSED:
            sg.popup("Goodbye!")
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
            password_editor(id_check)
            break
        if event == 4:
            window.close()
            update_particulars(id_check)
            break

#menu for checking gpa, you can check one semester,or your cap. you can filter by grade and (idk if i will implement this) check mean median standard derivation for everything, student accesing of scores is RESTRICTED
#only teachers are able to details for students
select_to_sem = {1 : 'Y1S1', 2 : "Y1S2", 3 : "Y2S1", 4 : "Y2S2", 5 : "Y3S1", 6 : "Y3S2", 7 : "Y4S1", 8 : "Y4S2"}
gpa_to_classification = {1 : "have failed", 2 : "have failed", 3 : "have failed", 4 : "have passed", 5 : "have passed", 6 : "are third class", 7 : "are second class lower", 8 : "are second class upper", 9 : "are first class honors", 10 :"are first class honors"}

def gpa_menu(id_check):
    while True:
        print("you are currently at the menu for chacking gpa")
        gpa_men = input("1. check current gpa 2.check gpa by semester 3.see statistics per module/gpa")
        if gpa_men.isdigit():
            gpa_men = int(gpa_men)
            if gpa_men == 1:
                gpa_calculator(id_check,0)
            elif gpa_men == 2:
                gpa_sem(id_check)
            else:
                print("invalid input")
                continue
        else:
            print("gpa must be a digit")

def gpa_calculator(id_check,all_or_sem): #add additional inputs in if stat
    if all_or_sem == 0:
        cursor.execute("""SELECT module_to_weightage.au,grade_to_gpa.gpa
                FROM student_grades 
                INNER JOIN module_to_weightage ON student_grades.module = module_to_weightage.module
                INNER JOIN grade_to_gpa ON student_grades.grade = grade_to_gpa.grade
                WHERE id = ? """,(id_check,))
        message = "Your total gpa"
    else:
        cursor.execute("""SELECT module_to_weightage.au,grade_to_gpa.gpa
               FROM student_grades 
               INNER JOIN module_to_weightage ON student_grades.module = module_to_weightage.module
               INNER JOIN grade_to_gpa ON student_grades.grade = grade_to_gpa.grade
               WHERE id = ? AND semester = ?""",(id_check,all_or_sem))
        message = f"Your gpa for {select_to_sem[all_or_sem]}"
    grades = cursor.fetchall() #list of tuples
    print(grades)
    grades_final = [list(grade) for grade in grades] #list of lists
    total_au = sum(map(lambda x : x[0],grades_final))
    total_grades = sum(map(lambda x : x[0] * x[1],grades_final))  
    total_gpa = round((total_grades / total_au),2)
    gpa_message(total_gpa,id_check,message)

def gpa_message(total_gpa,id_check,message): #edit this with year_to_sem
    gpa_classification = int(total_gpa // 0.5) 
    cursor.execute("SELECT school FROM student_particulars WHERE id =?",(id_check,))
    year_check = cursor.fetchone()
    if year_check[0] == "NBS":
        gpa_to_classification[6] = "have passed with merit"   
    print(f"{message} is {total_gpa} and you {gpa_to_classification[gpa_classification]}")
    main_menu_student(id_check)

def gpa_sem(id_check):
    while True:
        print("youre at the menu for selecting gpa by semester")
        sem_select = input("Select which semester you wish to find")
        if sem_select.isdigit():
            sem_select = int(sem_select)
        elif sem_select == "stop".upper():
            main_menu_student()
        elif sem_select.isdigit() != True:
            print("input must be an integer")
            continue
        cursor.execute("SELECT module,grade FROM student_grades WHERE id = ? AND semester = ?",(id_check,sem_select))
        grades = cursor.fetchall()
        if sem_select > 8 or sem_select < 1:
            print("semester does not exist in database")
            continue
        elif grades is not None:
            gpa_calculator(id_check,sem_select)
            break

#check particulars (framework done, just need to fill in features)
int_to_class = {1  : "Freshman", 2 : "Freshman", 3 : "Sophomore", 4 : "Sophomore", 5 : "Junior", 6 : "Junior", 7 : "Senior", 8 : "Senior"}
int_to_semester = {1 : "S1", 0 : "S2"}
int_to_year = {0 : "Y1", 1 : "Y1", 2 : "Y2", 3 :"Y3", 4 : "Y4"}
def check_particulars(id_check):
    while True:
        print("You're at the menu for checking particulars")
        print("1.Check current particulars")
        print("2.Return to main menu")
        particular_check = int(input("what do you want to do"))
        if particular_check == 1: 
            temp = getrecords("student_particulars",id_check,0)
            year_initialisation = temp[2]
            print(f"Student Classification: {int_to_class[year_initialisation]})")
            print(f"Current Year: {int_to_year[(year_initialisation // 2)]}{int_to_semester[((year_initialisation + 2) % 2)]}")
            print(f"")
            break
        elif particular_check == 2:
            main_menu_student(id_check)
            break


#password editor functions(done)
def new_pass(id_check):
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
            user_authenthication()
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
                        return True
                    elif popup == "Cancel":
                        connection.rollback()
                        window["-confirm_check-"].update("Password changes reverted", text_color = "black")
                if pass_final[0] is False:
                    temp = "Error, password failed checks, the following changes you need to make are: "
                    counter = 0
                    for index,element in enumerate(pass_final[1]):
                        if pass_final[1][index] is True:
                            continue
                        else:
                            counter += 1
                            temp += f"{counter}. {element}"
                    window["-confirm_check-"].update(temp, text_color = "black")

def password_editor(id_check):
    print("You're at the menu of editting passwords")
    print("1. Reset your password")
    print("2. Go back to main menu")
    password_menu = int(input("what do you want to do? "))
    while True:
        if password_menu == 1:
            cursor.execute("""SELECT * FROM password WHERE id = ?""",(id_check,))
            actual_pass = cursor.fetchone()
            break
        elif password_menu == 2:
            main_menu_student(id_check)
            break
    while True:
        pass_check = input("type in your password")
        if pass_check == actual_pass[1]:
            new_pass = input("print in your new password")
            if password_checker(new_pass):
                password_editor_2(id_check,new_pass)
                return False
            else:
                wrong_pass = int(input("\n1. Do you want to quit or 2. try again")) == 1
                if wrong_pass:
                    main_menu_student(id_check)
                    return False
                else:
                    continue           
        else:
            print("incorrect password")
            continue

def password_editor_2(id_check,new_pass):
    while True:
        print(f"do you really want to change your password? new password is {new_pass}")
        final_pass = int(input("1. Yes 2. No "))
        if final_pass == 1:
            cursor.execute("""UPDATE password SET password = ? WHERE id = ?""",(new_pass,id_check))
            connection.commit()
            print('changes executed succesfully')
            main_menu_student(id_check)
            return False
        elif final_pass == 2:
            print("changes reverted")
            main_menu_student(id_check)
            return False

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

def stat_calc_menu(module,id_check):
    mean , percentage = mean_calc(module,id_check)
    median , grades_user = median_calc(module,id_check)
    stan_dev = sd_calc(module,id_check)
    print(f"Your grade for {module} is {value_to_grade[grades_user // 0.5]}")
    print(f"here are the course statistics \n Mean: {value_to_grade[mean // 0.5]} \n Median: {value_to_grade[median // 0.5]} \n Standard derivation {stan_dev}")
    print(f"you are {percentage[0]}% {percentage[1]} then the mean of course {module} ")
    print("Do you want to")
    while True:
        stat_input = input("1. Look at statistics for other modules 2. Return to main menu")
        if stat_input.isdigit():
            stat_input = int(stat_input)
            if stat_input == 1:
                mod_check(id_check)
                break
            elif stat_input == 2:
                print("Returning to main menu")
                main_menu_student(id_check)
                break
            else:
                print("Enter valid input")
        else:
            print("input must be a number")
            
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

def mean_calc(module,id_check):
    temp = fetch_grades(module,id_check)
    grades_all = temp[1] #list of lists with one index of all grades in module
    mean = round((sum(map(lambda x : x[0],grades_all)) / len(grades_all)),2)
    percentage_temp = round((temp[0] / mean),2)
    if percentage_temp > 1:
        percentage = [int((percentage_temp - 1) * 100),"higher"]
    elif percentage_temp < 1:
        percentage = [int((1 - percentage_temp) * 100),"lower"]
    else:
        percentage = 0
    return mean,percentage

def median_calc(module,id_check):
    temp = fetch_grades(module,id_check)
    grades_temp = temp[1]
    grades_user = temp[0]
    grades_all = []
    for grade in grades_temp: #convert everything into a flat list
        for item in grade:
            grades_all.append(item)
    if len(grades_all) // 2 == 1:
        median = grades_all[(len(grades_all) // 2 )]
    else:
        median = round((grades_all[(len(grades_all) // 2 -1)] + grades_all[(len(grades_all) // 2 )]) /  2.2)
    return median,grades_user

def sd_calc(module,id_check):
    temp = fetch_grades(module,id_check)
    grades_temp = temp[1]
    grades_all = []
    list(map(lambda x : grades_all.append(x[0]),grades_temp))
    stan_dev = round(statistics.stdev(grades_all),2)
    return stan_dev

#this is the place for everything related to teachers
#this is where sorting,adding,removing students will take place
#adding and removing students should only be done in their respective schools, i.e only CEE teachers can edit CEE students and vice versa
#detailed preview of all grades should be done here, students only have restricted access
#table teacher_particulars (id,name text school(you will use this for filters when sorting) text,field_of_expertise integer (0-associate proffesor,1-proffesor,2-head of departmnet),student or teacher integer(as a check if you somehow manage to get in))
#test teacher(use this to check teacher functionality) id:123 name :test name school : CEE field_of_expertise Civil Engineering professor type
value_to_postion = {0 : "Associate proffessor", 1 : "Professor", 2 : "HOD" }

user_authenthication()

    

