from tkinter import *
from tkinter import messagebox
import mysql.connector as sql

passKey = input('Please input the password for your database: ')
try:
    db = sql.connect(
                     host = 'localhost',
                     user = 'root',
                     passwd = passKey, 
                     )
    cur = db.cursor()
    cur.execute('create database Inventory')
    db = sql.connect(
                     host = 'localhost',
                     user = 'root',
                     passwd = passKey,
                     database = 'Inventory' 
                     )
    cur = db.cursor()
    cur.execute('create table pharma(\
                 ID int(3) Primary Key,\
                 Item_Name varchar(20) ,\
                 Item_Price float(5),\
                 Item_Quantity float(5),\
                 Item_Category varchar(20),\
                 Item_Discount float(5)\
                                )'
                
               )
    db.commit()

except:
    db = sql.connect(
                     host = 'localhost',
                     user = 'root',
                     passwd = passKey,
                     database = 'Inventory' 
                     )
    cur = db.cursor()
    pass


def get():
    name =nameTxtBox.get()
    price = priceTxtBox.get()
    quan = quanTxtBox.get()
    cat = catTxtBox.get()
    dis =disTxtBox.get()
    return name,price,quan,cat,dis


def clear():
            nameTxtBox.delete(0, END)
            priceTxtBox.delete(0, END)
            quanTxtBox.delete(0, END)
            catTxtBox.delete(0, END)
            disTxtBox.delete(0, END)


def insert(name,price,quan,cat,dis):
            nameTxtBox.insert(0, name)
            priceTxtBox.insert(0, str(price))
            quanTxtBox.insert(0, str(quan))
            catTxtBox.insert(0, cat)
            disTxtBox.insert(0, str(dis))


checker = ''
def checkValidity():
    global checker
    global db
    global cur
    cur.execute('select max(ID) from pharma')
    for x in cur:
        try:
                count = x[0] + 1
        except:
                count = 1  
    name,price,quan,cat,dis = get()
    try:
       cur.execute("insert into pharma values("+str(count)+",'"+name+"',"+str(price)+","+str(quan)+",'"+cat+"',"+str(dis)+")")
       db.rollback()
       checker = True
    except:
        checker = False
        messagebox.showinfo("Title", 
                            "Some of the fields are either entry or have wrong entries."
                            )


root = Tk()
root.title("Simple Pharmacy Managment System")
root.configure(width=1500,height=600,bg='DARK RED')

# Functions

 
def addItem():
    checkValidity()
    if checker == True:
        name,price,quan,cat,dis = get()
        clear()
        cur.execute('select max(ID) from pharma')
        for x in cur:
            try:
                count = x[0] + 1
            except:
                count = 1
        cur.execute("insert into pharma values("+str(count)+",'"+name+"',"+str(price)+","+str(quan)+",'"+cat+"',"+str(dis)+")")
        db.commit()
        messagebox.showinfo("Title", 
                            "The entry has been added."
                            )
def deleteItem():
    name = nameTxtBox.get()
    clear()
    cur.execute("Delete from pharma where Item_Name = '"+name+"'")
    db.commit()
    messagebox.showinfo("Title", 
                        "The entry has been deleted"
                        )

def firstItem():
    clear()
    cur.execute("select * from pharma\
                 where ID = ( select min(ID) from pharma)")
    for x in cur :
        l1 = x
    name  = l1[1]
    price = l1[2]
    quan  = l1[3]
    cat   = l1[4]
    dis   = l1[5]
    insert(name,price,quan,cat,dis)

def lastItem():
    clear()
    cur.execute("select * from pharma\
                 where ID = ( select max(ID) from pharma)")
    for x in cur :
       l1 = x
    name  = l1[1]
    price = l1[2]
    quan  = l1[3]
    cat   = l1[4]
    dis   = l1[5]
    insert(name,price,quan,cat,dis)
            
def nextItem():
    name = nameTxtBox.get()
    clear()
    q = "select * from pharma where Item_Name = '"+name+"'"
    cur.execute(q)
    n = name 
    for x in cur :
        l1 = x
    ID = str(l1[0] + 1)
    c = 0
    while n == name :
        q = "select * from pharma where ID = '"+ID+"'"
        cur.execute(q)
        for x in cur :
            l1 = []
            l1 = x
        n     = l1[1]
        ID = str(eval(ID) + 1)
        c +=1
        if c == 20:
            messagebox.showinfo("Title", 
                            "No more records"
                            )
            break
    c = 0        
    price = l1[2]
    quan  = l1[3]
    cat   = l1[4]
    dis   = l1[5]
    insert(n,price,quan,cat,dis)


def previousItem():
    name = nameTxtBox.get()
    clear()
    q = "select * from pharma where Item_Name = '"+name+"'"
    cur.execute(q)
    n = name 
    for x in cur :
        l1 = x
    ID = str(l1[0] - 1)
    c = 0
    while n == name :
        q = "select * from pharma where ID = '"+ID+"'"
        cur.execute(q)
        for x in cur :
            l1 = []
            l1 = x
        n     = l1[1]
        ID = str(eval(ID) - 1)
        c +=1
        if c == 20:
            messagebox.showinfo("Title", 
                            "No more records "
                            )
            break
    c = 0        
    price = l1[2]
    quan  = l1[3]
    cat   = l1[4]
    dis   = l1[5]
    insert(n,price,quan,cat,dis)

def updateItem():
    checkValidity()
    if checker == True:
        name,price,quan,cat,dis = get()
        cur.execute("select * from pharma where Item_Name = '"+name+"'")
        a = 0
        for x in cur:
            if x != []:
                clear()
                def up(name,v,x):
                    global cur
                    global db
                    if v.isalpha() != True:
                        cur.execute("update pharma set "+x+" ="+str(v)+" where Item_Name = '"+name+"'")
                    else:
                        cur.execute("update pharma set "+x+" = '"+v+"' where Item_Name = '"+name+"'")
                    a = 1
                    db.commit()
                up(name,price,x = 'Item_Price')
                up(name,quan,x = 'Item_Quantity')
                up(name,cat,x = 'Item_Category')
                up(name,dis,x = 'Item_Discount')
                messagebox.showinfo("Title", 
                            "Record has been updated "
                            )

def searchItem():
    try:
        name = nameTxtBox.get()
        clear()
        q = "select * from pharma where Item_Name = '"+name+"'"
        cur.execute(q)
        for x in cur :
            l1 = x
        name  = l1[1]
        price = l1[2]
        quan  = l1[3]
        cat   = l1[4]
        dis   = l1[5]
        insert(name,price,quan,cat,dis)
    except:
        clear()
        messagebox.showinfo("Title", 
                            "Record - "+name+"\n Does not exist"
                            )

def clearItem():
    clear()

def exitProgram():
    qsn = messagebox.askyesno('Title','Do You Want to quit ?')
    if qsn == True:
        root.destroy()
                  

# Labels

headLab= Label(
              root,
              text="DP PHARMACY",
              bg="black",
              fg="white",
              font=("Times", 30)
             )

nameLab=Label(
             root,
             text="ENTER ITEM NAME",
             bg="black",
             relief="ridge",
             fg="white",
             font=("Times", 12),
             width=25
            )

priceLab=Label(
             root,
             text="ENTER ITEM PRICE",
             bd="2",
             relief="ridge",
             height="1",
             bg="black",
             fg="white",
             font=("Times", 12),
             width=25
            )

quanLab=Label(
             root,
             text="ENTER ITEM QUANTITY",
             bd="2",
             relief="ridge",
             bg="black",
             fg="white",
             font=("Times", 12),
             width=25
            )

catLab=Label(
             root,
             text="ENTER ITEM CATEGORY",
             bd="2",
             relief="ridge",
             bg="black",
             fg="white",
             font=("Times", 12),
             width=25
            )

discLab=Label(
             root,
             text="ENTER ITEM DISCOUNT",
             bg="black",
             relief="ridge",
             fg="white",
             font=("Times", 12),width=25
            )

# Textboxes

nameTxtBox=Entry(
              root ,
              font=("Times", 14)
             )

priceTxtBox= Entry(
                root,
                font=("Times", 14)
               )

quanTxtBox= Entry(
               root,
               font=("Times", 14)
              )

catTxtBox= Entry(
              root,
              font=("Times", 14)
             )

disTxtBox= Entry(
              root,
              font=("Times", 14)
             )
# Buttons

addBut = Button(
                root,
                text="ADD ITEM",
                bg="black",
                fg="white",
                width=20,
                font=("Times", 12),
                command=addItem
               )

delBut = Button(
                root,
                text="DELETE ITEM",
                bg="black",
                fg="white",
                width =20,
                font=("Times", 12),
                command=deleteItem
               )

vFirBut = Button(
                root,
                text="VIEW FIRST ITEM" ,
                bg="black",
                fg="white",
                width =20,
                font=("Times", 12),
                command=firstItem
               )

vNexBut = Button(
                root,
                text="VIEW NEXT ITEM" ,
                bg="black",
                fg="white",
                width =20,
                font=("Times", 12),
                command=nextItem
               )

vPreBut = Button(
                root,
                text="VIEW PREVIOUS ITEM",
                bg="black",
                fg="white",
                width =20,
                font=("Times", 12),
                command=previousItem
               )

vLasBut = Button(
                root,
                text="VIEW LAST ITEM",
                bg="black",
                fg="white",
                width =20,
                font=("Times", 12),
                command=lastItem
               )

upBut = Button(
                root,
                text="UPDATE ITEM",
                bg="black",
                fg="white",
                width =20,
                font=("Times", 12),
                command=updateItem
               )

serBut = Button(
                root,
                text="SEARCH ITEM",
                bg="black",
                fg="white",
                width =20,
                font=("Times", 12),
                command=searchItem
               )

clsBut = Button(
                root,
                text="CLEAR SCREEN",
                bg="black",
                fg="white",
                width=20,
                font=("Times", 12),
                command=clearItem
               )

exiBut = Button(
                root,
                text="EXIT",
                bg="black",
                fg="white",
                width=20,
                font=("Times", 12),
                command=exitProgram
               )
# Label layout

headLab.grid(
            columnspan=6,
            padx=10,
            pady=10
           )

nameLab.grid(
            row=2,
            column=0,
            sticky=W,
            padx=10,
            pady=10
           )

priceLab.grid(
            row=4,
            column=0,
            sticky=W,
            padx=10,
            pady=10
           )

quanLab.grid(
            row=6,
            column=0,
            sticky=W,
            padx=10,
            pady=10
           )

catLab.grid(
            row=8,
            column=0,
            sticky=W,
            padx=10,
            pady=10
           )

discLab.grid(
            row=10,
            column=0,
            sticky=W,
            padx=10,
            pady=10
           )

# Textbox layout

nameTxtBox.grid(
             row=2,
             column=1,
             padx=40,
             pady=10
            )

priceTxtBox.grid(
              row=4,
              column=1,
              padx=10,
              pady=10
             )

quanTxtBox.grid(
             row=6,
             column=1,
             padx=10,
             pady=10
            )

catTxtBox.grid(
            row=8,
            column=1,
            padx=10,
            pady=10
           )

disTxtBox.grid(
            row=10,
            column=1,
            padx=10,
            pady=10
           )

# Button layout

addBut.grid(
             row=2,
             column=4,
             padx=40,
             pady=10
            )

delBut.grid(
             row=2,
             column=5,
             padx=40,
             pady=10
            )

vFirBut.grid(
             row=4,
             column=4,
             padx=40,
             pady=10
            )

vNexBut.grid(
             row=4,
             column=5,
             padx=40,
             pady=10
            )

vPreBut.grid(
             row=6,
             column=4,
             padx=40,
             pady=10
            )

vLasBut.grid(
             row=6,
             column=5,
             padx=40,
             pady=10
            )

upBut.grid(
             row=8,
             column=4,
             padx=40,
             pady=10
            )

serBut.grid(
             row=8,
             column=5,
             padx=40,
             pady=10
            )

clsBut.grid(
             row=10,
             column=4,
             padx=40,
             pady=10
            )

exiBut.grid(
             row=10,
             column=5,
             padx=40,
             pady=10
            )

root.mainloop()
