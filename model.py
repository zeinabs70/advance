import sqlite3
from sys import path

class InventoryError(Exception):
    pass
class IdError(Exception):
    pass

#The commands of the books table 
def create_Book_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS book_table(isbn INTEGER PRIMARY KEY,title TEXT \
                    ,auther TEXT ,price FLOAT ,pages INTEGER ,category TEXT,publishr TEXT \
                    ,inventory INTEGER ) ")
    
def new_book(*book):
    try:
        cursor.execute("INSERT INTO book_table VALUES(?,?,?,?,?,?,?,?)" , book)
        database.commit()
    except(sqlite3.IntegrityError):
        raise IdError("isbn must be a unique 8 digit number ")
    
def list_all_book():
    return list(cursor.execute("SELECT * FROM book_table"))

def find_book( search_option , value ):
    if value == 1 :#daghighan ebarat dakhel ro peida mikone
       book = cursor.execute("SELECT * FROM book_table WHERE isbn= ?" , [search_option]).fetchall() 
    elif value == 2 :#tamame fieldhaie moshabehe ebarat search shode ra peida mikonad
       book = cursor.execute(f"SELECT * FROM book_table WHERE title like '%{search_option}%' ").fetchall() 
    elif value == 3 :
       book = cursor.execute(f"SELECT * FROM book_table WHERE auther like '%{search_option}%' " ).fetchall()
    else:
       book = cursor.execute(f"SELECT * FROM book_table WHERE publishr like '%{search_option}%' ").fetchall()
    return book

def delete_book(isbn):
    book = cursor.execute("SELECT * FROM book_table WHERE isbn= ?" , [isbn]).fetchone()
    if book[7] != 0 : #check mikone anbar mojodi darad 
        raise InventoryError("این کتاب دارای موجودی است امکان حذف کتاب  وجود ندارد!!")
    else:
        cursor.execute("DELETE FROM book_table WHERE isbn=?", [isbn])
        database.commit()
       

def book_count():
    list_isbn = list(cursor.execute("SELECT isbn FROM book_table"))
    c=0
    for count in list_isbn:
        c+=1
    return c


#The commands of the personnel table
def create_Personnel_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS personnel_table(prs_id INTEGER PRIMARY KEY, name TEXT \
                    ,family TEXT ,tel INTEGER ,user TEXT ,password TEXT )")
    
def new_personnel(*personnel):
    try:
        cursor.execute("INSERT INTO personnel_table VALUES(?,?,?,?,?,?)" , personnel)
        database.commit()
    except(sqlite3.IntegrityError):
        raise IdError("prs_id must be a unique 5 digit number")


def list_all_personnel():
    return list(cursor.execute("SELECT * FROM personnel_table"))

def delete_personnel(id):
    cursor.execute("DELETE FROM personnel_table WHERE prs_id=?", [id])
    database.commit()

def Credit_check(user , password):
    pw = cursor.execute("SELECT password FROM personnel_table WHERE user = ?",[user])
    if pw == None :
        raise ValueError("  !! این نام کاربری تعریف نشده است")
    elif pw == password:
        return True
    else:
        raise ValueError("رمز عبور اشتباه است!! ")
    
#The commands of the customer table
def create_Customer_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS customer_table(cst_id INTEGER PRIMARY KEY,name TEXT \
                    ,family TEXT ,tel INTEGER ) ")

def new_customer(*customer):
    cursor.execute("INSERT INTO customer_table VALUES(?,?,?,?)" , customer)
    database.commit()

def list_all_customer():
    return list(cursor.execute("SELECT * FROM customer_table"))

def delete_customer(id):
    cursor.execute("DELETE FROM customer_table WHERE cst_id=?", [id])
    database.commit()

#---------------------MAIN--------------------------
database = sqlite3.connect(path[0] + "/model_db.db" , check_same_thread= False)
cursor = database.cursor()
create_Book_table()
create_Personnel_table()
create_Customer_table()
