import sqlite3
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
#data types (IMPORTANT)
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
    
def user_authentication():
    person_type = int(input("Are you 1. student or 2. teacher"))
    if person_type == 1:
        while True:
            id_check = input("type in your id").upper()
            cursor.execute("SELECT * FROM student_particulars WHERE id = ?",(id_check,))
            result = cursor.fetchone()
            if result:
                break
            else:
                print("Id not found in database, please input correct id")
    if person_type == 1234:
        developer_menu()
        return False
    while True:
        password_input = input("please enter your password ")
        cursor.execute("""SELECT * FROM password WHERE id = ?""",(id_check,))
        password_check = cursor.fetchone()
        if password_check[1] == password_input:
            cursor.execute("SELECT * FROM student_particulars WHERE id = ?",(id_check,))
            stu_name = cursor.fetchone()
            print(f"Welcome {stu_name[1]}")
            main_menu_student(id_check)
            break
        else: 
            print("incorrect password")
            continue

def main_menu_student(id_check):
    print("1. Check student particulars")
    print("2. Check past and present gpa")
    print("3. Edit password")
    print("4. Check student particulars")
    print("0. Quit the program")
    while True:
        student_menu = int(input("what do you want to do"))
        if student_menu == 1:
            check_particulars(id_check)
            return False
        if student_menu == 2:
            gpa_menu(id_check)
            return False
        if student_menu == 3:
            password_editor(id_check)
            return False
        if student_menu == 4:
            update_particulars(id_check)
            return False
        if student_menu == 5:
            print("Thank you for using our program")
            break
        else:
            print("Please select a proper input")

#menu for checking gpa, you can check one semester,or your cap. you can filter by grade and (idk if i will implement this) check mean median standard derivation for everything, student accesing of scores is RESTRICTED
#only teachers are able to details for students
select_to_sem = {1 : 'Y1S1', 2 : "Y1S2", 3 : "Y2S1", 4 : "Y2S2", 5 : "Y3S1", 6 : "Y3S2", 7 : "Y4S1", 8 : "Y4S2"}
grade_to_value = {"A+": 5.0, "A": 5.0, "A-": 4.5, "B+": 4.0, "B": 3.5, "B-": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}
gpa_to_classification = {1 : "have failed", 2 : "have failed", 3 : "have failed", 4 : "have passed", 5 : "have passed", 6 : "are third class", 7 : "are second class lower", 8 : "are second class upper", 9 : "are first class honors", 10 :"are first class honors"}


def gpa_menu(id_check):
    while True:
        print("you are currently at the menu for chacking gpa")
        gpa_men = input("1. check current gpa 2.check gpa by semester 3.see statistics per module/gpa")
        if gpa_men.isdigit():
            gpa_men = int(gpa_men)
        elif gpa_men.isdigit() != True:
            print("input must be an integer")
        if gpa_men == 1:
            gpa_all(id_check)
        if gpa_men == 2:
            gpa_sem(id_check)

def gpa_all(id_check):
    cursor.execute("""SELECT module_to_weightage.au,grade_to_gpa.gpa
               FROM student_grades 
               INNER JOIN module_to_weightage ON student_grades.module = module_to_weightage.module
               INNER JOIN grade_to_gpa ON student_grades.grade = grade_to_gpa.grade
               WHERE id = ? """,(id_check,))
    grades = cursor.fetchall()
    grades_final = [list(grade) for grade in grades]
    total_au = sum(map(lambda x : x[0],grades_final))
    total_grades = sum(map(lambda x : x[0] * x[1],grades_final)) 
    total_gpa = round((total_grades / total_au),2)
    gpa_message(total_gpa,id_check)

def gpa_message(total_gpa,id_check):
    gpa_classification = int(total_gpa // 0.5) 
    cursor.execute("SELECT school FROM student_particulars WHERE id =?",(id_check,))
    year_check = cursor.fetchone()
    print(year_check)
    if year_check == "NBS":
        gpa_to_classification[6] = "have passed with merit"   
    print(f"your gpa is {total_gpa} and you {gpa_to_classification[gpa_classification]}")
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
        if sem_select > 8:
            print("semester does not exist in database")
            continue
        if grades is not None:
            total_gpa = gpa_calculator(grades,0)
            print(f"your grades for {select_to_sem[sem_select]} is {total_gpa}")
            main_menu_student(id_check)
            break

def gpa_calculator(grades): #change this later
    counter = 0
    au = []
    total_grade = 0
    total_au = 0 
    for grade in range(len(grades)):
        cursor.execute("SELECT au FROM module_to_weightage WHERE module = ? ",(grades[grade][0],))
        temp = cursor.fetchone()
        au.append(temp[0])
    for gpa in range(len(au)):
        grade = grade_to_value[grades[gpa][1]]
        total_au += au[counter]
        total_grade += grade * au[counter]
        counter += 1
    total_gpa = round((total_grade / total_au),2)
    return total_gpa
    
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
        elif particular_check == 2:
            main_menu_student(id_check)


#password editor functions(done)
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
        print("all conditions passed")
        return True
    else:
        counter = 0
        for check in total_check:
            if check is True:
                pass
            else:
                counter += 1
                print(f"{counter}. {check}", end = '')
        return False
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
#use this function for sorting, give it various filters and it will sort by grade/year/grades for au.(this is not done yet)
#this is applicable for both students and teachers. students: you will want to see mean/median/sd(maybe dont implement this) based on specifc grade or gpa by semester or total gpa
#applicable databses
# user_authentication()

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
            cursor.execute("SELECT module FROM student_grades WHERE id = ?",(id_check,))
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
        print("data editted succesfully")
        connection.commit()
        connection.close()

# cursor.execute("INSERT INTO student_particulars VALUES (?,?,?,?,?,?)",("U90312312F","Pos Mans",2,"COE","Civil Engineering",0))
#this is the place for everything related to teachers
#this is where sorting,adding,removing students will take place
#adding and removing students should only be done in their respective schools, i.e only CEE teachers can edit CEE students and vice versa
#detailed preview of all grades should be done here, students only have restricted access
#table teacher_particulars (id,name textschool(you will use this for filters when sorting),field_of_expertise integer (0-associate proffesor,1-proffesor,2-head of departmnet),student or teacher integer(as a check if you somehow manage to get in))
        
# cursor.execute("INSERT INTO teacher_particulars VALUES (?,?,?,?,?,?)",("123","123","COE"))
# def main_menu_teacher(id_check)
user_authentication()