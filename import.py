""" Author  : Jerome Goldwin M.
    Date    : May 25, 2023
    Program : Simple Pharmacy Management System """

from tkinter import *
from tkinter import messagebox
from tkinter import tt

def check_password(event=None):
	password = entry_password.get()
	if password == "12345":
		# Password is correct, proceed with the main program
		login_window.destroy()  # Close the password prompt window
		main_program()
	else:
		# Password is incorrect, show an error message
		messagebox.showerror("Error", "Incorrect password")

def main_program():
	import sqlite3 as db
	from sqlite3 import Error
	con=db.connect("pharma.db")
	c=con.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS "pharm" (
				"id"	INTEGER,
				"num"	INTEGER NOT NULL UNIQUE,
				"name"	TEXT NOT NULL,
				"price"	INTEGER NOT NULL,
				"quantity"	INTEGER NOT NULL,
				"cata"	TEXT NOT NULL,
				"discount"	INTEGER,
				"Date"	DATE NOT NULL DEFAULT CURRENT_DATE,
				PRIMARY KEY("id" AUTOINCREMENT),
				UNIQUE("id")
		);''')

	c.execute('''CREATE TABLE IF NOT EXISTS "cus" (
				"id"	INTEGER NOT NULL,
				"c_num"	INTEGER NOT NULL UNIQUE,
				"c_name"	TEXT NOT NULL,
				"Date"	DATE NOT NULL DEFAULT CURRENT_DATE,
				"c_q"	INTEGER NOT NULL,
				"c_con"	INTEGER NOT NULL,
				"num"	INTEGER NOT NULL,
				FOREIGN KEY("num") REFERENCES "pharm"("num"),
				PRIMARY KEY("id")
		);''')

	c.execute('''CREATE TABLE IF NOT EXISTS "bill" (
				"id"	INTEGER NOT NULL UNIQUE,
				"num"	INTEGER NOT NULL,
				"name"	TEXT NOT NULL,
				"price"	INTEGER NOT NULL,
				"quantity"	TEXT NOT NULL,
				"cata"	TEXT NOT NULL,
				"discount"	INTEGER NOT NULL,
				"c_num"	INTEGER NOT NULL,
				"c_name"	INTEGER NOT NULL,
				"Date"	DATE NOT NULL,
				"c_q"	INTEGER NOT NULL,
				"c_con"	INTEGER NOT NULL,
				PRIMARY KEY("id")
		);''')

	con.commit()
	from datetime import date, timedelta, datetime
	ex = False
	c.execute('''SELECT Date FROM pharm;''')
	con.commit()
	exmed = []

	for row in c:
		expiration_date = datetime.strptime(row[0], "%Y-%m-%d").date() + timedelta(days=30)
		if expiration_date <= date.today():
			ex = True

	if ex:
		c.execute('''SELECT num, name FROM pharm WHERE Date <= date('now', '-30 days');''')
		con.commit()
		for row in c:
			exmed.append(f"{str(row[0])}, {row[1]}")

		if exmed:
			exmed_string = '\n'.join(exmed)
			messagebox.showinfo("Alert!", f"Medicine(s) expired\n{exmed_string}")


	root = Tk()
	root.title("Simple Pharmacy Managment System")
	root.configure(width=1500,height=600,bg='BLACK')
	var=-1

	def additem():
		try:
			e0=entry0.get()
			e1=entry1.get()
			e2=entry2.get()
			e3=entry3.get()
			e4=drd.get()
			e5=entry5.get()
			c.execute('''INSERT INTO pharm (num, name, price, quantity, cata, discount) VALUES (?, ?, ?, ?, ?, ?);''', (e0, e1, e2, e3, e4, e5,))
			con.commit()
			entry0.delete(0, END)
			entry1.delete(0, END)
			entry2.delete(0, END)
			entry3.delete(0, END)
			drd.set(str(""))
			entry5.delete(0, END)
			messagebox.showinfo("","Record Inserted")
		except Error as e:
			messagebox.showinfo("",e)


	def deleteitem():
		try:
			e0=entry0.get()
			c.execute("DELETE FROM pharm WHERE num=?;",(e0,))
			entry0.delete(0, End)
			entry1.delete(0, END)
			entry2.delete(0, END)
			entry3.delete(0, END)
			drd.set(str(""))
			entry5.delete(0, END)
			con.commit()
			messagebox.showinfo("","Record deleted")
		except Error as e:
			messagebox.showinfo("",e)

	def firstitem():
		entry0.delete(0, END)
		entry1.delete(0, END)
		entry2.delete(0, END)
		entry3.delete(0, END)
		drd.set(str(""))
		entry5.delete(0, END)
		try:
			c.execute("SELECT * FROM pharm ORDER BY ROWID LIMIT 1;")
			for row in c:
				i0=row[1]
				i1=row[2]
				i2=row[3]
				i3=row[4]
				i4=row[5]
				i5=row[6]
			entry0.insert(0,i0)
			entry1.insert(0,i1)
			entry2.insert(0,i2)
			entry3.insert(0,i3)
			drd.set(str(i4))
			entry5.insert(0,i5)
			con.commit()
		except Error as e:
			messagebox.showinfo(e)

	def nextitem():
		try:
			e0=entry0.get()
			c.execute('''SELECT B.*
						 FROM pharm AS A
						 LEFT JOIN pharm AS B ON A.ROWID = B.ROWID - 1
						 LEFT JOIN pharm AS C ON A.ROWID = C.ROWID + 1
						 WHERE A.num = ?;''',(e0,))

			entry0.delete(0, END)
			entry1.delete(0, END)
			entry2.delete(0, END)
			entry3.delete(0, END)
			drd.set(str(""))
			entry5.delete(0, END)
			for row in c:
				i0=row[1]
				i1=row[2]
				i2=row[3]
				i3=row[4]
				i4=row[5]
				i5=row[6]
				entry0.insert(0, str(i0))
				entry1.insert(0, str(i1))
				entry2.insert(0, str(i2))
				entry3.insert(0, str(i3))
				drd.set(str(i4))
				entry5.insert(0, str(i5))
				con.commit()
		except Error as e:
			messagebox.showinfo("", e)
	def previousitem():
		try:
			e0=entry0.get()
			c.execute('''SELECT C.*
						FROM pharm AS A
						LEFT JOIN pharm AS B ON A.ROWID = B.ROWID - 1
						LEFT JOIN pharm AS C ON A.ROWID = C.ROWID + 1

						WHERE A.num = ? ;''',(e0,))
			entry0.delete(0, END)
			entry1.delete(0, END)
			entry2.delete(0, END)
			entry3.delete(0, END)
			drd.set(str(""))
			entry5.delete(0, END)
			for row in c:
				i0=row[1]
				i1=row[2]
				i2=row[3]
				i3=row[4]
				i4=row[5]
				i5=row[6]
				entry0.insert(0, str(i0))
				entry1.insert(0, str(i1))
				entry2.insert(0, str(i2))
				entry3.insert(0, str(i3))
				drd.set(str(i4))
				entry5.insert(0, str(i5))
				con.commit()
		except Error as e:
				messagebox.showinfo("", e)


	def lastitem():
		entry0.delete(0, END)
		entry1.delete(0, END)
		entry2.delete(0, END)
		entry3.delete(0, END)
		drd.set(str(""))
		entry5.delete(0, END)
		try:
			c.execute("SELECT * FROM pharm ORDER BY ROWID DESC LIMIT 1;")
			con.commit()
			for row in c:
				i0=row[1]
				i1=row[2]
				i2=row[3]
				i3=row[4]
				i4=row[5]
				i5=row[6]
			entry0.insert(0,i0)
			entry1.insert(0,i1)
			entry2.insert(0,i2)
			entry3.insert(0,i3)
			drd.set(str(i4))
			entry5.insert(0,i5)
			con.commit()
		except Error as e:
			messagebox.showinfo(e)


	def updateitem():
		try:
			e0 = entry0.get()
			e1 = entry1.get()
			e2 = entry2.get()
			e3 = entry3.get()
			e4=drd.get()
			e5 = entry5.get()
			upi=(e1,e2,e3,e4,e5,e0)
			c.execute("UPDATE pharm SET name=?,price=?,quantity=?,cata=?,discount=? WHERE num=?;",(upi))
			con.commit()
			messagebox.showinfo("","Record Updated")
		except Error as e:
			messagebox.showinfo("",e)


	def searchitem():
		try:
			e0 = entry0.get()
			si=(e0)
			c.execute("SELECT * FROM pharm WHERE num=?;",(e0,))
			for row in c:
				i0=row[1]
				i1=row[2]
				i2=row[3]
				i3=row[4]
				i4=row[5]
				i5=row[6]
				entry0.delete(0, END)
				entry0.insert(0, str(i0))
				entry1.insert(0, str(i1))
				entry2.insert(0, str(i2))
				entry3.insert(0, str(i3))
				drd.set(str(i4))
				entry5.insert(0, str(i5))
				con.commit()
		except Error as e:
			messagebox.showinfo("",e)
				
	def clearitem():
		entry0.delete(0, END)
		entry1.delete(0, END)
		entry2.delete(0, END)
		entry3.delete(0, END)
		drd.set(str("Category"))
		entry5.delete(0, END)
		entry6.delete(0, END)
		entry7.delete(0, END)
		entry8.delete(0, END)
		entry9.delete(0, END)
		entry10.delete(0, END)
		
	def addcus():
		try:
			e0 = entry0.get()
			e6 = entry6.get()
			e7 = entry7.get()
			e9 = entry9.get()
			e10 = entry10.get()
			c.execute("SELECT num FROM pharm;")
			con.commit()
			rows = c.fetchall()
			match_found = False
			for row in rows:
				if str(row[0]) == e0:
					match_found = True
					break
			
			if match_found == True:
				try:
					c.execute("INSERT INTO cus (c_num, c_name, c_q, c_con, num) VALUES (?,?,?,?,?);", (e6, e7, e9, e10, e0))
					con.commit()
					c.execute("UPDATE pharm SET quantity = quantity - ? WHERE num = ?;", (e9, e0))
					con.commit()
					entry6.delete(0, END)
					entry7.delete(0, END)
					entry8.delete(0, END)
					entry9.delete(0, END)
					entry10.delete(0, END)
					messagebox.showinfo("", "Record Inserted")
				except Error as e:
					messagebox.showinfo("", str(e))
			else:
				messagebox.showinfo("", "No medicine found with this number")
		except Error as e:
			messagebox.showinfo("", str(e))

			
	def nextcus():
		try:
			e6=entry6.get()
			e7=entry7.get()
			e9=entry9.get()
			e10=entry10.get()
			c.execute('''SELECT B.c_num, B.c_name, B.Date, B.c_q, B.c_con
						FROM cus AS A
						LEFT JOIN cus AS B ON A.ROWID = B.ROWID - 1
						LEFT JOIN cus AS C ON A.ROWID = C.ROWID + 1
						WHERE A.c_num = ?;''',(e6,))
			entry6.delete(0, END)
			entry7.delete(0, END)
			entry8.delete(0, END)
			entry9.delete(0, END)
			entry10.delete(0, END)
			for row in c:
				i0=row[0]
				i1=row[1]
				i2=row[2]
				i3=row[3]
				i4=row[4]
			entry6.insert(0, str(i0))
			entry7.insert(0, str(i1))
			entry8.insert(0, str(i2))
			entry9.insert(0, str(i3))
			entry10.insert(0, str(i4))
			con.commit()
		except Error as e:
			messagebox.showinfo("", e)
			
	def prevcus():
		try:
			e6=entry6.get()
			e7=entry7.get()
			e9=entry9.get()
			e10=entry10.get()
			c.execute('''SELECT C.c_num, C.c_name, C.Date, C.c_q, C.c_con
						FROM cus AS A
						LEFT JOIN cus AS B ON A.ROWID = B.ROWID - 1
						LEFT JOIN cus AS C ON A.ROWID = C.ROWID + 1
						WHERE A.c_num = ? ;''',(e6,))
			entry6.delete(0, END)
			entry7.delete(0, END)
			entry8.delete(0, END)
			entry9.delete(0, END)
			entry10.delete(0, END)

			for row in c:
				i0=row[0]
				i1=row[1]
				i2=row[2]
				i3=row[3]
				i4=row[4]
			entry6.insert(0, str(i0))
			entry7.insert(0, str(i1))
			entry8.insert(0, str(i2))
			entry9.insert(0, str(i3))
			entry10.insert(0, str(i4))
			con.commit()
		except Error as e:
				messagebox.showinfo("", e)
				
	def searchcus():
		try:
			e6 = entry6.get()
			c.execute("SELECT * FROM cus WHERE c_num=?;",(e6,))
			entry6.delete(0, END)
			entry7.delete(0, END)
			entry8.delete(0, END)
			entry9.delete(0, END)
			entry10.delete(0, END)
			for row in c:
				i0=row[1]
				i1=row[2]
				i2=row[3]
				i3=row[4]
				i4=row[5]
			entry6.insert(0, str(i0))
			entry7.insert(0, str(i1))
			entry8.insert(0, str(i2))
			entry9.insert(0, str(i3))
			entry10.insert(0, str(i4))
			con.commit()
		except Error as e:
			messagebox.showinfo("",e)
			
	def deleteitem():
		try:
			e0=entry0.get()
			c.execute("DELETE FROM pharm WHERE num=?;",(e0,))
			entry0.delete(0, End)
			entry1.delete(0, END)
			entry2.delete(0, END)
			entry3.delete(0, END)
			drd.set(str(""))
			entry5.delete(0, END)
			messagebox.showinfo("","Record deleted")
		except Error as e:
			messagebox.showinfo("",e)
				
	def sbd():
		try:
			e8 = entry8.get()
			c.execute("SELECT * FROM cus WHERE Date=? ORDER BY ROWID ASC LIMIT 1;",(e8,))
			for row in c:
				i0 = row[1]
				i1 = row[2]
				i2 = row[3]
				i3 = row[4]
				i4 = row[5]
			entry6.delete(0, END)
			entry7.delete(0, END)
			entry8.delete(0, END)
			entry9.delete(0, END)
			entry10.delete(0, END)
			entry6.insert(0, str(i0))
			entry7.insert(0, str(i1))
			entry8.insert(0, str(i2))
			entry9.insert(0, str(i3))
			entry10.insert(0, str(i4))

			con.commit()
		except Error as e:
			messagebox.showinfo("", e)
			
	def nsbd():
		try:
			e6=entry6.get()
			e8=entry8.get()
			c.execute('''SELECT B.*
						FROM cus AS A
						LEFT JOIN cus AS B ON A.ROWID = B.ROWID - 1
						LEFT JOIN cus AS C ON A.ROWID = C.ROWID + 1
						WHERE A.c_num = ? AND A.Date = ?;''',(e6,e8,))
			entry6.delete(0, END)
			entry7.delete(0, END)
			entry8.delete(0, END)
			entry9.delete(0, END)
			entry10.delete(0, END)
			for row in c:
				i0=row[1]
				i1=row[2]
				i2=row[3]
				i3=row[4]
				i4=row[5]
			entry6.insert(0, str(i0))
			entry7.insert(0, str(i1))
			entry8.insert(0, str(i2))
			entry9.insert(0, str(i3))
			entry10.insert(0, str(i4))
			con.commit()
		except Error as e:
			messagebox.showinfo("", e)
			
	def psbd():
		try:
			e6 = entry6.get()
			e8 = entry8.get()
			c.execute('''SELECT C.*
						FROM cus AS A
						LEFT JOIN cus AS B ON A.ROWID = B.ROWID - 1
						LEFT JOIN cus AS C ON A.ROWID = C.ROWID + 1
						WHERE A.c_num = ? AND A.Date = ?;''',(e6,e8,))
						
			entry6.delete(0, END)
			entry7.delete(0, END)
			entry8.delete(0, END)
			entry9.delete(0, END)
			entry10.delete(0, END)
			for row in c:
				i0 = row[1]
				i1 = row[2]
				i2 = row[3]
				i3 = row[4]
				i4 = row[5]
			entry6.insert(0, str(i0))
			entry7.insert(0, str(i1))
			entry8.insert(0, str(i2))
			entry9.insert(0, str(i3))
			entry10.insert(0, str(i4))
			con.commit()
		except Error as e:
			messagebox.showinfo("", e)
			
	def dd():
		options = [
		"Inflammation",
		"Allergy",
		"Flu",
		"Common-cold",
		"Cough"
		]
		global drd
		drd = StringVar()
		drd.set( "Category" )
		drop = OptionMenu( root , drd , *options )
		drop.config(width=16)
		drop.grid(row=5,column=1, padx=10, pady=10)

	def addbill():
			e0=entry0.get()
			e1=entry1.get()
			e2=entry2.get()
			e3=entry3.get()
			e4=drd.get()
			e5=entry5.get()
			e6=entry6.get()
			e7=entry7.get()
			e8=entry8.get()
			e9=entry9.get()
			e10=entry10.get()
			c.execute('''INSERT INTO bill VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?);''',(e0,e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,))
			con.commit()
			messagebox.showinfo("", "Record Inserted")
			
	def showbill():
		rows=False
		try:
			e6=entry6.get()
			e8=entry8.get()
			c.execute('''SELECT * FROM bill where c_num=? OR Date=?;''',(e6,e8,))
			entry0.delete(0, END)
			entry1.delete(0, END)
			entry2.delete(0, END)
			entry3.delete(0, END)
			drd.set(str(""))
			entry5.delete(0, END)
			entry6.delete(0, END)
			entry7.delete(0, END)
			entry8.delete(0, END)
			entry9.delete(0, END)
			entry10.delete(0, END)
			for row in c:
				i0=row[1]
				i1=row[2]
				i2=row[3]
				i3=row[4]
				i4=row[5]
				i5=row[6]
				i6=row[7]
				i7=row[8]
				i8=row[9]
				i9=row[10]
				i10=row[11]
				rows = True
			if rows:
				entry0.insert(0, str(i0))
				entry1.insert(0, str(i1))
				entry2.insert(0, str(i2))
				entry3.insert(0, str(i3))
				drd.set(str(i4))
				entry5.insert(0, str(i5))
				entry6.insert(0, str(i6))
				entry7.insert(0, str(i7))
				entry8.insert(0, str(i8))
				entry9.insert(0, str(i9))
				entry10.insert(0, str(i10))
			else:
				 messagebox.showinfo("","No record found")
			con.commit()
			
		except Error as e:
			messagebox.showinfo("",e)

		
	def nb():
		try:
			e6=entry6.get()
			c.execute('''SELECT B.*
						FROM bill AS A
						LEFT JOIN bill AS B ON A.ROWID = B.ROWID - 1
						LEFT JOIN bill AS C ON A.ROWID = C.ROWID + 1
						WHERE A.c_num = ?;''',(e6,))
			entry0.delete(0, END)
			entry1.delete(0, END)
			entry2.delete(0, END)
			entry3.delete(0, END)
			drd.set(str(""))
			entry5.delete(0, END)
			entry6.delete(0, END)
			entry7.delete(0, END)
			entry8.delete(0, END)
			entry9.delete(0, END)
			entry10.delete(0, END)
			for row in c:
				i0=row[1]
				i1=row[2]
				i2=row[3]
				i3=row[4]
				i4=row[5]
				i5=row[6]
				i6=row[7]
				i7=row[8]
				i8=row[9]
				i9=row[10]
				i10=row[11]
				entry0.insert(0, str(i0))
				entry1.insert(0, str(i1))
				entry2.insert(0, str(i2))
				entry3.insert(0, str(i3))
				drd.set(str(i4))
				entry5.insert(0, str(i5))
				entry6.insert(0, str(i6))
				entry7.insert(0, str(i7))
				entry8.insert(0, str(i8))
				entry9.insert(0, str(i9))
				entry10.insert(0, str(i10))
			con.commit()
		except Error as e:
			messagebox.showinfo("",e)
			
		
	def pb():
		try:
			e6=entry6.get()
			c.execute('''SELECT C.*
						FROM bill AS A
						LEFT JOIN bill AS B ON A.ROWID = B.ROWID - 1
						LEFT JOIN bill AS C ON A.ROWID = C.ROWID + 1
						WHERE A.c_num = ?;''',(e6,))
			entry0.delete(0, END)
			entry1.delete(0, END)
			entry2.delete(0, END)
			entry3.delete(0, END)
			drd.set(str(""))
			entry5.delete(0, END)
			entry6.delete(0, END)
			entry7.delete(0, END)
			entry8.delete(0, END)
			entry9.delete(0, END)
			entry10.delete(0, END)
			for row in c:
				i0=row[1]
				i1=row[2]
				i2=row[3]
				i3=row[4]
				i4=row[5]
				i5=row[6]
				i6=row[7]
				i7=row[8]
				i8=row[9]
				i9=row[10]
				i10=row[11]
			entry0.insert(0, str(i0))
			entry1.insert(0, str(i1))
			entry2.insert(0, str(i2))
			entry3.insert(0, str(i3))
			drd.set(str(i4))
			entry5.insert(0, str(i5))
			entry6.insert(0, str(i6))
			entry7.insert(0, str(i7))
			entry8.insert(0, str(i8))
			entry9.insert(0, str(i9))
			entry10.insert(0, str(i10))
			con.commit()
		except Error as e:
			messagebox.showinfo("",e)
		
	label= Label(root,text="PHARMACY MANAGEMENT SYSTEM ",bg="black",fg="white",font=("Times", 30))
	label0=Label(root,text="ENTER ITEM NUMBER",bg="red",relief="ridge",fg="white",font=("Times", 12),width=25)
	entry0=Entry(root , font=("Times", 12))
	label1=Label(root,text="ENTER ITEM NAME",bg="red",relief="ridge",fg="white",font=("Times", 12),width=25)
	entry1=Entry(root , font=("Times", 12))
	label2=Label(root, text="ENTER ITEM PRICE",bd="2",relief="ridge",height="1",bg="red",fg="white", font=("Times", 12),width=25)
	entry2= Entry(root, font=("Times", 12))
	label3=Label(root, text="ENTER ITEM QUANTITY",bd="2",relief="ridge",bg="red",fg="white", font=("Times", 12),width=25)
	entry3= Entry(root, font=("Times", 12))
	label4=Label(root, text="ENTER ITEM CATEGORY",bd="2",relief="ridge",bg="red",fg="white", font=("Times", 12),width=25) 
	label5=Label(root, text="ENTER ITEM DISCOUNT",bg="red",relief="ridge",fg="white", font=("Times", 12),width=25)
	entry5= Entry(root, font=("Times", 12))
	label6=Label(root, text="CUSTOMER NUMBER",bg="red",relief="ridge",fg="white", font=("Times", 12),width=25)
	entry6= Entry(root, font=("Times", 12))
	label7=Label(root, text="CUSTOMER NAME",bg="red",relief="ridge",fg="white", font=("Times", 12),width=25)
	entry7= Entry(root, font=("Times", 12))
	label8=Label(root, text="PURCHASE DATE",bg="red",relief="ridge",fg="white", font=("Times", 12),width=25)
	entry8= Entry(root, font=("Times", 12))
	label9=Label(root, text="PURCHASE QUANTITY",bg="red",relief="ridge",fg="white", font=("Times", 12),width=25)
	entry9= Entry(root, font=("Times", 12))
	label10=Label(root, text="CONTACT",bg="red",relief="ridge",fg="white", font=("Times", 12),width=25)
	entry10= Entry(root, font=("Times", 12))
	button1= Button(root, text="ADD ITEM", bg="white", fg="black", width=20, font=("Times", 12),command=additem)
	button2= Button(root, text="DELETE ITEM", bg="white", fg="black", width =20, font=("Times", 12),command=deleteitem)
	button3= Button(root, text="VIEW FIRST ITEM" , bg="white", fg="black", width =20, font=("Times", 12),command=firstitem)
	button4= Button(root, text="VIEW NEXT ITEM" , bg="white", fg="black", width =20, font=("Times", 12), command=nextitem)
	button5= Button(root, text="VIEW PREVIOUS ITEM", bg="white", fg="black", width =20, font=("Times", 12),command=previousitem)
	button6= Button(root, text="VIEW LAST ITEM", bg="white", fg="black", width =20, font=("Times", 12),command=lastitem)
	button7= Button(root, text="UPDATE ITEM", bg="white", fg="black", width =20, font=("Times", 12),command=updateitem)
	button8= Button(root, text="SEARCH ITEM", bg="white", fg="black", width =20, font=("Times", 12),command=searchitem)
	button9= Button(root, text="CLEAR SCREEN", bg="cyan", fg="black", width=20, font=("Times", 12),command=clearitem)
	button10= Button(root, text="ADD CUSTOMER", bg="white", fg="black", width=20, font=("Times", 12),command=addcus)
	button11= Button(root, text="NEXT CUSTOMER", bg="white", fg="black", width=20, font=("Times", 12),command=nextcus)
	button12= Button(root, text="PREVIOUS CUSTOMER", bg="white", fg="black", width=20, font=("Times", 12),command=prevcus)
	button13= Button(root, text="DATE SEARCH CUSTOMER", bg="white", fg="black", width=23, font=("Times", 12),command=sbd)
	button14= Button(root, text="SEARCH CUSTOMER", bg="white", fg="black", width=20, font=("Times", 12),command=searchcus)
	button15= Button(root, text="SHOW BILL", bg="white", fg="black", width=20, font=("Times", 12),command=showbill)
	button16= Button(root, text="ADD BILL", bg="white", fg="black", width=20, font=("Times", 12),command=addbill)
	button17= Button(root, text="NEXT BILL", bg="white", fg="black", width=20, font=("Times", 12),command=nb)
	button18= Button(root, text="PREVIOUS BILL", bg="white", fg="black", width=20, font=("Times", 12),command=pb)
	button20= Button(root, text=">", bg="white", fg="black", width=1, font=("Times", 12),command=nsbd)
	button21= Button(root, text="<", bg="white", fg="black", width=1, font=("Times", 12),command=psbd)

	label.grid(columnspan=6, padx=10, pady=10)
	label0.grid(row=1,column=0, sticky=W, padx=10, pady=10)
	label1.grid(row=2,column=0, sticky=W, padx=10, pady=10)
	label2.grid(row=3,column=0, sticky=W, padx=10, pady=10)
	label3.grid(row=4,column=0, sticky=W, padx=10, pady=10)
	label4.grid(row=5,column=0, sticky=W, padx=10, pady=10)
	label5.grid(row=6,column=0, sticky=W, padx=10, pady=10)
	label6.grid(row=7,column=0, sticky=W, padx=10, pady=10)
	label7.grid(row=8,column=0, sticky=W, padx=10, pady=10)
	label8.grid(row=9,column=0, sticky=W, padx=10, pady=10)
	label9.grid(row=10,column=0, sticky=W, padx=10, pady=10)
	label10.grid(row=11,column=0, sticky=W, padx=10, pady=10)
	entry0.grid(row=1,column=1, padx=40, pady=10)
	entry1.grid(row=2,column=1, padx=40, pady=10)
	entry2.grid(row=3,column=1, padx=10, pady=10)
	entry3.grid(row=4,column=1, padx=10, pady=10)
	dd()
	entry5.grid(row=6,column=1, padx=10, pady=10)
	entry6.grid(row=7,column=1, padx=10, pady=10)
	entry7.grid(row=8,column=1, padx=10, pady=10)
	entry8.grid(row=9,column=1, padx=10, pady=10)
	entry9.grid(row=10,column=1, padx=10, pady=10)
	entry10.grid(row=11,column=1, padx=10, pady=10)
	button1.grid(row=1,column=4, padx=40, pady=10)
	button2.grid(row=1,column=5, padx=40, pady=10)
	button3.grid(row=2,column=4, padx=40, pady=10)
	button4.grid(row=3,column=4, padx=40, pady=10)
	button5.grid(row=3,column=5, padx=40, pady=10)
	button6.grid(row=2,column=5, padx=40, pady=10)
	button7.grid(row=4,column=4, padx=40, pady=10)
	button8.grid(row=4,column=5, padx=40, pady=10)
	button9.grid(row=11,column=5, padx=40, pady=10)
	button10.grid(row=7,column=4, padx=40, pady=10)
	button11.grid(row=8,column=4, padx=40, pady=10)
	button12.grid(row=8,column=5, padx=40, pady=10)
	button13.grid(row=7,column=5, padx=40, pady=10)
	button14.grid(row=9,column=5, padx=40, pady=10)
	button15.grid(row=8,column=5, padx=40, pady=10)
	button15.grid(row=11,column=4, padx=40, pady=10)
	button16.grid(row=9,column=4, padx=40, pady=10)
	button17.grid(row=10,column=4, padx=40, pady=10)
	button18.grid(row=10,column=5, padx=40, pady=10)
	button20.place(x=1022,y=390)
	button21.place(x=786,y=390)

	root.mainloop()

# Create the password prompt window
login_window = Tk()
login_window.title("Password Prompt")

# Set a themed style for the window
style = ttk.Style(login_window)
style.theme_use("clam")

# Create a frame for the content
content_frame = ttk.Frame(login_window, padding=20)
content_frame.pack()

# Create a label and entry for the password
label_password = ttk.Label(content_frame, text="Password:")
label_password.pack()
entry_password = ttk.Entry(content_frame, show="*")
entry_password.pack()

# Bind the Enter key to the check_password function
entry_password.bind("<Return>", check_password)

# Create a button to check the password
button_login = ttk.Button(content_frame, text="Login", command=check_password)
button_login.pack()

# Run the password prompt window
login_window.mainloop()

