Hi guys welcome to the github of the student score management, our final project for CV1014

before you begin be sure to download these things
https://www.atlassian.com/git/tutorials/install-git - follow this tutorial and download git from this page. without git, you would not be able to reflect your code on the main website
https://sqlitebrowser.org/ - this is an app that allows you to see .db files. .db stands for database, and as the name implies, stores all information related to this project

About git:
tbc.

About sqlite3:
You all do not need to care about database, i have created helper functions so that you can pull out information without interacting with sqlite
these functions are:
get_records(database,id,,datatype): This allows you to select specifc database and id(This is very important as id is basically the "key" to all tables.)
datatype allows you to filter specifc data you want. for student_particulars(table) it goes like(type in the integer) 0. print out everything 1. name  2.semester 3.school 4.major 5.student_or_teacher(you most likely wont need this)
for 0 it will be in the form of a tuple which is a list whose elements are immutable e.g (1,2,3,4) you can never change the values inside the tuple
get_records_all(not yet implemented) you will most likely be using it for sorting, which one of you will do. it will theroetically, from the table(grades)
filter out a specific subject and the grades for all the student in it. or it can filter things based on semester as well.
