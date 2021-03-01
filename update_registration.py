#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:25:07 2021

This sctipt allows to update the Registration table in ACar DB.
similar to:
    INSERT INTO registration(v.id, new_owner, date.now())    #! autocommit off

steps: 
    UPDATE registration WHERE 'to' IS NULL
    INSERT .... COMMIT;
    
@author: sungria
"""

import psycopg2

### connect to the DB
try:
    connection = psycopg2.connect(
        host = "localhost",
        database = "ACar",
        user = "postgres",
        password = "")
except psycopg2.Error as err:
    print("Connection to the database failed: ", err)


### create a cursor
cursor = connection.cursor()

### execute a single query cursor.execute("query")
### execute multy-line query cursor.executescript
# cursor.executescript("SQL-query")

### get results: fetchall, fetchone, fetchmany
# cursor.fetchone()

### get data to write
name = input("Enter new owner's name: ")

names = []
cursor.execute("SELECT name FROM owner;")
owners = cursor.fetchall()
for i in range(len(owners)):
    names.append(owners[i][0])

### check if name is in owner table, 
### if not, add new to the table owners, print the message
if name not in names:
    sql_insert = ("INSERT INTO owner(name) VALUES (%s);")
    cursor.execute(sql_insert, (name, ))
    connection.commit() 
    print ("New owner added to DB.")
else: 
    pass

vehicle = input("Enter car number: ")

cars = []
cursor.execute("SELECT licence FROM vehicle;")
lics = cursor.fetchall()
for j in range(len(lics)):
    cars.append(lics[j][0])

### check if car number is in vehicle table, 
### if not, print the error message
if vehicle not in cars:
    print ("The vehicle is not found.")
    cursor.close()
    connection.close()
    print ("Connection closed")
else:
    pass

sql_sel = ''' SELECT vehicleid,
                     registrationnum,
                    "From",
                    "To"
             FROM registration 
             JOIN vehicle AS v ON vehicleid = v.id WHERE v.licence = (%s);      
'''

cursor.execute(sql_sel, (vehicle, ))
regs = cursor.fetchall()
vid, regnum, dto, dfrom = [], [], [], []
for k in range(len(regs)):
    vid.append(regs[k][0])
    regnum.append(int(regs[k][1]))
    dto.append(regs[k][2])
    dfrom.append(regs[k][3])

newreg = max(regnum) + 1

sql_upd = '''UPDATE registration SET "To" = now()
             WHERE "To" IS NULL AND vehicleid = (%s);'''
cursor.execute(sql_upd, (vid[0], ))
connection.commit()
print("Previous record is updated")
             

sql_newreg = '''INSERT INTO registration(vehicleid, ownerid, registrationnum, "From")
                SELECT v.id, o.id, (%s), now()
                FROM vehicle AS v, owner AS o
                WHERE v.licence = (%s) AND o.name = (%s);'''
ins_data = (newreg, vehicle, name)
cursor.execute(sql_newreg, ins_data)
connection.commit() 
print ("New registration record added to DB.")    

### print("Current owner(s): ... 
### ans = input("Update record (Y/n)?")
### if input == lowercase('Y') or input == '':
###    do sql_upd =  '''UPDATE registration SET "To" = now()
###                     WHERE "To" = NULL AND vehicleid = 1; '''


cursor.close()
connection.close()