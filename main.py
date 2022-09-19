import tkinter as tk
import customtkinter
import mysql.connector

# Connects to database
# ENTER YOUR CONNECTION INFORMATION HERE
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="supermarket"
)

# Access Database
mycursor = db.cursor()

# Sets up the GUI window
window = customtkinter.CTk()
window.geometry('900x700')
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)
window.resizable(False, False)

# GUI Related Variables
tv1 = tk.StringVar()
tv2 = tk.StringVar()
tv3 = tk.StringVar()
tv4 = tk.StringVar()
tv5 = tk.StringVar()
tv6 = tk.StringVar()
tv7 = tk.StringVar()
tv8 = tk.StringVar()
tv9 = tk.StringVar()
tv10 = tk.StringVar()
tv11 = tk.StringVar()
tv12 = tk.StringVar()
tv13 = tk.StringVar()
tv14 = tk.StringVar()
tv15 = tk.StringVar()
tv16 = tk.StringVar()
textVariables = [tv1, tv2, tv3, tv4, tv5, tv6, tv7, tv8, tv9, tv10, tv11, tv12, tv13, tv14, tv15, tv16]
toDelete = tk.StringVar()
managerView = False
customerView = False
empDel = False
itemDel = False
custDel = False
supDel = False
rowHeight = 0
tvi = 0


# Handles switching to the correct page
def switch_page(frame):
    frame.tkraise()


# Functions for the GUI
# Sign-in handler function
def sign_in():
    global managerView, customerView
    empID = siEntry1.get()
    empSSN = siEntry2.get()
    mycursor.execute(
        "SELECT fname FROM employee INNER JOIN department WHERE ID = " + empID + " AND SSN = '" + empSSN + "' AND SSN = MgrSSN")
    Name = None
    for x in mycursor:
        Name = x
    if Name == None:
        mycursor.execute("SELECT fname FROM employee WHERE ID = " + empID + " AND SSN = '" + empSSN + "'")
        for x in mycursor:
            Name = x
        if Name == None:
            mycursor.execute("SELECT CFName FROM customer WHERE CustomerID = " + empID + " AND CPhoneNumber = '" + empSSN + "'")
            for x in mycursor:
                Name = x
            if Name == None:
                errorLabel.config(text="Incorrect ID or SSN")
            else:
                # Load customer page
                errorLabel.config(text="")
                managerView = False
                customerView = True
                switch_page(custViewFrame)
        else:
            # Load employee page
            errorLabel.config(text="")
            managerView = False
            customerView = False
            switch_page(employeeViewFrame)
    else:
        # Load manager page
        errorLabel.config(text="")
        managerView = True
        customerView = False
        switch_page(managerViewFrame)


# Handles signing out of the GUI
def sign_out():
    siEntry1.delete(0, 'end')
    siEntry2.delete(0, 'end')
    switch_page(signInFrame)


# Gets information from database
def info(type):
    if type == "employee":
        attributes = ['ID', 'SSN', 'Fname', 'Lname', 'Email', 'Phone_Number', 'EmergencyContactNumber', 'DepartmentNumber', 'Address', 'Salary']
        for x,y in zip(attributes, range(0, 10)):
            if managerView:
                mycursor.execute("SELECT " + x + " FROM employee WHERE ID = " + mvEntry1.get())
            else:
                mycursor.execute("SELECT " + x + " FROM employee WHERE ID = " + siEntry1.get())
            for x in mycursor:
                textVariables[y].set(x)
        switch_page(employeeInfoFrame)
    elif type == "item":
        attributes = ['ItemID', 'Price', 'ItemName', 'SupplierID', 'ItemCount']
        for x, y in zip(attributes, range(0, 5)):
            mycursor.execute("SELECT " + x + " FROM inventory WHERE ItemID = " + mvEntry2.get())
            for x in mycursor:
                textVariables[y].set(x)
        switch_page(itemInfoFrame)
    elif type == "customer":
        attributes = ['CustomerID', 'CFName', 'CLName', 'Points', 'CEmail', 'CPhoneNumber', 'CAddress']
        for x, y in zip(attributes, range(0, 7)):
            if managerView:
                mycursor.execute("SELECT " + x + " FROM customer WHERE CustomerID = " + mvEntry3.get())
            else:
                mycursor.execute("SELECT " + x + " FROM customer WHERE CustomerID = " + siEntry1.get())
            for x in mycursor:
                textVariables[y].set(x)
        switch_page(custInfoFrame)
    elif type == "department":
        attributes = ['DepartmentID', 'DepartmentName', 'DepartmentPhoneNumber']
        for x, y in zip(attributes, range(0, 3)):
            mycursor.execute("SELECT " + x + " FROM department WHERE DepartmentID = (SELECT DepartmentNumber FROM employee WHERE ID = " + siEntry1.get() +") ")
            for x in mycursor:
                textVariables[y].set(x)
        mycursor.execute("SELECT Fname FROM employee INNER JOIN department WHERE DepartmentNumber = (SELECT DepartmentNumber FROM employee WHERE ID = " + siEntry1.get() + ") AND ID = MgrId")
        for x in mycursor:
            Fname = x
        mycursor.execute("SELECT Lname FROM employee INNER JOIN department WHERE DepartmentNumber = (SELECT DepartmentNumber FROM employee WHERE ID = " + siEntry1.get() + ") AND ID = MgrId")
        for x in mycursor:
            Lname = x
        Lname = ''.join(filter(str.isalpha, str(Lname)))
        Fname = ''.join(filter(str.isalpha, str(Fname)))
        textVariables[3].set(Fname + " " + Lname)
        switch_page(deptInfoFrame)


# Deletes a row in the database
def delete(type):
    global empDel, itemDel, supDel, custDel
    empDel, itemDel, supDel, custDel = False, False, False, False
    if type == "employee":
        empDel = True
        mycursor.execute("SELECT Fname FROM employee WHERE ID = " + mvEntry1.get())
        for x in mycursor:
            Fname = x
        mycursor.execute("SELECT Lname FROM employee WHERE ID = " + mvEntry1.get())
        for x in mycursor:
            Lname = x
        Lname = ''.join(filter(str.isalpha, str(Lname)))
        Fname = ''.join(filter(str.isalpha, str(Fname)))
        toDelete.set("Are you sure you want to delete " + Fname + " " + Lname + "? ID number: " + mvEntry1.get())
    elif type == "item":
        itemDel = True
        mycursor.execute("SELECT ItemName FROM inventory WHERE ItemID = " + mvEntry2.get())
        for x in mycursor:
            name = x
        name = ''.join(filter(str.isalpha, str(name)))
        toDelete.set("Are you sure you want to delete " + name + "? ItemID number: " + mvEntry2.get())
    elif type == "customer":
        custDel = True
        if managerView:
            mycursor.execute("SELECT CFname FROM customer WHERE CustomerID = " + mvEntry3.get())
            for x in mycursor:
                Fname = x
            mycursor.execute("SELECT CLname FROM customer WHERE CustomerID = " + mvEntry3.get())
            for x in mycursor:
                Lname = x
            Lname = ''.join(filter(str.isalpha, str(Lname)))
            Fname = ''.join(filter(str.isalpha, str(Fname)))
            toDelete.set("Are you sure you want to delete " + Fname + " " + Lname + "? ID number: " + mvEntry3.get())
        else:
            toDelete.set("Are you sure you want to delete your account")
    switch_page(deleteFrame)


# Confirms that we want to delete
def confirm_delete():
    global empDel, itemDel, supDel, custDel
    if empDel:
        mycursor.execute("DELETE FROM employee WHERE ID = " + mvEntry1.get())
    elif itemDel:
        mycursor.execute("DELETE FROM inventory WHERE ItemID = " + mvEntry2.get())
    elif custDel and managerView:
        mycursor.execute("DELETE FROM customer WHERE CustomerID = " + mvEntry3.get())
    elif custDel and not managerView:
        mycursor.execute("DELETE FROM customer WHERE CustomerID = " + siEntry1.get())
    db.commit()
    if managerView:
        switch_page(managerViewFrame)
    else:
        switch_page(signInFrame)


# Edits a row in the database
def edit(type):
    global managerView
    entries = []
    update = ''
    if type == "employee":
        entries = [eeEntry1, eeEntry2, eeEntry3, eeEntry4, eeEntry5, eeEntry6, eeEntry7, eeEntry8, eeEntry9]
        attributes = [' SSN', ' Fname', ' Lname', ' Email', ' Phone_number', ' EmergencyContactNumber', 'ZDepartmentNumber', ' Address', 'ZSalary']
        update = "UPDATE employee SET"
        for x, y in zip(entries, range(0, 9)):
            if x.get() != '':
                if attributes[y].startswith('Z'):
                    attributes[y] = attributes[y].replace("Z", " ", 1)
                    update += attributes[y] + " = " + x.get() + ","
                else:
                    update += attributes[y] + " = '" + x.get() + "',"
        update = update.rstrip(update[-1])
        if managerView:
            update += " WHERE ID = " + mvEntry1.get()
        else:
            update += " WHERE ID = " + siEntry1.get()

    elif type == "item":
        entries = [eiEntry1, eiEntry2, eiEntry3, eiEntry4]
        attributes = ['ZPrice', ' ItemName', 'ZSupplierID', 'ZItemCount']
        update = "UPDATE inventory SET"
        for x, y in zip(entries, range(0,4)):
            if x.get() != '':
                if attributes[y].startswith('Z'):
                    attributes[y] = attributes[y].replace("Z", " ", 1)
                    update += attributes[y] + " = " + x.get() + ","
                else:
                    update += attributes[y] + " = '" + x.get() + "',"
        update = update.rstrip(update[-1])
        update += " WHERE ItemID = " + mvEntry2.get()

    elif type == "customer":
        entries = [ecEntry1, ecEntry2, ecEntry3, ecEntry4, ecEntry5, ecEntry6]
        attributes = [' CFName', ' CLName', 'ZPoints', ' CEmail', ' CPhoneNumber', ' CAddress']
        update = "UPDATE customer SET"
        for x, y in zip(entries, range(0,6)):
            if x.get() != '':
                if attributes[y].startswith('Z'):
                    attributes[y] = attributes[y].replace("Z", " ", 1)
                    update += attributes[y] + " = " + x.get() + ","
                else:
                    update += attributes[y] + " = '" + x.get() + "',"
        update = update.rstrip(update[-1])
        update += " WHERE CustomerID = " + mvEntry3.get()

    elif type == "customerView":
        entries = [ecvEntry1, ecvEntry2, ecvEntry4, ecvEntry5, ecvEntry6]
        attributes = [' CFName', ' CLName', ' CEmail', ' CPhoneNumber', ' CAddress']
        update = "UPDATE customer SET"
        for x, y in zip(entries, range(0,5)):
            if x.get() != '':
                if attributes[y].startswith('Z'):
                    attributes[y] = attributes[y].replace("Z", " ", 1)
                    update += attributes[y] + " = " + x.get() + ","
                else:
                    update += attributes[y] + " = '" + x.get() + "',"
        update = update.rstrip(update[-1])
        update += " WHERE CustomerID = " + siEntry1.get()

    mycursor.execute(update)
    db.commit()
    for each in entries:
        each.delete(0, 'end')
    back()


# adds a new row to database
def add(type):
    entries = []
    if type == "employee":
        entries = [aeEntry1, aeEntry2, aeEntry3, aeEntry4, aeEntry5, aeEntry6, aeEntry7, aeEntry8, aeEntry9]
        mycursor.execute("INSERT INTO employee (ID, SSN, Fname, Lname, Email, Phone_Number, "
                         "EmergencyContactNumber, DepartmentNumber, Address, Salary) VALUES (null, '" +
                         aeEntry1.get() + "', '" + aeEntry2.get() + "', '" + aeEntry3.get() + "', '" + aeEntry4.get() +
                         "', '" + aeEntry5.get() + "', '" + aeEntry6.get() + "', " + aeEntry7.get() + ", '" + aeEntry8.get() + "', " + aeEntry9.get() +")")
    elif type == "item":
        entries = [aiEntry1, aiEntry2, aiEntry3, aiEntry4]
        mycursor.execute("INSERT INTO inventory (ItemID, Price, ItemName, SupplierID, ItemCount) VALUES (null, " +
                         aiEntry1.get() + ", '" + aiEntry2.get() + "', " + aiEntry3.get() + ", " + aiEntry4.get() + ")")
    elif type == "customer":
        entries = [aeEntry1, aeEntry2, aeEntry3, aeEntry4, aeEntry5, aeEntry6]
        mycursor.execute("INSERT INTO customer (CustomerID, CFName, CLName, Points, CEmail, CPhoneNumber, "
                         "CAddress) VALUES (null, '" + acEntry1.get() + "', '" + acEntry2.get() + "', '" + acEntry3.get() + "', '" + acEntry4.get() +
                         "', '" + acEntry5.get() + "', '" + acEntry6.get() + "')")
    db.commit()
    for each in entries:
        each.delete(0, 'end')
    switch_page(managerViewFrame)


# goes back to main menu
def back():
    if managerView:
        switch_page(managerViewFrame)
    elif customerView:
        switch_page(custViewFrame)
    else:
        switch_page(employeeViewFrame)


# places order for more inventory
def place_order():
    global textVariables, rowHeight, tvi
    rowHeight = 160
    entries = [oiEntry1, oiEntry3, oiEntry5, oiEntry7]
    quantities = [oiEntry2, oiEntry4, oiEntry6, oiEntry8]
    for i in range(len(entries)):
        if entries[i].get() != '':
            id = entries[i].get()
            quan = quantities[i].get()
            mycursor.execute("SELECT ItemName FROM inventory WHERE ItemID = " + id)
            for x in mycursor:
                textVariables[tvi*4].set(x)
                textVariables[tvi*4+1].set(quan)
            mycursor.execute("SELECT SupplierName FROM supplier S INNER JOIN inventory I WHERE I.ItemID = " + id + " AND I.SupplierID = S.SupplierID")
            for x in mycursor:
                textVariables[tvi*4+2].set(x)
            mycursor.execute("SELECT Price FROM inventory WHERE ItemID = " + id)
            for x in mycursor:
                price = float(''.join(str(elem) for elem in x))
            price = "{:.2f}".format((price/2) * float(quan))
            textVariables[tvi*4+3].set("$" + str(price))
            order()
            rowHeight += 45
            tvi += 1
    switch_page(confOrderFrame)
    rowHeight = 0
    tvi = 0


def order():
    global textVariables, rowHeight, tvi
    oLabel1 = customtkinter.CTkLabel(confOrderFrame, textvariable=textVariables[tvi*4], width=32, text_font=("Calibri", 14))
    oLabel1.place(x=80, y=rowHeight)
    oLabel2 = customtkinter.CTkLabel(confOrderFrame, textvariable=textVariables[tvi*4+1], width=32, text_font=("Calibri", 14))
    oLabel2.place(x=280, y=rowHeight)
    oLabel3 = customtkinter.CTkLabel(confOrderFrame, textvariable=textVariables[tvi*4+2], width=32, text_font=("Calibri", 14))
    oLabel3.place(x=480, y=rowHeight)
    oLabel4 = customtkinter.CTkLabel(confOrderFrame, textvariable=textVariables[tvi*4+3], width=32, text_font=("Calibri", 14))
    oLabel4.place(x=680, y=rowHeight)


def conf_order():
    global textVariables
    entries = [oiEntry1, oiEntry3, oiEntry5, oiEntry7]
    quantities = [oiEntry2, oiEntry4, oiEntry6, oiEntry8]
    for tv in textVariables:
        tv.set('')
    for i in range(len(entries)):
        if entries[i].get() != '':
            mycursor.execute("SELECT SupplierID FROM inventory WHERE ItemID = " + entries[i].get())
            for x in mycursor:
                supplierID = str(''.join(str(elem) for elem in x))
            mycursor.execute("INSERT INTO supplies (SupplierID, ItemID, OrderAmount) VALUES (" +
                             supplierID + ", " + entries[i].get() + ", " + quantities[i].get() + ")")
            db.commit()
    for each in entries:
        each.delete(0, 'end')
    for each in quantities:
        each.delete(0, 'end')
    switch_page(managerViewFrame)


# Gets entire tables
def all(type, frame):
    global rowHeight
    for widget in frame.winfo_children():
        widget.destroy()
    create(frame)
    infoList = []
    if type == "orders":
        mycursor.execute("SELECT * FROM supplies ORDER BY SupplierID")
        for x in mycursor:
            infoList.append(list(x))
        rowHeight = 110
        for itemList in infoList:
            rowHeight += 25
            orderAllLabel1 = customtkinter.CTkLabel(allOrderFrame, text=itemList[0], width=32, text_font=("Calibri", 14))
            orderAllLabel1.place(x=80, y=rowHeight)
            orderAllLabel2 = customtkinter.CTkLabel(allOrderFrame, text=itemList[1], width=32, text_font=("Calibri", 14))
            orderAllLabel2.place(x=280, y=rowHeight)
            mycursor.execute("SELECT ItemName FROM inventory WHERE ItemID = " + str(itemList[1]))
            for x in mycursor:
                txt = str(''.join(str(elem) for elem in x))
            orderAllLabel3 = customtkinter.CTkLabel(allOrderFrame, text=txt, width=32, text_font=("Calibri", 14))
            orderAllLabel3.place(x=480, y=rowHeight)
            orderAllLabel4 = customtkinter.CTkLabel(allOrderFrame, text=itemList[2], width=32, text_font=("Calibri", 14))
            orderAllLabel4.place(x=680, y=rowHeight)
        switch_page(allOrderFrame)
    if type == "employee":
        mycursor.execute("SELECT * FROM employee ORDER BY Lname")
        for x in mycursor:
            infoList.append(list(x))
        rowHeight = 110
        for itemList in infoList:
            rowHeight += 25
            empAllLabel1 = customtkinter.CTkLabel(allEmployeeFrame, text=itemList[0], width=32, text_font=("Calibri", 14))
            empAllLabel1.place(x=50, y=rowHeight)
            empAllLabel2 = customtkinter.CTkLabel(allEmployeeFrame, text=itemList[1], width=32, text_font=("Calibri", 14))
            empAllLabel2.place(x=200, y=rowHeight)
            empAllLabel3 = customtkinter.CTkLabel(allEmployeeFrame, text=itemList[2], width=32, text_font=("Calibri", 14))
            empAllLabel3.place(x=350, y=rowHeight)
            empAllLabel4 = customtkinter.CTkLabel(allEmployeeFrame, text=itemList[3], width=32, text_font=("Calibri", 14))
            empAllLabel4.place(x=500, y=rowHeight)
            empAllLabel5 = customtkinter.CTkLabel(allEmployeeFrame, text=itemList[7], width=32, text_font=("Calibri", 14))
            empAllLabel5.place(x=650, y=rowHeight)
        switch_page(allEmployeeFrame)
    if type == "department":
        mycursor.execute("SELECT * FROM employee WHERE DepartmentNumber = (SELECT DepartmentNumber FROM employee WHERE ID = " + siEntry1.get() + ") ORDER BY Lname")
        for x in mycursor:
            infoList.append(list(x))
        rowHeight = 110
        mycursor.execute("SELECT COUNT(*) FROM employee WHERE DepartmentNumber = (SELECT DepartmentNumber FROM employee WHERE ID = " + siEntry1.get() + ")")
        for x in mycursor:
            count = str(''.join(str(elem) for elem in x))
        txt = 'Employee Count: ' + count
        empCountLabel = customtkinter.CTkLabel(allDeptFrame, text=txt, width=32, text_font=("Calibri", 14), bg_color="#262529")
        empCountLabel.place(x=500, y=5)
        mycursor.execute(
            "SELECT MAX(Salary) FROM employee WHERE DepartmentNumber = (SELECT DepartmentNumber FROM employee WHERE ID = " + siEntry1.get() + ")")
        for x in mycursor:
            max = str(''.join(str(elem) for elem in x))
        txt = 'Max Salary: ' + max
        maxCountLabel = customtkinter.CTkLabel(allDeptFrame, text=txt, width=32, text_font=("Calibri", 14),bg_color="#262529")
        maxCountLabel.place(x=500, y=32)
        for itemList in infoList:
            rowHeight += 25
            deptAllLabel1 = customtkinter.CTkLabel(allDeptFrame, text=itemList[0], width=32, text_font=("Calibri", 14))
            deptAllLabel1.place(x=50, y=rowHeight)
            deptAllLabel2 = customtkinter.CTkLabel(allDeptFrame, text=itemList[1], width=32, text_font=("Calibri", 14))
            deptAllLabel2.place(x=200, y=rowHeight)
            deptAllLabel3 = customtkinter.CTkLabel(allDeptFrame, text=itemList[2], width=32, text_font=("Calibri", 14))
            deptAllLabel3.place(x=350, y=rowHeight)
            deptAllLabel4 = customtkinter.CTkLabel(allDeptFrame, text=itemList[3], width=32, text_font=("Calibri", 14))
            deptAllLabel4.place(x=500, y=rowHeight)
            deptAllLabel5 = customtkinter.CTkLabel(allDeptFrame, text=itemList[5], width=32, text_font=("Calibri", 14))
            deptAllLabel5.place(x=650, y=rowHeight)
        switch_page(allDeptFrame)
    if type == "customer":
        mycursor.execute("SELECT * FROM customer ORDER BY CLName")
        for x in mycursor:
            infoList.append(list(x))
        rowHeight = 110
        for itemList in infoList:
            rowHeight += 25
            custAllLabel1 = customtkinter.CTkLabel(allCustomerFrame, text=itemList[0], width=32, text_font=("Calibri", 14))
            custAllLabel1.place(x=50, y=rowHeight)
            custAllLabel2 = customtkinter.CTkLabel(allCustomerFrame, text=itemList[1], width=32, text_font=("Calibri", 14))
            custAllLabel2.place(x=200, y=rowHeight)
            custAllLabel3 = customtkinter.CTkLabel(allCustomerFrame, text=itemList[2], width=32, text_font=("Calibri", 14))
            custAllLabel3.place(x=350, y=rowHeight)
            custAllLabel4 = customtkinter.CTkLabel(allCustomerFrame, text=itemList[5], width=32, text_font=("Calibri", 14))
            custAllLabel4.place(x=500, y=rowHeight)
            custAllLabel5 = customtkinter.CTkLabel(allCustomerFrame, text=itemList[3], width=32, text_font=("Calibri", 14))
            custAllLabel5.place(x=700, y=rowHeight)
        switch_page(allCustomerFrame)
    if type == "item":
        mycursor.execute("SELECT * FROM inventory")
        for x in mycursor:
            infoList.append(list(x))
        rowHeight = 110
        for itemList in infoList:
            rowHeight += 25
            itemAllLabel1 = customtkinter.CTkLabel(allItemFrame, text=itemList[0], width=32, text_font=("Calibri", 14))
            itemAllLabel1.place(x=50, y=rowHeight)
            itemAllLabel2 = customtkinter.CTkLabel(allItemFrame, text=itemList[2], width=32, text_font=("Calibri", 14))
            itemAllLabel2.place(x=180, y=rowHeight)
            itemAllLabel3 = customtkinter.CTkLabel(allItemFrame, text=itemList[1], width=32, text_font=("Calibri", 14))
            itemAllLabel3.place(x=370, y=rowHeight)
            itemAllLabel4 = customtkinter.CTkLabel(allItemFrame, text=itemList[3], width=32, text_font=("Calibri", 14))
            itemAllLabel4.place(x=520, y=rowHeight)
            itemAllLabel5 = customtkinter.CTkLabel(allItemFrame, text=itemList[4], width=32, text_font=("Calibri", 14))
            itemAllLabel5.place(x=700, y=rowHeight)
        switch_page(allItemFrame)
    rowHeight = 0


def create(frame):
    if frame == allEmployeeFrame:
        allEmployeeFrame.configure(bg="#17161a")
        allEmployeetopper = customtkinter.CTkFrame(master=allEmployeeFrame, fg_color="#262529", height=64,corner_radius=0)
        allEmployeetopper.grid(row=0, column=0, sticky='ew')
        backButton = customtkinter.CTkButton(allEmployeeFrame, width=100, height=32, corner_radius=8, text="Back",border_width=2, bg_color="#262529", text_font=("Calibri", 12),command=back)
        backButton.place(x=765, y=15)
        topLabel = customtkinter.CTkLabel(allEmployeeFrame, text="All Employees", text_font=("Calibri", 32, "bold"),bg_color="#262529")
        topLabel.place(x=30, y=3)
        ohLabel1 = customtkinter.CTkLabel(allEmployeeFrame, text="Employee ID:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel1.place(x=50, y=100)
        ohLabel2 = customtkinter.CTkLabel(allEmployeeFrame, text="Employee SSN:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel2.place(x=200, y=100)
        ohLabel3 = customtkinter.CTkLabel(allEmployeeFrame, text="First Name:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel3.place(x=350, y=100)
        ohLabel4 = customtkinter.CTkLabel(allEmployeeFrame, text="Last Name:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel4.place(x=500, y=100)
        ohLabel4 = customtkinter.CTkLabel(allEmployeeFrame, text="Department Number:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel4.place(x=650, y=100)
    elif frame == allOrderFrame:
        allOrderFrame.configure(bg="#17161a")
        allOrdertopper = customtkinter.CTkFrame(master=allOrderFrame, fg_color="#262529", height=64, corner_radius=0)
        allOrdertopper.grid(row=0, column=0, sticky='ew')
        backButton = customtkinter.CTkButton(allOrderFrame, width=100, height=32, corner_radius=8, text="Back",border_width=2, bg_color="#262529", text_font=("Calibri", 12),command=back)
        backButton.place(x=765, y=15)
        # All orders page widgets
        topLabel = customtkinter.CTkLabel(allOrderFrame, text="All Orders", text_font=("Calibri", 32, "bold"),bg_color="#262529")
        topLabel.place(x=30, y=3)
        ohLabel1 = customtkinter.CTkLabel(allOrderFrame, text="Supplier ID:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel1.place(x=80, y=100)
        ohLabel2 = customtkinter.CTkLabel(allOrderFrame, text="Item ID:", width=32, text_font=("Calibri", 14, "bold"))
        ohLabel2.place(x=280, y=100)
        ohLabel3 = customtkinter.CTkLabel(allOrderFrame, text="Item Name:", width=32, text_font=("Calibri", 14, "bold"))
        ohLabel3.place(x=480, y=100)
        ohLabel4 = customtkinter.CTkLabel(allOrderFrame, text="Quantity:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel4.place(x=680, y=100)
    elif frame == allDeptFrame:
        allDeptFrame.configure(bg="#17161a")
        allDepttopper = customtkinter.CTkFrame(master=allDeptFrame, fg_color="#262529", height=64, corner_radius=0)
        allDepttopper.grid(row=0, column=0, sticky='ew')
        backButton = customtkinter.CTkButton(allDeptFrame, width=100, height=32, corner_radius=8, text="Back",border_width=2, bg_color="#262529", text_font=("Calibri", 12),command=back)
        backButton.place(x=765, y=15)
        # All dept page widgets
        topLabel = customtkinter.CTkLabel(allDeptFrame, text="My Department", text_font=("Calibri", 32, "bold"),bg_color="#262529")
        topLabel.place(x=30, y=3)
        ohLabel1 = customtkinter.CTkLabel(allDeptFrame, text="Employee ID:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel1.place(x=50, y=100)
        ohLabel2 = customtkinter.CTkLabel(allDeptFrame, text="Employee SSN:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel2.place(x=200, y=100)
        ohLabel3 = customtkinter.CTkLabel(allDeptFrame, text="First Name:", width=32, text_font=("Calibri", 14, "bold"))
        ohLabel3.place(x=350, y=100)
        ohLabel4 = customtkinter.CTkLabel(allDeptFrame, text="Last Name:", width=32, text_font=("Calibri", 14, "bold"))
        ohLabel4.place(x=500, y=100)
        ohLabel4 = customtkinter.CTkLabel(allDeptFrame, text="Phone Number:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel4.place(x=650, y=100)
    elif frame == allCustomerFrame:
        allCustomerFrame.configure(bg="#17161a")
        allCustomertopper = customtkinter.CTkFrame(master=allCustomerFrame, fg_color="#262529", height=64, corner_radius=0)
        allCustomertopper.grid(row=0, column=0, sticky='ew')
        backButton = customtkinter.CTkButton(allCustomerFrame, width=100, height=32, corner_radius=8, text="Back",border_width=2, bg_color="#262529", text_font=("Calibri", 12),command=back)
        backButton.place(x=765, y=15)
        # All dept page widgets
        topLabel = customtkinter.CTkLabel(allCustomerFrame, text="All Customers", text_font=("Calibri", 32, "bold"),bg_color="#262529")
        topLabel.place(x=30, y=3)
        ohLabel1 = customtkinter.CTkLabel(allCustomerFrame, text="Customer ID:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel1.place(x=50, y=100)
        ohLabel2 = customtkinter.CTkLabel(allCustomerFrame, text="First Name:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel2.place(x=200, y=100)
        ohLabel3 = customtkinter.CTkLabel(allCustomerFrame, text="Last Name:", width=32, text_font=("Calibri", 14, "bold"))
        ohLabel3.place(x=350, y=100)
        ohLabel4 = customtkinter.CTkLabel(allCustomerFrame, text="Phone Number:", width=32, text_font=("Calibri", 14, "bold"))
        ohLabel4.place(x=500, y=100)
        ohLabel4 = customtkinter.CTkLabel(allCustomerFrame, text="Points:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel4.place(x=700, y=100)
    elif frame == allItemFrame:
        allItemFrame.configure(bg="#17161a")
        allItemtopper = customtkinter.CTkFrame(master=allItemFrame, fg_color="#262529", height=64, corner_radius=0)
        allItemtopper.grid(row=0, column=0, sticky='ew')
        backButton = customtkinter.CTkButton(allItemFrame, width=100, height=32, corner_radius=8, text="Back",border_width=2, bg_color="#262529", text_font=("Calibri", 12),command=back)
        backButton.place(x=765, y=15)
        # All dept page widgets
        topLabel = customtkinter.CTkLabel(allItemFrame, text="All Inventory", text_font=("Calibri", 32, "bold"),bg_color="#262529")
        topLabel.place(x=30, y=3)
        ohLabel1 = customtkinter.CTkLabel(allItemFrame, text="Item ID:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel1.place(x=50, y=100)
        ohLabel2 = customtkinter.CTkLabel(allItemFrame, text="Item Name:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel2.place(x=180, y=100)
        ohLabel3 = customtkinter.CTkLabel(allItemFrame, text="Price:", width=32, text_font=("Calibri", 14, "bold"))
        ohLabel3.place(x=370, y=100)
        ohLabel4 = customtkinter.CTkLabel(allItemFrame, text="Supplier ID:", width=32, text_font=("Calibri", 14, "bold"))
        ohLabel4.place(x=520, y=100)
        ohLabel4 = customtkinter.CTkLabel(allItemFrame, text="Quantity:", width=32,text_font=("Calibri", 14, "bold"))
        ohLabel4.place(x=700, y=100)


# ------------ ALL CODE BELOW THIS POINT INVOLVES NO MYSQL AND IS PURELY FOR CREATING THE LAYOUT OF THE GUI ------------


# Layout of the sign-in page
signInFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
siButton1 = customtkinter.CTkButton(signInFrame, width=100, height=32, corner_radius=8, text="Sign In", border_width=2, text_font=("Calibri", 12), command=sign_in)
siButton1.place(x=400, y=360)
siEntry1 = customtkinter.CTkEntry(signInFrame, placeholder_text="Enter your ID...", width=210, border_width=2, height=34, text_font=("Calibri", 12))
siEntry1.place(x=345, y=240)
siEntry2 = customtkinter.CTkEntry(signInFrame, placeholder_text="Enter your SSN...", width=210, border_width=2, height=34, text_font=("Calibri", 12))
siEntry2.place(x=345, y=290)
errorLabel = customtkinter.CTkLabel(signInFrame, text="", text_font=("Calibri", 16), bg_color="#17161a", text_color="red")
errorLabel.place(x=348, y=415)
signInFrame.grid(row=0, column=0, sticky='nesw')

# Layout of the manager view page
managerViewFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
managerViewFrame.grid_columnconfigure(0, weight=1)
topper = customtkinter.CTkFrame(master=managerViewFrame, fg_color="#262529", height=64, corner_radius=0)
topper.grid(row=0, column=0, sticky='ew')
# Employee Column widgets
topLabel = customtkinter.CTkLabel(managerViewFrame, text="Manager View", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
columnborder = customtkinter.CTkFrame(master=managerViewFrame, fg_color="#262529", width=260, height=60)
columnborder.place(x=35, y=120)
columnborder2 = customtkinter.CTkFrame(master=managerViewFrame, fg_color="#262529", width=260, height=240)
columnborder2.place(x=35, y=210)
columnborder25 = customtkinter.CTkFrame(master=managerViewFrame, fg_color="#262529", width=260, height=120)
columnborder25.place(x=35, y=480)
signoutButton = customtkinter.CTkButton(managerViewFrame, width=100, height=32, corner_radius=8, bg_color="#262529", text="Sign Out", border_width=2, text_font=("Calibri", 12), command=sign_out)
signoutButton.place(x=765, y=15)
mvLabel1 = customtkinter.CTkLabel(managerViewFrame, text="Employee Information", text_font=("Calibri", 20, "bold"))
mvLabel1.place(x=30, y=75)
mvButton1 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Add Employee", text_font=("Calibri", 18), bg_color="#262529", command=lambda: switch_page(employeeAddFrame))
mvButton1.place(x=45, y=130)
mvEntry1 = customtkinter.CTkEntry(managerViewFrame, placeholder_text="Enter Employee ID...", width=240, height=36, border_width=2, corner_radius=0, text_font=("Calibri", 18))
mvEntry1.place(x=45, y=220)
mvButton2 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Edit Employee", text_font=("Calibri", 18), bg_color="#262529", command=lambda: switch_page(employeeEditFrame))
mvButton2.place(x=45, y=280)
mvButton3 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Delete Employee", text_font=("Calibri", 18), bg_color="#262529", command=lambda: delete("employee"))
mvButton3.place(x=45, y=340)
mvButton4 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Employee Info", text_font=("Calibri", 18), bg_color="#262529", command=lambda: info("employee"))
mvButton4.place(x=45, y=400)
mvButton5 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="My Department", text_font=("Calibri", 18), bg_color="#262529", command=lambda: all("department", allDeptFrame))
mvButton5.place(x=45, y=490)
mvButton6 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="All Employees", text_font=("Calibri", 18), bg_color="#262529", command=lambda: all("employee", allEmployeeFrame))
mvButton6.place(x=45, y=550)
# Inventory Column Widgets
columnborder3 = customtkinter.CTkFrame(master=managerViewFrame, fg_color="#262529", width=260, height=60)
columnborder3.place(x=320, y=120)
columnborder4 = customtkinter.CTkFrame(master=managerViewFrame, fg_color="#262529", width=260, height=240)
columnborder4.place(x=320, y=210)
columnborder45 = customtkinter.CTkFrame(master=managerViewFrame, fg_color="#262529", width=260, height=180)
columnborder45.place(x=320, y=480)
mvLabel2 = customtkinter.CTkLabel(managerViewFrame, text="Inventory Information", text_font=("Calibri", 20, "bold"))
mvLabel2.place(x=315, y=75)
mvButton5 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Add Item", text_font=("Calibri", 18), bg_color="#262529", command=lambda: switch_page(itemAddFrame))
mvButton5.place(x=330, y=130)
mvEntry2 = customtkinter.CTkEntry(managerViewFrame, placeholder_text="Enter Item ID...", width=240, height=36, border_width=2, corner_radius=0, text_font=("Calibri", 18))
mvEntry2.place(x=330, y=220)
mvButton6 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Edit Item", text_font=("Calibri", 18), bg_color="#262529", command=lambda: switch_page(itemEditFrame))
mvButton6.place(x=330, y=280)
mvButton7 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Delete Item", text_font=("Calibri", 18), bg_color="#262529", command=lambda: delete("item"))
mvButton7.place(x=330, y=340)
mvButton8 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Item Info", text_font=("Calibri", 18), bg_color="#262529", command=lambda: info("item"))
mvButton8.place(x=330, y=400)
mvButton9 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Place Order", text_font=("Calibri", 18), bg_color="#262529", command=lambda: switch_page(orderFrame))
mvButton9.place(x=330, y=490)
mvButton6 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="All Orders", text_font=("Calibri", 18), bg_color="#262529", command=lambda: all("orders", allOrderFrame))
mvButton6.place(x=330, y=550)
mvButton6 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="All Items", text_font=("Calibri", 18), bg_color="#262529", command=lambda: all("item", allItemFrame))
mvButton6.place(x=330, y=610)
# Customer Column Widgets
columnborder5 = customtkinter.CTkFrame(master=managerViewFrame, fg_color="#262529", width=260, height=60)
columnborder5.place(x=605, y=120)
columnborder6 = customtkinter.CTkFrame(master=managerViewFrame, fg_color="#262529", width=260, height=240)
columnborder6.place(x=605, y=210)
columnborder65 = customtkinter.CTkFrame(master=managerViewFrame, fg_color="#262529", width=260, height=60)
columnborder65.place(x=605, y=480)
mvLabel3 = customtkinter.CTkLabel(managerViewFrame, text="Customer Information", text_font=("Calibri", 20, "bold"))
mvLabel3.place(x=600, y=75)
mvButton9 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Add Account", text_font=("Calibri", 18), bg_color="#262529", command=lambda: switch_page(custAddFrame))
mvButton9.place(x=615, y=130)
mvEntry3 = customtkinter.CTkEntry(managerViewFrame, placeholder_text="Enter Account ID...", width=240, height=36, border_width=2, corner_radius=0, text_font=("Calibri", 18))
mvEntry3.place(x=615, y=220)
mvButton10 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Edit Account", text_font=("Calibri", 18), bg_color="#262529", command=lambda: switch_page(custEditFrame))
mvButton10.place(x=615, y=280)
mvButton11 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Delete Account", text_font=("Calibri", 18), bg_color="#262529", command=lambda: delete("customer"))
mvButton11.place(x=615, y=340)
mvButton12 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Account Info", text_font=("Calibri", 18), bg_color="#262529", command=lambda: info("customer"))
mvButton12.place(x=615, y=400)
mvButton9 = customtkinter.CTkButton(managerViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="All Customers", text_font=("Calibri", 18), bg_color="#262529", command=lambda: all("customer", allCustomerFrame))
mvButton9.place(x=615, y=490)
managerViewFrame.grid(row=0, column=0, sticky='nesw')

# Layout of the Employee Info Page
employeeInfoFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
employeeInfoFrame.grid_columnconfigure(0, weight=1)
employeeInfotopper = customtkinter.CTkFrame(master=employeeInfoFrame, fg_color="#262529", height=64, corner_radius=0)
employeeInfotopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(employeeInfoFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=back)
backButton.place(x=765, y=15)
# Employee info page widgets
topLabel = customtkinter.CTkLabel(employeeInfoFrame, text="Employee Information", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
eiLabel1 = customtkinter.CTkLabel(employeeInfoFrame, text="ID:", width=32, text_font=("Calibri", 14, "bold"))
eiLabel1.place(x=45, y=100)
eiLabel2 = customtkinter.CTkLabel(employeeInfoFrame, text="SSN:", width=32, text_font=("Calibri", 14, "bold"))
eiLabel2.place(x=45, y=140)
eiLabel3 = customtkinter.CTkLabel(employeeInfoFrame, text="First Name:", width=32, text_font=("Calibri", 14, "bold"))
eiLabel3.place(x=45, y=180)
eiLabel4 = customtkinter.CTkLabel(employeeInfoFrame, text="Last Name:", width=32, text_font=("Calibri", 14, "bold"))
eiLabel4.place(x=45, y=220)
eiLabel5 = customtkinter.CTkLabel(employeeInfoFrame, text="Email:", width=32, text_font=("Calibri", 14, "bold"))
eiLabel5.place(x=45, y=260)
eiLabel6 = customtkinter.CTkLabel(employeeInfoFrame, text="Phone Number:", width=32, text_font=("Calibri", 14, "bold"))
eiLabel6.place(x=45, y=300)
eiLabel7 = customtkinter.CTkLabel(employeeInfoFrame, text="Emergency Contact Number:", width=32, text_font=("Calibri", 14, "bold"))
eiLabel7.place(x=45, y=340)
eiLabel8 = customtkinter.CTkLabel(employeeInfoFrame, text="Department Number:", width=32, text_font=("Calibri", 14, "bold"))
eiLabel8.place(x=45, y=380)
eiLabel9 = customtkinter.CTkLabel(employeeInfoFrame, text="Address:", width=32, text_font=("Calibri", 14, "bold"))
eiLabel9.place(x=45, y=420)
eiLabel95 = customtkinter.CTkLabel(employeeInfoFrame, text="Salary:", width=32, text_font=("Calibri", 14, "bold"))
eiLabel95.place(x=45, y=460)
eiLabel10 = customtkinter.CTkLabel(employeeInfoFrame, textvariable=tv1, width=32, text_font=("Calibri", 14))
eiLabel10.place(x=300, y=100)
eiLabel11 = customtkinter.CTkLabel(employeeInfoFrame, textvariable=tv2, width=32, text_font=("Calibri", 14))
eiLabel11.place(x=300, y=140)
eiLabel12 = customtkinter.CTkLabel(employeeInfoFrame, textvariable=tv3, width=32, text_font=("Calibri", 14))
eiLabel12.place(x=300, y=180)
eiLabel13 = customtkinter.CTkLabel(employeeInfoFrame, textvariable=tv4, width=32, text_font=("Calibri", 14))
eiLabel13.place(x=300, y=220)
eiLabel14 = customtkinter.CTkLabel(employeeInfoFrame, textvariable=tv5, width=32, text_font=("Calibri", 14))
eiLabel14.place(x=300, y=260)
eiLabel15 = customtkinter.CTkLabel(employeeInfoFrame, textvariable=tv6, width=32, text_font=("Calibri", 14))
eiLabel15.place(x=300, y=300)
eiLabel16 = customtkinter.CTkLabel(employeeInfoFrame, textvariable=tv7, width=32, text_font=("Calibri", 14))
eiLabel16.place(x=300, y=340)
eiLabel17 = customtkinter.CTkLabel(employeeInfoFrame, textvariable=tv8, width=32, text_font=("Calibri", 14))
eiLabel17.place(x=300, y=380)
eiLabel18 = customtkinter.CTkLabel(employeeInfoFrame, textvariable=tv9, width=32, text_font=("Calibri", 14))
eiLabel18.place(x=300, y=420)
eiLabel19 = customtkinter.CTkLabel(employeeInfoFrame, textvariable=tv10, width=32, text_font=("Calibri", 14))
eiLabel19.place(x=300, y=460)
employeeInfoFrame.grid(row=0, column=0, sticky='nesw')

# Layout for employee edit page
employeeEditFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
employeeEditFrame.grid_columnconfigure(0, weight=1)
employeeEdittopper = customtkinter.CTkFrame(master=employeeEditFrame, fg_color="#262529", height=64, corner_radius=0)
employeeEdittopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(employeeEditFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=back)
backButton.place(x=765, y=15)
saveButton = customtkinter.CTkButton(employeeEditFrame, width=100, height=32, corner_radius=8, text="Save Changes", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: edit("employee"))
saveButton.place(x=755, y=553)
# Employee edit page widgets
topLabel = customtkinter.CTkLabel(employeeEditFrame, text="Employee Edit", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
eeLabel1 = customtkinter.CTkLabel(employeeEditFrame, text="SSN:", width=32, text_font=("Calibri", 14, "bold"))
eeLabel1.place(x=45, y=100)
eeLabel2 = customtkinter.CTkLabel(employeeEditFrame, text="First Name:", width=32, text_font=("Calibri", 14, "bold"))
eeLabel2.place(x=45, y=140)
eeLabel3 = customtkinter.CTkLabel(employeeEditFrame, text="Last Name:", width=32, text_font=("Calibri", 14, "bold"))
eeLabel3.place(x=45, y=180)
eeLabel4 = customtkinter.CTkLabel(employeeEditFrame, text="Email:", width=32, text_font=("Calibri", 14, "bold"))
eeLabel4.place(x=45, y=220)
eeLabel5 = customtkinter.CTkLabel(employeeEditFrame, text="Phone Number:", width=32, text_font=("Calibri", 14, "bold"))
eeLabel5.place(x=45, y=260)
eeLabel6 = customtkinter.CTkLabel(employeeEditFrame, text="Emergency Contact Number:", width=32, text_font=("Calibri", 14, "bold"))
eeLabel6.place(x=45, y=300)
eeLabel7 = customtkinter.CTkLabel(employeeEditFrame, text="Department Number:", width=32, text_font=("Calibri", 14, "bold"))
eeLabel7.place(x=45, y=340)
eeLabel8 = customtkinter.CTkLabel(employeeEditFrame, text="Address:", width=32, text_font=("Calibri", 14, "bold"))
eeLabel8.place(x=45, y=380)
eeLabel9 = customtkinter.CTkLabel(employeeEditFrame, text="Salary:", width=32, text_font=("Calibri", 14, "bold"))
eeLabel9.place(x=45, y=420)
eeEntry1 = customtkinter.CTkEntry(employeeEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
eeEntry1.place(x=300, y=100)
eeEntry2 = customtkinter.CTkEntry(employeeEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
eeEntry2.place(x=300, y=140)
eeEntry3 = customtkinter.CTkEntry(employeeEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
eeEntry3.place(x=300, y=180)
eeEntry4 = customtkinter.CTkEntry(employeeEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
eeEntry4.place(x=300, y=220)
eeEntry5 = customtkinter.CTkEntry(employeeEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
eeEntry5.place(x=300, y=260)
eeEntry6 = customtkinter.CTkEntry(employeeEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
eeEntry6.place(x=300, y=300)
eeEntry7 = customtkinter.CTkEntry(employeeEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
eeEntry7.place(x=300, y=340)
eeEntry8 = customtkinter.CTkEntry(employeeEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
eeEntry8.place(x=300, y=380)
eeEntry9 = customtkinter.CTkEntry(employeeEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
eeEntry9.place(x=300, y=420)
eeLabel10 = customtkinter.CTkLabel(employeeEditFrame, text="Note: Only enter into the fields you wish to change, leave all others blank.", width=32, text_font=("Calibri", 14))
eeLabel10.place(x=45, y=480)
employeeEditFrame.grid(row=0, column=0, sticky='nesw')

# Layout for employee add page
employeeAddFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
employeeAddFrame.grid_columnconfigure(0, weight=1)
employeeAddtopper = customtkinter.CTkFrame(master=employeeAddFrame, fg_color="#262529", height=64, corner_radius=0)
employeeAddtopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(employeeAddFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: switch_page(managerViewFrame))
backButton.place(x=765, y=15)
saveButton = customtkinter.CTkButton(employeeAddFrame, width=100, height=32, corner_radius=8, text="Add Employee", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: add("employee"))
saveButton.place(x=755, y=553)
# Employee add page widgets
topLabel = customtkinter.CTkLabel(employeeAddFrame, text="Employee Addition", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
aeLabel1 = customtkinter.CTkLabel(employeeAddFrame, text="SSN:", width=32, text_font=("Calibri", 14, "bold"))
aeLabel1.place(x=45, y=100)
aeLabel2 = customtkinter.CTkLabel(employeeAddFrame, text="First Name:", width=32, text_font=("Calibri", 14, "bold"))
aeLabel2.place(x=45, y=140)
aeLabel3 = customtkinter.CTkLabel(employeeAddFrame, text="Last Name:", width=32, text_font=("Calibri", 14, "bold"))
aeLabel3.place(x=45, y=180)
aeLabel4 = customtkinter.CTkLabel(employeeAddFrame, text="Email:", width=32, text_font=("Calibri", 14, "bold"))
aeLabel4.place(x=45, y=220)
aeLabel5 = customtkinter.CTkLabel(employeeAddFrame, text="Phone Number:", width=32, text_font=("Calibri", 14, "bold"))
aeLabel5.place(x=45, y=260)
aeLabel6 = customtkinter.CTkLabel(employeeAddFrame, text="Emergency Contact Number:", width=32, text_font=("Calibri", 14, "bold"))
aeLabel6.place(x=45, y=300)
aeLabel7 = customtkinter.CTkLabel(employeeAddFrame, text="Department Number:", width=32, text_font=("Calibri", 14, "bold"))
aeLabel7.place(x=45, y=340)
aeLabel8 = customtkinter.CTkLabel(employeeAddFrame, text="Address:", width=32, text_font=("Calibri", 14, "bold"))
aeLabel8.place(x=45, y=380)
aeLabel9 = customtkinter.CTkLabel(employeeAddFrame, text="Salary:", width=32, text_font=("Calibri", 14, "bold"))
aeLabel9.place(x=45, y=420)
aeEntry1 = customtkinter.CTkEntry(employeeAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
aeEntry1.place(x=300, y=100)
aeEntry2 = customtkinter.CTkEntry(employeeAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
aeEntry2.place(x=300, y=140)
aeEntry3 = customtkinter.CTkEntry(employeeAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
aeEntry3.place(x=300, y=180)
aeEntry4 = customtkinter.CTkEntry(employeeAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
aeEntry4.place(x=300, y=220)
aeEntry5 = customtkinter.CTkEntry(employeeAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
aeEntry5.place(x=300, y=260)
aeEntry6 = customtkinter.CTkEntry(employeeAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
aeEntry6.place(x=300, y=300)
aeEntry7 = customtkinter.CTkEntry(employeeAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
aeEntry7.place(x=300, y=340)
aeEntry8 = customtkinter.CTkEntry(employeeAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
aeEntry8.place(x=300, y=380)
aeEntry9 = customtkinter.CTkEntry(employeeAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
aeEntry9.place(x=300, y=420)
aeLabel10 = customtkinter.CTkLabel(employeeAddFrame, text="Note: If you wish to set a field to null, you must enter null", width=32, text_font=("Calibri", 14))
aeLabel10.place(x=45, y=480)
employeeAddFrame.grid(row=0, column=0, sticky='nesw')

# Layout for all employees page
allEmployeeFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
allEmployeeFrame.grid_columnconfigure(0, weight=1)
allEmployeetopper = customtkinter.CTkFrame(master=allEmployeeFrame, fg_color="#262529", height=64, corner_radius=0)
allEmployeetopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(allEmployeeFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: switch_page(managerViewFrame))
backButton.place(x=765, y=15)
allEmployeeFrame.grid(row=0, column=0, sticky='nesw')

# Layout for all dept page
allDeptFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
allDeptFrame.grid_columnconfigure(0, weight=1)
allDepttopper = customtkinter.CTkFrame(master=allDeptFrame, fg_color="#262529", height=64, corner_radius=0)
allDepttopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(allDeptFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: switch_page(managerViewFrame))
backButton.place(x=765, y=15)
allDeptFrame.grid(row=0, column=0, sticky='nesw')

# Layout for delete page
deleteFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
deleteFrame.grid_columnconfigure(0, weight=1)
deletetopper = customtkinter.CTkFrame(master=deleteFrame, fg_color="#262529", height=64, corner_radius=0)
deletetopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(deleteFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=back)
backButton.place(x=765, y=15)
topLabel = customtkinter.CTkLabel(deleteFrame, text="Delete", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
dLabel1 = customtkinter.CTkLabel(deleteFrame, textvariable=toDelete, width=120, text_font=("Calibri", 20, "bold"))
dLabel1.place(x=450, y=250, anchor="center")
dButton1 = customtkinter.CTkButton(deleteFrame, width=40, height=32, corner_radius=8, text="No", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: back())
dButton1.place(x=390, y=300)
dButton2 = customtkinter.CTkButton(deleteFrame, width=40, height=32, corner_radius=8, text="Yes", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: confirm_delete())
dButton2.place(x=450, y=300)
deleteFrame.grid(row=0, column=0, sticky='nesw')

# Layout for item info page
itemInfoFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
itemInfoFrame.grid_columnconfigure(0, weight=1)
itemInfotopper = customtkinter.CTkFrame(master=itemInfoFrame, fg_color="#262529", height=64, corner_radius=0)
itemInfotopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(itemInfoFrame, width=100, height=32, corner_radius=8, text="Back",border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=back)
backButton.place(x=765, y=15)
topLabel = customtkinter.CTkLabel(itemInfoFrame, text="Item Information", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
labelText = ["Item ID:", "Price:", "Item Name:", "Supplier ID:", "Item Count:", tv1, tv2, tv3, tv4, tv5]
currY = 60
currY2 = 60
for i in range(10):
    if i < 5:
        iiLabel = customtkinter.CTkLabel(itemInfoFrame, text=labelText[i], width=32, text_font=("Calibri", 14, "bold"))
        currY += 40
        iiLabel.place(x=45, y=currY)
    else:
        iiLabel = customtkinter.CTkLabel(itemInfoFrame, textvariable=labelText[i], width=32, text_font=("Calibri", 14))
        currY2 += 40
        iiLabel.place(x=300, y=currY2)
itemInfoFrame.grid(row=0, column=0, sticky='nesw')

# Layout for item add page
itemAddFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
itemAddFrame.grid_columnconfigure(0, weight=1)
itemAddtopper = customtkinter.CTkFrame(master=itemAddFrame, fg_color="#262529", height=64, corner_radius=0)
itemAddtopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(itemAddFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: switch_page(managerViewFrame))
backButton.place(x=765, y=15)
saveButton = customtkinter.CTkButton(itemAddFrame, width=100, height=32, corner_radius=8, text="Add Item", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: add("item"))
saveButton.place(x=755, y=553)
# Item add page widgets
topLabel = customtkinter.CTkLabel(itemAddFrame, text="Item Addition", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
aiLabel1 = customtkinter.CTkLabel(itemAddFrame, text="Price:", width=32, text_font=("Calibri", 14, "bold"))
aiLabel1.place(x=45, y=100)
aiLabel2 = customtkinter.CTkLabel(itemAddFrame, text="Item Name:", width=32, text_font=("Calibri", 14, "bold"))
aiLabel2.place(x=45, y=140)
aiLabel3 = customtkinter.CTkLabel(itemAddFrame, text="Supplier ID:", width=32, text_font=("Calibri", 14, "bold"))
aiLabel3.place(x=45, y=180)
aiLabel4 = customtkinter.CTkLabel(itemAddFrame, text="Item Count:", width=32, text_font=("Calibri", 14, "bold"))
aiLabel4.place(x=45, y=220)
aiEntry1 = customtkinter.CTkEntry(itemAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
aiEntry1.place(x=300, y=100)
aiEntry2 = customtkinter.CTkEntry(itemAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
aiEntry2.place(x=300, y=140)
aiEntry3 = customtkinter.CTkEntry(itemAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
aiEntry3.place(x=300, y=180)
aiEntry4 = customtkinter.CTkEntry(itemAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
aiEntry4.place(x=300, y=220)
aiLabel5 = customtkinter.CTkLabel(itemAddFrame, text="Note: If you wish to set a field to null, you must enter null", width=32, text_font=("Calibri", 14))
aiLabel5.place(x=45, y=480)
itemAddFrame.grid(row=0, column=0, sticky='nesw')

# Layout for item edit page
itemEditFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
itemEditFrame.grid_columnconfigure(0, weight=1)
itemEdittopper = customtkinter.CTkFrame(master=itemEditFrame, fg_color="#262529", height=64, corner_radius=0)
itemEdittopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(itemEditFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: switch_page(managerViewFrame))
backButton.place(x=765, y=15)
saveButton = customtkinter.CTkButton(itemEditFrame, width=100, height=32, corner_radius=8, text="Save Changes", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: edit("item"))
saveButton.place(x=755, y=553)
# Item edit page widgets
topLabel = customtkinter.CTkLabel(itemEditFrame, text="Item Edit", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
eiLabel1 = customtkinter.CTkLabel(itemEditFrame, text="Price:", width=32, text_font=("Calibri", 14, "bold"))
eiLabel1.place(x=45, y=100)
eiLabel2 = customtkinter.CTkLabel(itemEditFrame, text="Item Name:", width=32, text_font=("Calibri", 14, "bold"))
eiLabel2.place(x=45, y=140)
eiLabel3 = customtkinter.CTkLabel(itemEditFrame, text="Supplier ID:", width=32, text_font=("Calibri", 14, "bold"))
eiLabel3.place(x=45, y=180)
eiLabel4 = customtkinter.CTkLabel(itemEditFrame, text="ItemCount:", width=32, text_font=("Calibri", 14, "bold"))
eiLabel4.place(x=45, y=220)
eiEntry1 = customtkinter.CTkEntry(itemEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
eiEntry1.place(x=300, y=100)
eiEntry2 = customtkinter.CTkEntry(itemEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
eiEntry2.place(x=300, y=140)
eiEntry3 = customtkinter.CTkEntry(itemEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
eiEntry3.place(x=300, y=180)
eiEntry4 = customtkinter.CTkEntry(itemEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
eiEntry4.place(x=300, y=220)
eiLabel5 = customtkinter.CTkLabel(itemEditFrame, text="Note: Only enter into the fields you wish to change, leave all others blank.", width=32, text_font=("Calibri", 14))
eiLabel5.place(x=45, y=480)
itemEditFrame.grid(row=0, column=0, sticky='nesw')

# Layout for order page
orderFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
orderFrame.grid_columnconfigure(0, weight=1)
ordertopper = customtkinter.CTkFrame(master=orderFrame, fg_color="#262529", height=64, corner_radius=0)
ordertopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(orderFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: switch_page(managerViewFrame))
backButton.place(x=765, y=15)
saveButton = customtkinter.CTkButton(orderFrame, width=100, height=32, corner_radius=8, text="Place Order", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=place_order)
saveButton.place(x=755, y=553)
# Order page widgets
topLabel = customtkinter.CTkLabel(orderFrame, text="Order Inventory", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
oiLabel1 = customtkinter.CTkLabel(orderFrame, text="Item 1:", width=32, text_font=("Calibri", 14, "bold"))
oiLabel1.place(x=45, y=150)
oiLabel2 = customtkinter.CTkLabel(orderFrame, text="Item 2:", width=32, text_font=("Calibri", 14, "bold"))
oiLabel2.place(x=45, y=250)
oiLabel3 = customtkinter.CTkLabel(orderFrame, text="Item 3:", width=32, text_font=("Calibri", 14, "bold"))
oiLabel3.place(x=45, y=300)
oiLabel4 = customtkinter.CTkLabel(orderFrame, text="Item 4:", width=32, text_font=("Calibri", 14, "bold"))
oiLabel4.place(x=45, y=350)
oiLabel5 = customtkinter.CTkLabel(orderFrame, text="Item ID:", width=32, text_font=("Calibri", 14, "bold"))
oiLabel5.place(x=160, y=100)
oiLabel6 = customtkinter.CTkLabel(orderFrame, text="Quantity:", width=32, text_font=("Calibri", 14, "bold"))
oiLabel6.place(x=340, y=100)
oiLabel5 = customtkinter.CTkLabel(orderFrame, text="Optional", width=36, text_font=("Calibri", 14, "bold"))
oiLabel5.place(x=100, y=200)
oiEntry1 = customtkinter.CTkEntry(orderFrame, width=140, text_font=("Calibri", 14), border_width=2, corner_radius=0)
oiEntry1.place(x=160, y=150)
oiEntry2 = customtkinter.CTkEntry(orderFrame, width=140, text_font=("Calibri", 14), border_width=2, corner_radius=0)
oiEntry2.place(x=340, y=150)
oiEntry3 = customtkinter.CTkEntry(orderFrame, width=140, text_font=("Calibri", 14), border_width=2, corner_radius=0)
oiEntry3.place(x=160, y=250)
oiEntry4 = customtkinter.CTkEntry(orderFrame, width=140, text_font=("Calibri", 14), border_width=2, corner_radius=0)
oiEntry4.place(x=340, y=250)
oiEntry5 = customtkinter.CTkEntry(orderFrame, width=140, text_font=("Calibri", 14), border_width=2, corner_radius=0)
oiEntry5.place(x=160, y=300)
oiEntry6 = customtkinter.CTkEntry(orderFrame, width=140, text_font=("Calibri", 14), border_width=2, corner_radius=0)
oiEntry6.place(x=340, y=300)
oiEntry7 = customtkinter.CTkEntry(orderFrame, width=140, text_font=("Calibri", 14), border_width=2, corner_radius=0)
oiEntry7.place(x=160, y=350)
oiEntry8 = customtkinter.CTkEntry(orderFrame, width=140, text_font=("Calibri", 14), border_width=2, corner_radius=0)
oiEntry8.place(x=340, y=350)
oiLabel7 = customtkinter.CTkLabel(orderFrame, text="Note: If you do not wish to order an item, leave the field blank.", width=32, text_font=("Calibri", 14))
oiLabel7.place(x=45, y=480)
orderFrame.grid(row=0, column=0, sticky='nesw')

# Layout for confirm order page
confOrderFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
confOrderFrame.grid_columnconfigure(0, weight=1)
confOrdertopper = customtkinter.CTkFrame(master=confOrderFrame, fg_color="#262529", height=64, corner_radius=0)
confOrdertopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(confOrderFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: switch_page(managerViewFrame))
backButton.place(x=765, y=15)
saveButton = customtkinter.CTkButton(confOrderFrame, width=100, height=32, corner_radius=8, text="Confirm Order", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=conf_order)
saveButton.place(x=755, y=553)
# Confirm order page widgets
topLabel = customtkinter.CTkLabel(confOrderFrame, text="Order Inventory", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
ohLabel1 = customtkinter.CTkLabel(confOrderFrame, text="Item:", width=32, text_font=("Calibri", 14, "bold"))
ohLabel1.place(x=80, y=100)
ohLabel2 = customtkinter.CTkLabel(confOrderFrame, text="Quantity:", width=32, text_font=("Calibri", 14, "bold"))
ohLabel2.place(x=280, y=100)
ohLabel3 = customtkinter.CTkLabel(confOrderFrame, text="Supplier:", width=32, text_font=("Calibri", 14, "bold"))
ohLabel3.place(x=480, y=100)
ohLabel4 = customtkinter.CTkLabel(confOrderFrame, text="Cost:", width=32, text_font=("Calibri", 14, "bold"))
ohLabel4.place(x=680, y=100)
confOrderFrame.grid(row=0, column=0, sticky='nesw')

# Layout for all orders page
allOrderFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
allOrderFrame.grid_columnconfigure(0, weight=1)
allOrdertopper = customtkinter.CTkFrame(master=allOrderFrame, fg_color="#262529", height=64, corner_radius=0)
allOrdertopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(allOrderFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: switch_page(managerViewFrame))
backButton.place(x=765, y=15)
allOrderFrame.grid(row=0, column=0, sticky='nesw')

# Layout for all items page
allItemFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
allItemFrame.grid_columnconfigure(0, weight=1)
allItemtopper = customtkinter.CTkFrame(master=allItemFrame, fg_color="#262529", height=64, corner_radius=0)
allItemtopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(allItemFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=back)
backButton.place(x=765, y=15)
allItemFrame.grid(row=0, column=0, sticky='nesw')

# Layout for customer info page
custInfoFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
custInfoFrame.grid_columnconfigure(0, weight=1)
custInfotopper = customtkinter.CTkFrame(master=custInfoFrame, fg_color="#262529", height=64, corner_radius=0)
custInfotopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(custInfoFrame, width=100, height=32, corner_radius=8, text="Back",border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=back)
backButton.place(x=765, y=15)
topLabel = customtkinter.CTkLabel(custInfoFrame, text="Customer Information", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
labelText = ["Customer ID:", "First Name:", "Last Name:", "Points Count:", "Email:", "Phone Number:", "Address:", tv1, tv2, tv3, tv4, tv5, tv6, tv7]
currYc = 60
currY2c = 60
for i in range(14):
    if i < 7:
        ciLabel = customtkinter.CTkLabel(custInfoFrame, text=labelText[i], width=32, text_font=("Calibri", 14, "bold"))
        currYc += 40
        ciLabel.place(x=45, y=currYc)
    else:
        ciLabel = customtkinter.CTkLabel(custInfoFrame, textvariable=labelText[i], width=32, text_font=("Calibri", 14))
        currY2c += 40
        ciLabel.place(x=300, y=currY2c)
custInfoFrame.grid(row=0, column=0, sticky='nesw')

# Layout for customer add page
custAddFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
custAddFrame.grid_columnconfigure(0, weight=1)
custAddtopper = customtkinter.CTkFrame(master=custAddFrame, fg_color="#262529", height=64, corner_radius=0)
custAddtopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(custAddFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: switch_page(managerViewFrame))
backButton.place(x=765, y=15)
saveButton = customtkinter.CTkButton(custAddFrame, width=100, height=32, corner_radius=8, text="Add Account", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: add("customer"))
saveButton.place(x=755, y=553)
# Item add page widgets
topLabel = customtkinter.CTkLabel(custAddFrame, text="Customer Addition", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
acLabel1 = customtkinter.CTkLabel(custAddFrame, text="First Name:", width=32, text_font=("Calibri", 14, "bold"))
acLabel1.place(x=45, y=100)
acLabel2 = customtkinter.CTkLabel(custAddFrame, text="Last Name:", width=32, text_font=("Calibri", 14, "bold"))
acLabel2.place(x=45, y=140)
acLabel3 = customtkinter.CTkLabel(custAddFrame, text="Points:", width=32, text_font=("Calibri", 14, "bold"))
acLabel3.place(x=45, y=180)
acLabel4 = customtkinter.CTkLabel(custAddFrame, text="Email:", width=32, text_font=("Calibri", 14, "bold"))
acLabel4.place(x=45, y=220)
acLabel5 = customtkinter.CTkLabel(custAddFrame, text="Phone Number:", width=32, text_font=("Calibri", 14, "bold"))
acLabel5.place(x=45, y=260)
acLabel6 = customtkinter.CTkLabel(custAddFrame, text="Address:", width=32, text_font=("Calibri", 14, "bold"))
acLabel6.place(x=45, y=300)
acEntry1 = customtkinter.CTkEntry(custAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
acEntry1.place(x=300, y=100)
acEntry2 = customtkinter.CTkEntry(custAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
acEntry2.place(x=300, y=140)
acEntry3 = customtkinter.CTkEntry(custAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
acEntry3.place(x=300, y=180)
acEntry4 = customtkinter.CTkEntry(custAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
acEntry4.place(x=300, y=220)
acEntry5 = customtkinter.CTkEntry(custAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
acEntry5.place(x=300, y=260)
acEntry6 = customtkinter.CTkEntry(custAddFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
acEntry6.place(x=300, y=300)
acLabel5 = customtkinter.CTkLabel(custAddFrame, text="Note: If you wish to set a field to null, you must enter null", width=32, text_font=("Calibri", 14))
acLabel5.place(x=45, y=480)
custAddFrame.grid(row=0, column=0, sticky='nesw')

# Layout for customer edit page
custEditFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
custEditFrame.grid_columnconfigure(0, weight=1)
custEdittopper = customtkinter.CTkFrame(master=custEditFrame, fg_color="#262529", height=64, corner_radius=0)
custEdittopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(custEditFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: switch_page(managerViewFrame))
backButton.place(x=765, y=15)
saveButton = customtkinter.CTkButton(custEditFrame, width=100, height=32, corner_radius=8, text="Save Changes", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: edit("customer"))
saveButton.place(x=755, y=553)
# customer edit page widgets
topLabel = customtkinter.CTkLabel(custEditFrame, text="Customer Edit", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
ecLabel1 = customtkinter.CTkLabel(custEditFrame, text="First Name:", width=32, text_font=("Calibri", 14, "bold"))
ecLabel1.place(x=45, y=100)
ecLabel2 = customtkinter.CTkLabel(custEditFrame, text="Last Name:", width=32, text_font=("Calibri", 14, "bold"))
ecLabel2.place(x=45, y=140)
ecLabel3 = customtkinter.CTkLabel(custEditFrame, text="Points:", width=32, text_font=("Calibri", 14, "bold"))
ecLabel3.place(x=45, y=180)
ecLabel4 = customtkinter.CTkLabel(custEditFrame, text="Email:", width=32, text_font=("Calibri", 14, "bold"))
ecLabel4.place(x=45, y=220)
ecLabel5 = customtkinter.CTkLabel(custEditFrame, text="Phone Number:", width=32, text_font=("Calibri", 14, "bold"))
ecLabel5.place(x=45, y=260)
ecLabel6 = customtkinter.CTkLabel(custEditFrame, text="Address:", width=32, text_font=("Calibri", 14, "bold"))
ecLabel6.place(x=45, y=300)
ecEntry1 = customtkinter.CTkEntry(custEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
ecEntry1.place(x=300, y=100)
ecEntry2 = customtkinter.CTkEntry(custEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
ecEntry2.place(x=300, y=140)
ecEntry3 = customtkinter.CTkEntry(custEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
ecEntry3.place(x=300, y=180)
ecEntry4 = customtkinter.CTkEntry(custEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
ecEntry4.place(x=300, y=220)
ecEntry5 = customtkinter.CTkEntry(custEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
ecEntry5.place(x=300, y=260)
ecEntry6 = customtkinter.CTkEntry(custEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
ecEntry6.place(x=300, y=300)
ecLabel7 = customtkinter.CTkLabel(custEditFrame, text="Note: Only enter into the fields you wish to change, leave all others blank.", width=32, text_font=("Calibri", 14))
ecLabel7.place(x=45, y=480)
custEditFrame.grid(row=0, column=0, sticky='nesw')

# Layout for all customers page
allCustomerFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
allCustomerFrame.grid_columnconfigure(0, weight=1)
allCustomertopper = customtkinter.CTkFrame(master=allCustomerFrame, fg_color="#262529", height=64, corner_radius=0)
allCustomertopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(allCustomerFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: switch_page(managerViewFrame))
backButton.place(x=765, y=15)
allCustomerFrame.grid(row=0, column=0, sticky='nesw')

########################################################################################################################
# Layout of the Employee View Page
employeeViewFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
employeeViewFrame.grid_columnconfigure(0, weight=1)
topper = customtkinter.CTkFrame(master=employeeViewFrame, fg_color="#262529", height=64, corner_radius=0)
topper.grid(row=0, column=0, sticky='ew')
signoutButton = customtkinter.CTkButton(employeeViewFrame, width=100, height=32, corner_radius=8, bg_color="#262529", text="Sign Out", border_width=2, text_font=("Calibri", 12), command=sign_out)
signoutButton.place(x=765, y=15)
# Employee Column Widgets
topLabel = customtkinter.CTkLabel(employeeViewFrame, text="Employee View", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
ecolumnborder1 = customtkinter.CTkFrame(master=employeeViewFrame, fg_color="#262529", width=260, height=180)
ecolumnborder1.place(x=320, y=120)
evLabel1 = customtkinter.CTkLabel(employeeViewFrame, text="Personal Information", text_font=("Calibri", 20, "bold"))
evLabel1.place(x=315, y=75)
evButton1 = customtkinter.CTkButton(employeeViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="My Info", text_font=("Calibri", 18), bg_color="#262529", command=lambda: info("employee"))
evButton1.place(x=330, y=130)
evButton2 = customtkinter.CTkButton(employeeViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Edit My Info", text_font=("Calibri", 18), bg_color="#262529", command=lambda: switch_page(employeeEditFrame))
evButton2.place(x=330, y=190)
evButton3 = customtkinter.CTkButton(employeeViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Department Info", text_font=("Calibri", 18), bg_color="#262529", command=lambda: info("department"))
evButton3.place(x=330, y=250)
employeeViewFrame.grid(row=0, column=0, sticky='nesw')

# Layout for department info page
deptInfoFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
deptInfoFrame.grid_columnconfigure(0, weight=1)
deptInfotopper = customtkinter.CTkFrame(master=deptInfoFrame, fg_color="#262529", height=64, corner_radius=0)
deptInfotopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(deptInfoFrame, width=100, height=32, corner_radius=8, text="Back",border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=back)
backButton.place(x=765, y=15)
topLabel = customtkinter.CTkLabel(deptInfoFrame, text="Department Information", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
labelText = ["Department ID:", "Department Name:", "Department Phone Number:", "Manager Name:", tv1, tv2, tv3, tv4]
currYd = 60
currY2d = 60
for i in range(8):
    if i < 4:
        diLabel = customtkinter.CTkLabel(deptInfoFrame, text=labelText[i], width=32, text_font=("Calibri", 14, "bold"))
        currYd += 40
        diLabel.place(x=45, y=currYd)
    else:
        diLabel = customtkinter.CTkLabel(deptInfoFrame, textvariable=labelText[i], width=32, text_font=("Calibri", 14))
        currY2d += 40
        diLabel.place(x=300, y=currY2d)
deptInfoFrame.grid(row=0, column=0, sticky='nesw')

########################################################################################################################
# Layout of the Customer View Page
custViewFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
custViewFrame.grid_columnconfigure(0, weight=1)
topper = customtkinter.CTkFrame(master=custViewFrame, fg_color="#262529", height=64, corner_radius=0)
topper.grid(row=0, column=0, sticky='ew')
signoutButton = customtkinter.CTkButton(custViewFrame, width=100, height=32, corner_radius=8, bg_color="#262529", text="Sign Out", border_width=2, text_font=("Calibri", 12), command=sign_out)
signoutButton.place(x=765, y=15)
# Customer Column Widgets
topLabel = customtkinter.CTkLabel(custViewFrame, text="Customer View", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
custborder1 = customtkinter.CTkFrame(master=custViewFrame, fg_color="#262529", width=260, height=240)
custborder1.place(x=320, y=120)
cvLabel1 = customtkinter.CTkLabel(custViewFrame, text="Information", text_font=("Calibri", 20, "bold"))
cvLabel1.place(x=385, y=75)
cvButton1 = customtkinter.CTkButton(custViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="My Info", text_font=("Calibri", 18), bg_color="#262529", command=lambda: info("customer"))
cvButton1.place(x=330, y=130)
cvButton2 = customtkinter.CTkButton(custViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Edit My Info", text_font=("Calibri", 18), bg_color="#262529", command=lambda: switch_page(custViewEditFrame))
cvButton2.place(x=330, y=190)
cvButton3 = customtkinter.CTkButton(custViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Delete Account", text_font=("Calibri", 18), bg_color="#262529", command=lambda: delete("customer"))
cvButton3.place(x=330, y=250)
cvButton3 = customtkinter.CTkButton(custViewFrame, width=240, height=36, border_width=2, corner_radius=8, text="Inventory Information", text_font=("Calibri", 18), bg_color="#262529", command=lambda: all("item",allItemFrame))
cvButton3.place(x=330, y=310)
custViewFrame.grid(row=0, column=0, sticky='nesw')

# Layout for customer view edit page
custViewEditFrame = customtkinter.CTkFrame(master=window, corner_radius=0, fg_color="#17161a")
custViewEditFrame.grid_columnconfigure(0, weight=1)
custViewEdittopper = customtkinter.CTkFrame(master=custViewEditFrame, fg_color="#262529", height=64, corner_radius=0)
custViewEdittopper.grid(row=0, column=0, sticky='ew')
backButton = customtkinter.CTkButton(custViewEditFrame, width=100, height=32, corner_radius=8, text="Back", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=back)
backButton.place(x=765, y=15)
saveButton = customtkinter.CTkButton(custViewEditFrame, width=100, height=32, corner_radius=8, text="Save Changes", border_width=2, bg_color="#262529", text_font=("Calibri", 12), command=lambda: edit("customerView"))
saveButton.place(x=755, y=553)
# customer edit page widgets
topLabel = customtkinter.CTkLabel(custViewEditFrame, text="Customer Edit", text_font=("Calibri", 32, "bold"), bg_color="#262529")
topLabel.place(x=30, y=3)
ecvvLabel1 = customtkinter.CTkLabel(custViewEditFrame, text="First Name:", width=32, text_font=("Calibri", 14, "bold"))
ecvvLabel1.place(x=45, y=100)
ecvLabel2 = customtkinter.CTkLabel(custViewEditFrame, text="Last Name:", width=32, text_font=("Calibri", 14, "bold"))
ecvLabel2.place(x=45, y=140)
ecvLabel4 = customtkinter.CTkLabel(custViewEditFrame, text="Email:", width=32, text_font=("Calibri", 14, "bold"))
ecvLabel4.place(x=45, y=180)
ecvLabel5 = customtkinter.CTkLabel(custViewEditFrame, text="Phone Number:", width=32, text_font=("Calibri", 14, "bold"))
ecvLabel5.place(x=45, y=220)
ecvLabel6 = customtkinter.CTkLabel(custViewEditFrame, text="Address:", width=32, text_font=("Calibri", 14, "bold"))
ecvLabel6.place(x=45, y=260)
ecvEntry1 = customtkinter.CTkEntry(custViewEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
ecvEntry1.place(x=300, y=100)
ecvEntry2 = customtkinter.CTkEntry(custViewEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
ecvEntry2.place(x=300, y=140)
ecvEntry4 = customtkinter.CTkEntry(custViewEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
ecvEntry4.place(x=300, y=180)
ecvEntry5 = customtkinter.CTkEntry(custViewEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
ecvEntry5.place(x=300, y=220)
ecvEntry6 = customtkinter.CTkEntry(custViewEditFrame, width=240, text_font=("Calibri", 14), border_width=2, corner_radius=0)
ecvEntry6.place(x=300, y=260)
ecvLabel7 = customtkinter.CTkLabel(custViewEditFrame, text="Note: Only enter into the fields you wish to change, leave all others blank.", width=32, text_font=("Calibri", 14))
ecvLabel7.place(x=45, y=480)
custViewEditFrame.grid(row=0, column=0, sticky='nesw')

# Start the program on the sign-in page
switch_page(signInFrame)
window.mainloop()
