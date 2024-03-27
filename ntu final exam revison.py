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
    cursor.execute("SELECT * FROM student_particulars WHERE Id = ?",(id_check,))
    edit_version = cursor.fetchone()
    while True:
        if edit_version:
            edit_version = list(edit_version)
            update_particulars_2(edit_version,id_check)
            break

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
int_to_moduletype = {1 : "General Engineering", 2 : "Civil Engineering", 3 : "ICC"}
def new_module():
    module = input("type in your module").upper()
    weightage = int(input("type in your weightage"))
    cursor.execute("INSERT INTO module_to_weightage VALUES (?,?)",(module,weightage))
    connection.commit()
    connection.close()
    return False

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
        if module == module_check[0]:
            cursor.execute("SELECT module FROM student_grades WHERE module = ?",(module,))
            module_check2 = cursor.fetchone()
            if module_check2 is not None:
                print("module is already present")
                continue
            else:
                break
        elif module != module_check[0]:
            print("module not in database")
        elif module == "stop".upper():
            break
    while True:
        grade = input("what is your grade").upper()
        if grade in grade_to_value:
            print("pog")
            break     
        if grade == "stop".upper():
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
        cursor.execute("INSERT INTO student_grades VALUES (?,?,?,?)",(id,module,grade,semester))
    except Exception as e: 
        print(e)      
    finally:
        print("data editted succesfully")
        connection.commit()
        connection.close()
# grade_adder("U2323911F")

grade_adder()