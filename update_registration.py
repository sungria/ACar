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
    
@author: sungria\
    
    TODO:
        - add timers on inputs, if it more that 2 minutes, close connection
        - add user id
        
"""

import psycopg2
import time

# custom
import db_connect


### connect to the DB
try:
    connection = db_connect.conn()
    print ("DB connected")
except psycopg2.Error as err:
    print("Connection to the database failed: ", err)


# countdown timer to limit open connection to db  
def countdown(t):
    print('Countdown is going')
    while t: 
        #mins, secs = divmod(t, 60) 
        #timer = '{:02d}:{:02d}'.format(mins, secs) 
        #print(timer, end="\r") 
        print ('.', end="\r")
        time.sleep(1) 
        t -= 1
    print('Fire in the hole!!!') 


### create a cursor
cursor = connection.cursor()

###### Get the registration, owner and car info...
vin = input("Enter VIN: ")

### check if car number is in vehicle table, 
### if not, print the error message
cars = []
cursor.execute("SELECT vin FROM vehicle WHERE vin = (%s);", (vin, ))
lics = cursor.fetchall()
if lics[0] == '':
    print ("The vehicle is not found.")
    cursor.close()
    connection.close()
    print ("Connection closed")
else:
    sql_read_car = '''SELECT b.name AS brand, 
                             m.name AS model, 
                             o.name AS owner, 
                             r."From" AS "reg. from"
                      FROM registration AS r
                        JOIN vehicle AS v ON v.id = r.vehicleid
                        JOIN brand AS b ON b.id = v.brand_id
                        JOIN model AS m ON m.id = v.model_id
                        JOIN owner AS o ON o.id = r.ownerid
                      WHERE r."To" IS NULL
                        AND v.vin = (%s); '''


    cursor.execute(sql_read_car, (vin, ))
    vehic = cursor.fetchall()[0]
    print ("Car information: \n brand: {}\n model: {}\n owner: {}\n reg. from: {}\n".format(vehic[0], vehic[1], vehic[2], vehic[3]))
    
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
              From: {}, To: now'''.format(reg_info[0], reg_info[1], reg_info[2]) )


reg_input = input("Do you want to add new registration (Y/n)? ").lower()
print (reg_input)
if reg_input == 'y' or reg_input == '':
    name = input("Enter new owner's name: ")
    #uid = input("Enter owner's ID: ")
    
### check if name is in owner table, 
### if not, add new to the table owners, print the message
    cursor.execute("SELECT name FROM owner WHERE name = (%s) ;", (name, ))
    owners = cursor.fetchall()
    if owners[0] == '':
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
