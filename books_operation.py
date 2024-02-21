import model
from flask import request 

class InventoryError(Exception):
    pass

class MustNumeric(Exception):
    pass

class IntegerError(Exception):
    pass

class AlphaError(Exception):
    pass

class IdError(Exception):
    pass

def login(func):
    def wrapper(*args, **kwargs):
        username = request.form.get('username')
        password = request.form.get('password')
        if model.Credit_check(username , password) == True:
            func(*args, **kwargs)
        else:
            raise ValueError("نام کاربری یا رمز عبور اشتباه است")
    return wrapper

#in class har att ro az har class migire va check mikone ke faghat horof alefba bashad 
class AlphaProperty:
    def __set_name__(self, owner ,name):
        self.name = name

    def __get__(self, instance):
        if instance is None:
            return self
        return getattr(instance, "_" + self.name)

    def __set__(self, instance, value):
                if is_farsi_alpha(value) == False:
                   raise AlphaError(f"{self.name} must contain only alphabetic characters.")
                setattr(instance, "_" + self.name, value)

def is_farsi_alpha(text):
    for char in text:
        if not ('\u0600' <= char <= '\u06FF'):  #shomare codehaye horof farsi
            return False
    return True


class Book:
    Material = "paper"
    count = model.book_count()  # tedad ketabhaye mojod dar database

    def __init__(self,ISBN,title,auther,price,pages,category,publisher,inventory=1):
        self.isbn = ISBN
        self.title = title
        self.auther = auther
        self.price = price
        self.pages = pages
        self.category = category
        self.publisher = publisher
        self.inventory = inventory 
        auther = AlphaProperty()
        publisher = AlphaProperty()
        try:
            model.new_book(self.isbn, self.title, self.auther, self.price, self.pages, self.category,\
                        self.publisher, self.inventory)
            Book.count +=1
        except(model.IdError):
            raise IdError("isbn باید یک عدد 8 رقمی منحصر به فرد باشد")

    # check kardan tedad argham isbn
    @property
    def isbn(self):
        return self._isbn
    @isbn.setter
    def isbn(self,value):
        if len(str(value)) == 8 :
            self._isbn = value
        else:
            raise IntegerError("ISBN باید عددی 8 رقمی باشد")

    # check kardan gheimat: adad ya ashar bashad
    @property
    def price(self):
        return self._price
    @price.setter
    def price(self, value):
        if not str(value).isdigit() and not isinstance(value, float):
            raise MustNumeric("قیمت باید فقط عدد باشد")
        self._price = value

    # check kardan safhe: adad bashad
    @property
    def pages(self):
        return self._pages
    @pages.setter
    def pages(self, value):
        if not str(value).isdigit():
            raise ValueError("صفحات باید یک مقدار صحیح باشند.")
        self._pages = value

    # list ketabha
    @staticmethod
    def show_all_book() :
        return model.list_all_book()  

    @staticmethod
    def delete_book(isbn):
        try:
            return model.delete_book(isbn)
        except:
            raise InventoryError("این کتاب دارای موجودی است امکان حذف کتاب  وجود ندارد")

    @staticmethod
    def find_books(search_option , value=2):
        books = model.find_book(search_option ,value )
        return books


    @classmethod
    def books_count(cls):
        return cls.count

class Person:
    store = "ketabkhan"
    def __init__(self , name , family , tel  ):
        self.name = name
        self.family = family
        self.tel = tel
        

class Personnel(Person):
    
    def __init__(self,prs_id , name, family, tel, user , password ):
        super().__init__(name, family, tel)
        self.prs_id = prs_id
        self.user = user
        self.password = password
        name = AlphaProperty()
        family = AlphaProperty()
        try:
            model.new_personnel(self.prs_id, self.name, self.family, self.tel, self.user, self.password)
        except(model.IdError):
            raise IdError("کد پرسنلی باید یک عدد 5 رقمی منحصر به فرد باشد")

    @property
    def prs_id(self):
        return self._prs_id
    @prs_id.setter
    def prs_id(self,value):
        if len(str(value)) == 5 :
            self._prs_id = value
        else:
            raise IntegerError("کد پرسنلی باید عددی 5 رقمی باشد")

    @staticmethod
    def show_all_personnel():
        return model.list_all_personnel()
    
    @staticmethod
    def delete_personnel(prs_id):
        model.delete_personnel(prs_id)


class Customer(Person):
    def __init__(self,cst_id, name, family, tel):
        super().__init__(name, family, tel)
        self.cst_id = cst_id
        model.new_customer(self.cst_id, self.name, self.family, self.tel)

    @staticmethod
    def show_all_customer():
        return model.list_all_customer()
    
    @staticmethod
    def delete_customer(cst_id):
        model.delete_customer(cst_id)

#-----------------------main------------------------------
# book1 = Book(12312348,"اثر مرکب","دارن هاردی",97000,210,"موفقیت","سپید",12)
# personnel1 = Personnel(12348,"مینا","کریمی",9133332660,"کاربر1",123480)
# customer1 = Customer(98766,"سارا","حمیدی",9133038794)
# print(Book.show_all_book())
# print(Personnel.show_all_personnel())
# print(Customer.show_all_customer())
# # Book.delete_book(12312347)
# # print(Book.books_count())
# print(Book.find_books("اثر" , 2))
# print(Book.delete_book(12312347))