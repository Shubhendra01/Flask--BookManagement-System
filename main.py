import flask
from flask import Flask, render_template, request, redirect
import sqlite3
con = sqlite3.connect("bookmanagementsystem.db", check_same_thread= False)
cursor = con.cursor()
listOfTables = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='BOOKS' ").fetchall()
listOfTables1 = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='USERS' ").fetchall()
if listOfTables!=[]:
    print("Table Already Exists ! ")
else:
    con.execute(''' CREATE TABLE BOOKS(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            BOOKNAME TEXT,
                            AUTHOR TEXT,
                            CATEGORY TEXT,
                            PRICE INTEGER,
                            PUBLISHER TEXT,
                            PASSWORD TEXT); ''')

print("Book table has created")
if listOfTables1!=[]:
    print("Table Already Exists ! ")
else:
    con.execute(''' CREATE TABLE USERS(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            address TEXT,
                            email TEXT,
                            phone TEXT,
                            password TEXT); ''')

print("User table has created")

app = Flask(__name__)

@app.route("/")
def welcomepage():
    return render_template("base2.html")

@app.route("/login", methods=["GET","POST"])
def welcome():
    if request.method == "POST":
        getlogUsername = request.form["logusername"]
        getlogpassword = request.form["logpassword"]
        print(getlogUsername)
        print(getlogpassword)
        if getlogUsername == "admin" and getlogpassword == "9875":
            return redirect("/bookentry")
    return render_template("login.html")

@app.route("/user", methods=["GET","POST"])
def user():
    if request.method == "POST":
        getEmail = request.form["email"]
        getpass = request.form["pass"]
        print(getEmail)
        print(getpass)
        try:
            cursor.execute("SELECT * FROM USERS WHERE email='"+getEmail+"' AND password='"+getpass+"'")
            r = cursor.fetchall()
            print(r)
            if len(r) == 0:
                print("invalid user!")
            else:
                return redirect("/userview")

        except Exception as e:
            print(e)
    return render_template("user.html")

@app.route("/userregister", methods=["GET","POST"])
def userreg():
    if request.method == "POST":
        getName = request.form["name"]
        getAddress = request.form["address"]
        getEmail = request.form["email"]
        getPhone = request.form["phnnumber"]
        getPass = request.form["pwd"]
        getCfnpass = request.form["cfnpwd"]
        print(getName)
        print(getAddress)
        print(getEmail)
        print(getPhone)
        print(getPass)
        print(getCfnpass)
        try:
            if getPass == getCfnpass :
                cursor.execute("INSERT INTO USERS(name, address, email, phone, password) VALUES('"+getName+"','"+getAddress+"','"+getEmail+"','"+getPhone+"','"+getPass+"')")
                print("Successfully created.")
                con.commit()
            else:
                print("Password mismatch")
            # return redirect("/userview")
        except Exception as e:
            print(e)

    return render_template("userregister.html")

@app.route("/userview")
def userviewing():
    return render_template("userdash.html")

@app.route("/bookentry", methods=["GET","POST"])
def register():
    if request.method == "POST":
        getBookname = request.form["bookname"]
        getAuthor = request.form["author"]
        getCategory = request.form["category"]
        getPrice = request.form["price"]
        getPublisher = request.form["publisher"]
        getPassword = request.form["pwd"]
        print(getBookname)
        print(getAuthor)
        print(getCategory)
        print(getPrice)
        print(getPublisher)
        print(getPassword)
        try:
            con.execute("INSERT INTO BOOKS(BOOKNAME, AUTHOR, CATEGORY, PRICE, PUBLISHER, PASSWORD) VALUES('"+getBookname+"','"+getAuthor+"','"+getCategory+"','"+getPrice+"','"+getPublisher+"','"+getPassword+"')")
            print("Successfully inserted.")
            con.commit()
        except Exception as e:
            print(e)

    return render_template("bookentry.html")

@app.route("/booksearch", methods=["GET","POST"])
def search():
    if request.method == "POST":
        getBookname = request.form["bookname"]
        print(getBookname)
        try:
            cursor.execute("SELECT * FROM BOOKS WHERE BOOKNAME='"+getBookname+"'")
            print("Selected")
            q = cursor.fetchall()
            if len(q) == 0:
                print("Invalid name")
            else:
                print("Search successful")
                print(len(q))
                return render_template("booksearch.html", books=q, status=True)
        except Exception as e:
            print(e)

    return render_template("booksearch.html", books=[], Status=False)

@app.route("/usersearch", methods=["GET","POST"])
def userbooksearch():
    if request.method == "POST":
        getBookname = request.form["bookname"]
        print(getBookname)
        try:
            cursor.execute("SELECT * FROM BOOKS WHERE BOOKNAME='"+getBookname+"'")
            print("Selected")
            q = cursor.fetchall()
            if len(q) == 0:
                print("Invalid name")
            else:
                print("Search successful")
                print(len(q))
                return render_template("usersearch.html", books=q, status=True)
        except Exception as e:
            print(e)

    return render_template("usersearch.html", books=[], Status=False)


@app.route("/bookdelete", methods =['GET','POST'])
def delete():
    if request.method == "POST":
        getBookname = request.form['bookname']
        print(getBookname)
        try:
            con.execute("DELETE FROM BOOKS WHERE BOOKNAME='"+getBookname+"'")
            print("SUCCESSFULLY DELETED!")
            con.commit()
            return redirect("/viewallbook")
        except Exception as e:
            print(e)
    return flask.render_template("bookdelete.html")

@app.route("/bookupdate",methods=["GET","POST"])
def update():
    if request.method == "POST":
        getBookname = request.form["bookname"]
        print(getBookname)
        try:
            cursor.execute("SELECT * FROM BOOKS WHERE MOBILE="+getBookname)
            print("Selected a patient")
            r = cursor.fetchall()
            if len(r)==0:
                print("Invalid mobile number")
            else:
                print(len(r))
                return render_template("bookviewupdate.html", patients=r)
            return redirect("/bookviewupdate")
        except Exception as e:
            print(e)
    return render_template("bookupdate.html")

@app.route("/bookviewupdate", methods = ['GET','POST'])
def viewupdate():
    if request.method == "POST":
        getBookname = request.form["bookname"]
        getAuthor = request.form["author"]
        getCategory = request.form["category"]
        getPrice = request.form["price"]
        getPublisher = request.form["publisher"]
        getPassword = request.form["pwd"]
        getConformPassword = request.form["cfnpwd"]
        print(getBookname)
        print(getAuthor)
        print(getCategory)
        print(getPrice)
        print(getPublisher)
        print(getPassword)
        print(getConformPassword)
        try:
            con.execute("INSERT INTO BOOKS(BOOKNAME, AUTHOR, CATEGORY, PRICE, PUBLISHER, PASSWORD) VALUES('"+getBookname+"','"+getAuthor+"','"+getCategory+"','"+getPrice+"','"+getPublisher+"','"+getPassword+"')")
            print("Successfully inserted.")
            con.commit()
            return redirect('/viewallbook')
        except Exception as e:
            print(e)

    return render_template("bookviewupdate.html")

@app.route("/viewallbook")
def viewall():
    cursor.execute("SELECT * FROM BOOKS")
    r = cursor.fetchall()
    return render_template("viewallbook.html", books=r)

@app.route("/userbookview")
def userallbook():
    cursor.execute("SELECT * FROM BOOKS")
    r = cursor.fetchall()
    return render_template("userbookview.html", books=r)

if __name__=="__main__":
    app.run(debug=True)