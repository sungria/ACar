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

import db_connect

### connect to the DB
try:
    connection = db_connect.conn()
    print ("DB connected")
except psycopg2.Error as err:
    print("Connection to the database failed: ", err)
    # exit()


### create a cursor
cursor = connection.cursor()

### execute a single query cursor.execute("query")
### execute multy-line query cursor.executescript
# cursor.executescript("SQL-query")

### get results: fetchall, fetchone, fetchmany
# cursor.fetchone()

###### Get the registration, owner and car info...
vin = input("Enter VIN: ")

cars = []
cursor.execute("select vin from vehicle;")
lics = cursor.fetchall()
for j in range(len(lics)):
    cars.append(lics[j][0])

### check if car number is in vehicle table, 
### if not, print the error message
if vin not in cars:
    print ("The vehicle is not found.")
    cursor.close()
    connection.close()
    print ("Connection closed")
else:
    ### get car info from the DB
    sql_read_car = '''SELECT brand, model, year 
                      FROM 
                        (SELECT v.vin,
                            b.name as brand,
                            m.name as model,
                            m.year
                          FROM brand as b
                          JOIN model as m ON b.id = m.brand_id
                          JOIN vehicle AS v ON v.model_id = m.id) AS sub
                    WHERE vin = (%s);'''
    cursor.execute(sql_read_car, (vin, ))
    vehic = cursor.fetchall()[0]
    print ("Car information: brand: {}, model: {}, year: {}".format(vehic[0], vehic[1], vehic[2]))
    
    ### get registration info from DB
    sql_read_reg = ''' WITH cte_reg AS (
                            SELECT o.name, 
                                   r.registrationnum AS regnum,
                                   r."From",
                                   r."To",
                                   v.vin
                            FROM registration AS r
                            JOIN owner AS o ON o.id = r.ownerid
                            JOIN vehicle AS v ON v.id = r.vehicleid)

                            SELECT name, regnum, "From", "To"
                            FROM cte_reg
                            WHERE vin = (%s) AND "To" IS NULL;'''
    cursor.execute(sql_read_reg, (vin, ))
    reg_info = cursor.fetchone()
    print ('''Current registration: 
              owner: {}, regnum: {}, 
              From: {}, To: {}'''.format(reg_info[0], reg_info[1], reg_info[2], reg_info[3]) )


reg_input = input("Do you want to add new registration (Y/n)? ").lower()
print (reg_input)
if reg_input == 'y' or reg_input == '':
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
    
    new_num = input("ENTER new registratin number (not longer than 10 characters): ")
    
    sql_upd_reg = '''UPDATE registration r
                     SET "To" = now()
                     FROM vehicle v
                     WHERE r.vehicleid = v.id AND v.vin = (%s) AND r."To" IS NULL'''
    cursor.execute(sql_upd_reg, (vin, ))
    
    sql_newreg = '''INSERT INTO registration(vehicleid, ownerid, registrationnum, "From")
                SELECT v.id, o.id, (%s), now()
                FROM vehicle AS v, owner AS o
                WHERE v.vin = (%s) AND o.name = (%s);'''
    ins_data = (new_num, vin, name)
    cursor.execute(sql_newreg, ins_data)
    connection.commit() 
    print ("New registration record added to DB.") 
else:
    print("Goodbye!")
    

cursor.close()
connection.close()     




### get data to write
# name = input("Enter new owner's name: ")

# names = []
# cursor.execute("SELECT name FROM owner;")
# owners = cursor.fetchall()
# for i in range(len(owners)):
#     names.append(owners[i][0])

# ### check if name is in owner table, 
# ### if not, add new to the table owners, print the message
# if name not in names:
#     sql_insert = ("INSERT INTO owner(name) VALUES (%s);")
#     cursor.execute(sql_insert, (name, ))
#     connection.commit() 
#     print ("New owner added to DB.")
# else: 
#     pass



# sql_sel = ''' SELECT vehicleid,
#                      registrationnum,
#                     "From",
#                     "To"
#              FROM registration 
#              JOIN vehicle AS v ON vehicleid = v.id WHERE v.licence = (%s);      
# '''

# cursor.execute(sql_sel, (vin, ))
# regs = cursor.fetchall()
# vid, regnum, dto, dfrom = [], [], [], []
# for k in range(len(regs)):
#     vid.append(regs[k][0])
#     regnum.append(int(regs[k][1]))
#     dto.append(regs[k][2])
#     dfrom.append(regs[k][3])

# newreg = max(regnum) + 1

# sql_upd = '''UPDATE registration SET "To" = now()
#              WHERE "To" IS NULL AND vehicleid = (%s);'''
# cursor.execute(sql_upd, (vid[0], ))
# connection.commit()
# print("Previous record is updated")
             

# sql_newreg = '''INSERT INTO registration(vehicleid, ownerid, registrationnum, "From")
#                 SELECT v.id, o.id, (%s), now()
#                 FROM vehicle AS v, owner AS o
#                 WHERE v.licence = (%s) AND o.name = (%s);'''
# ins_data = (newreg, vehicle, name)
# cursor.execute(sql_newreg, ins_data)
# connection.commit() 
# print ("New registration record added to DB.")    

# ### print("Current owner(s): ... 
# ### ans = input("Update record (Y/n)?")
# ### if input == lowercase('Y') or input == '':
# ###    do sql_upd =  '''UPDATE registration SET "To" = now()
# ###                     WHERE "To" = NULL AND vehicleid = 1; '''


# cursor.close()
# connection.close()