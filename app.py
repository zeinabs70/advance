import flask
from books_operation import Book, Personnel , InventoryError , MustNumeric, IntegerError ,AlphaError ,IdError 

myapp = flask.Flask(__name__)

@myapp.route("/")
def index():
    return flask.render_template("index.html")

@myapp.route("/about")
def about():
    return flask.render_template("about.html")


#The commands of the book
@myapp.route("/newbook" , methods=["GET","POST"])
def newbook():
    if flask.request.method == "POST":
        book = dict(flask.request.form)
        try:
            Book(int(book["isbn"]),book["title"],book["auther"],float(book["price"]),int(book["pages"])\
                 , book["category"],book["publisher"],int(book["inventory"]))
        except(IdError):
            return flask.render_template("error.html", errortext ="isbn باید یک عدد منحصر به فرد باشد")
        except(ValueError):
            return flask.render_template("error.html", errortext ="صفحات باید یک مقدار صحیح باشند")
        except(MustNumeric):
            return flask.render_template("error.html", errortext = "قیمت باید فقط عدد باشد")
        except(IntegerError):
            return flask.render_template("error.html", errortext ="ISBN باید عددی 8 رقمی باشد" )
        except(AlphaError):
            return flask.render_template("error.html", errortext ="ناشر و نویسنده باید فقط حروف الفبا باشند")
        return flask.redirect("/bookslist") 
    return flask.render_template("newbook.html")

@myapp.route("/bookslist")
def bookslist():
    return flask.render_template("bookslist.html" ,bookslist=Book.show_all_book() )

@myapp.route("/deletebook", methods=["GET","POST"] )
def deletebook():
    if flask.request.method == "POST":
        book = dict(flask.request.form)
        try:
            Book.delete_book(book["isbn"])
            return flask.redirect("/bookslist")
        except(InventoryError):
            return flask.render_template("error.html", errortext ="این کتاب دارای موجودی است امکان حذف کتاب  وجود ندارد")
    elif flask.request.method == "GET":
        return flask.render_template("deletebook.html")
    
@myapp.route("/error")
def error():
    return flask.render_template("error.html")

@myapp.route("/search" , methods=["GET","POST"])
def search():
    if flask.request.method == "POST":
        sch = dict(flask.request.form)
        value = flask.request.form.get('search-type')
        books = Book.find_books(sch["search-query"], int(value))
        return flask.render_template("search.html", bookslist = books)
    return flask.render_template("search.html")


#The commands of the personnel
@myapp.route("/personelindex")
def personelindex():
    return flask.render_template("personelindex.html")

@myapp.route("/newpersonel" , methods=["GET","POST"])
def newpersonel():
    if flask.request.method == "POST":
        prs = dict(flask.request.form)
        try:
            Personnel(int(prs["prs_id"]),prs["name"],prs["family"],int(prs["tel"]),prs["user"],prs["password"])
        except(IdError):
            return flask.render_template("error.html", errortext ="کد پرسنلی باید یک عدد منحصر به فرد باشد")
        except(IntegerError):
            return flask.render_template("error.html", errortext = "کد پرسنلی باید عددی 5 رقمی باشد")
        except(AlphaError):
            return flask.render_template("error.html", errortext ="نام و نام خانوادگی باید فقط حروف الفبا باشند")
        return flask.redirect("personelindex")
    return flask.render_template("newpersonel.html")

@myapp.route("/personellist")
def personellist():
    return flask.render_template("personellist.html" ,prslist=Personnel.show_all_personnel() )

@myapp.route("/deletepersonel", methods=["GET","POST"])
def deletepersonel():
    if flask.request.method == "POST":
        PRS = dict(flask.request.form)
        Personnel.delete_personnel(PRS["prs_id"])
        return flask.redirect("/personellist")
    return flask.render_template("deletepersonel.html")

myapp.run(debug=True)